import os
import json
import re
import logging
from typing import Any, Dict, Optional

from google import genai
from google.genai.types import GenerateContentConfig, HttpOptions
from pydantic import BaseModel

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_core.memory import ConversationBufferMemory
from langchain_google_vertexai import ChatVertexAI

from config.settings import settings


logger = logging.getLogger("zelta.copilot")
if not logger.handlers:
    logging.basicConfig(level=logging.INFO)


class CopilotResult(BaseModel):
    summary: Optional[str] = None
    reasoning: Optional[str] = None
    action: Optional[str] = None
    what_this_means_for_you: Optional[str] = None
    bias_explanation: Optional[str] = None
    confidence_note: Optional[str] = None
    bq_alert: Optional[str] = None
    context_summary: Optional[str] = None


class ZeltaCopilot:
    """
    Vertex AI-backed Co-Pilot for ZELTA.
    Uses the Google Gen AI SDK on Vertex AI.
    """

    SYSTEM_PROMPT = """
You are ZELTA, a friendly money guide for Nigerian university students.

Your job is to explain ZELTA results in simple, calm, everyday English.
Pretend you are talking to a student who has little or no finance knowledge.

You should:
- explain what the market is doing
- explain what it means for the student
- explain what action to take
- use real Naira amounts
- use student life examples when helpful

You must NEVER:
- sound like a textbook
- use heavy finance jargon
- be vague
- be dramatic

Keep answers short, clear, and practical.
Always end with a clear verdict and Naira amount when relevant.

If you are returning JSON, return ONLY valid JSON.
If you are answering a question, keep the answer under 120 words.
""".strip()

    JSON_SYSTEM_PROMPT = """
You are a strict JSON generator.

Rules:
- Return ONLY valid JSON.
- Do NOT wrap in markdown fences.
- Do NOT add commentary before or after JSON.
- Do NOT truncate output.
- Use double quotes for all strings.
- If a field is unknown, use null.
- Keep the action field short and direct.
- Keep the wording simple enough for a student to understand.
""".strip()

    def __init__(self):
        project_id = (
            getattr(settings, "GOOGLE_CLOUD_PROJECT", None)
            or os.getenv("GOOGLE_CLOUD_PROJECT")
        )
        location = (
            getattr(settings, "GOOGLE_CLOUD_LOCATION", None)
            or os.getenv("GOOGLE_CLOUD_LOCATION", "global")
        )

        if not project_id:
            raise ValueError(
                "GOOGLE_CLOUD_PROJECT not set. Add it to your environment or settings."
            )

        self.client = genai.Client(
            vertexai=True,
            project=project_id,
            location=location,
            http_options=HttpOptions(api_version="v1"),
        )

        self.model = os.getenv(
            "VERTEX_GEMINI_MODEL",
            os.getenv("GEMINI_MODEL", "gemini-1.5-flash"),
        )

        # LangChain ChatVertexAI for answer_question (with memory)
        self.langchain_llm = ChatVertexAI(
            model_name=self.model,
            project=project_id,
            location=location,
            temperature=0.3,
        )

        # Conversation memory with window (keep last 5 exchanges)
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True,
            output_key="answer",
        )

    @staticmethod
    def _response_schema() -> Dict[str, Any]:
        return {
            "type": "OBJECT",
            "properties": {
                "summary": {"type": "STRING"},
                "reasoning": {"type": "STRING"},
                "action": {"type": "STRING"},
                "what_this_means_for_you": {"type": "STRING"},
                "bias_explanation": {"type": "STRING"},
                "confidence_note": {"type": "STRING"},
                "bq_alert": {"type": "STRING", "nullable": True},
                "context_summary": {"type": "STRING", "nullable": True},
            },
            "required": [
                "summary",
                "reasoning",
                "action",
                "what_this_means_for_you",
                "bias_explanation",
                "confidence_note",
                "bq_alert",
                "context_summary",
            ],
            "propertyOrdering": [
                "summary",
                "reasoning",
                "action",
                "what_this_means_for_you",
                "bias_explanation",
                "confidence_note",
                "bq_alert",
                "context_summary",
            ],
        }

    def _build_pipeline_prompt(self, data: Dict[str, Any]) -> str:
        decision = data.get("decision", {})
        stress = data.get("stress", {})
        bias = data.get("bias", {})
        nlp = data.get("nlp", {})
        kelly = data.get("allocation") or data.get("kelly", {})
        sharpe = data.get("sharpe") or data.get("score", {})

        headlines = nlp.get("scored_headlines", [])[:3]
        headline_text = "\n".join(
            f"- {h.get('title', 'Untitled')} ({h.get('sentiment_label', 'neutral')})"
            for h in headlines
        ) if headlines else "No headlines available"

        verdict = decision.get("verdict", "HOLD")
        invest_ngn = kelly.get("invest_ngn", 0)
        save_ngn = kelly.get("save_ngn", 0)
        hold_ngn = kelly.get("hold_ngn", 0)
        stress_score = stress.get("score", 50)
        stress_level = stress.get("level", "MODERATE")
        bias_name = bias.get("bias", "Rational")
        market_prob = round((decision.get("market_probability", 0.5) or 0) * 100)
        rational_prob = round((decision.get("rational_probability", 0.5) or 0) * 100)
        market_title = data.get("bayse", {}).get("market_title", "Nigerian financial market")
        decision_score = sharpe.get("decision_score", sharpe.get("score", 0))

        return f"""
You are ZELTA, a money guide for Nigerian university students.

Explain this result like you are talking to a student friend who does not understand finance.
The student cares about:
- hostel fees
- food money
- transport
- data
- side hustle money
- savings
- avoiding panic

HERE IS THE SITUATION:
- Market stress: {stress_score}/100 ({stress_level})
- Market event: "{market_title}"
- Crowd view: {market_prob}% are leaning YES
- ZELTA view: {rational_prob}% are leaning YES
- Difference between crowd and ZELTA: {abs(market_prob - rational_prob)}%
- Active money habit: {bias_name}
- What that means: {bias.get("explanation", "")}
- ZELTA recommendation: {verdict}
- Safe amount to invest: ₦{invest_ngn:,.0f}
- Amount to save: ₦{save_ngn:,.0f}
- Amount to keep as buffer: ₦{hold_ngn:,.0f}
- Decision quality score: {decision_score}

TOP NIGERIAN NEWS HEADLINES:
{headline_text}

HOW TO RESPOND:
- Use very simple English
- Talk like a calm, smart friend
- Connect the advice to student life
- Mention the actual Naira amounts
- Explain the "why" in a way anyone can understand
- Do not sound like a finance lecturer
- Do not use technical terms
- Keep each field short and clear

RETURN ONLY VALID JSON.
No markdown.
No backticks.
No extra text outside JSON.

{{
  "summary": "1 short sentence: what is happening in the market today in simple words.",
  "reasoning": "2 short sentences: why ZELTA made this recommendation.",
  "action": "1 short sentence: what the student should do with their money right now, with actual NGN amounts.",
  "what_this_means_for_you": "1-2 short sentences: explain how this affects the student's real life.",
  "bias_explanation": "1 short sentence: explain the active bias in simple language.",
  "confidence_note": "A note on the recommendation quality.",
  "bq_alert": "Short warning if needed or null.",
  "context_summary": "1 short line for the UI pills"
}}
""".strip()

    def _build_question_prompt(self, question: str, context: Dict[str, Any]) -> str:
        stress = context.get("stress", {})
        bias = context.get("bias", {})
        kelly = context.get("allocation") or context.get("kelly", {})
        decision = context.get("decision", {})
        bayse = context.get("bayse", {})

        invest_ngn = kelly.get("invest_ngn", 0)
        save_ngn = kelly.get("save_ngn", 0)
        hold_ngn = kelly.get("hold_ngn", 0)

        # CRITICAL CHANGE: We ask for plain text here to avoid the JSON truncation error
        return f"""
You are ZELTA, a money assistant for Nigerian university students.
A student just asked you a question. Reply like a calm smart friend.

The student asked: "{question}"

Their current situation:
- Market: "{bayse.get("market_title", "Market")}" ({stress.get("level", "MODERATE")})
- ZELTA recommendation: {decision.get("verdict", "HOLD")}
- Safe to invest: ₦{invest_ngn:,.0f}
- Save: ₦{save_ngn:,.0f} | Buffer: ₦{hold_ngn:,.0f}
- Active habit: {bias.get("bias", "Rational")}

INSTRUCTIONS:
- Answer the question directly and simply.
- Use plain text only.
- Do NOT use JSON formatting.
- Do NOT use backticks or markdown.
- Keep it under 100 words.
- End with a clear action involving the Naira amounts.
""".strip()

    @staticmethod
    def _extract_text(response) -> str:
        text = getattr(response, "text", None)
        if text:
            return text.strip()
        try:
            return response.candidates[0].content.parts[0].text.strip()
        except Exception:
            return ""

    @staticmethod
    def _fallback_result() -> Dict[str, Any]:
        return {
            "summary": None,
            "reasoning": None,
            "action": None,
            "what_this_means_for_you": None,
            "bias_explanation": None,
            "confidence_note": "AI explanation temporarily unavailable.",
            "bq_alert": None,
            "context_summary": None,
        }

    @staticmethod
    def _strip_code_fences(text: str) -> str:
        text = text.strip()
        if text.startswith("```"):
            text = re.sub(r"^```(?:json)?\s*", "", text, flags=re.IGNORECASE)
            text = re.sub(r"\s*```$", "", text)
        return text.strip()

    @staticmethod
    def _extract_first_json_object(text: str) -> str:
        text = ZeltaCopilot._strip_code_fences(text)
        start = text.find("{")
        if start == -1:
            return ""
        depth = 0
        in_string = False
        escape = False
        for i in range(start, len(text)):
            ch = text[i]
            if escape:
                escape = False
                continue
            if ch == "\\":
                escape = True
                continue
            if ch == '"':
                in_string = not in_string
                continue
            if in_string:
                continue
            if ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
                if depth == 0:
                    return text[start:i + 1]
        return ""

    @staticmethod
    def _parse_json_to_result(text: str) -> CopilotResult:
        json_text = ZeltaCopilot._extract_first_json_object(text)
        if not json_text:
            raise ValueError("No complete JSON object found in model output.")
        data = json.loads(json_text)
        return CopilotResult.model_validate(data)

    @staticmethod
    def _shorten_action(action: Optional[str]) -> Optional[str]:
        if not action:
            return action
        action = action.strip()
        verdict_match = re.search(
            r"(VERDICT:\s*(INVEST|SAVE|HOLD)\s*[₦N]?\s*[\d,]+(?:\.\d+)?)",
            action,
            flags=re.IGNORECASE,
        )
        if verdict_match:
            verdict = verdict_match.group(1).strip()
            prefix = action[:verdict_match.start()].strip()
            if prefix:
                prefix = re.split(r"(?<=[.!?])\s+", prefix)[0].strip()
                return f"{prefix} {verdict}".strip()
            return verdict
        parts = re.split(r"(?<=[.!?])\s+", action)
        return parts[0].strip() if parts else action

    @staticmethod
    def _normalize_question_answer(answer: str) -> str:
        answer = answer.strip()
        # If the model mistakenly returned JSON (despite instructions), strip it
        if answer.startswith("{"):
            try:
                data = json.loads(ZeltaCopilot._extract_first_json_object(answer))
                if "answer" in data:
                    answer = data["answer"]
            except:
                pass
        
        answer = re.sub(
            r"VERDICT:\s*(INVEST|SAVE|HOLD)\s*([₦N])?\s*([\d,]+)",
            r"VERDICT: \1 ₦\3",
            answer,
            flags=re.IGNORECASE,
        )
        return answer

    async def _call_gemini_json(self, prompt: str) -> CopilotResult:
        config = GenerateContentConfig(
            system_instruction=f"{self.SYSTEM_PROMPT}\n\n{self.JSON_SYSTEM_PROMPT}",
            temperature=0.2,
            max_output_tokens=2048,
            response_mime_type="application/json",
            response_schema=self._response_schema(),
        )
        response = await self.client.aio.models.generate_content(
            model=self.model,
            contents=prompt,
            config=config,
        )
        text = self._extract_text(response)
        if not text:
            return CopilotResult(confidence_note="AI explanation temporarily unavailable.")
        try:
            result = self._parse_json_to_result(text)
            result.action = self._shorten_action(result.action)
            return result
        except Exception as e:
            logger.warning("[ZELTA Co-Pilot] JSON parse error, attempting repair: %s", e)
            repair_prompt = f"Fix this into valid JSON only:\n{text}"
            repair_config = GenerateContentConfig(
                system_instruction=f"{self.SYSTEM_PROMPT}\n\n{self.JSON_SYSTEM_PROMPT}",
                temperature=0.0,
                response_mime_type="application/json",
            )
            try:
                repair_response = await self.client.aio.models.generate_content(
                    model=self.model, contents=repair_prompt, config=repair_config
                )
                repaired_text = self._extract_text(repair_response)
                return self._parse_json_to_result(repaired_text)
            except:
                return CopilotResult(confidence_note="AI explanation temporarily unavailable.")

    async def _call_gemini_text(self, prompt: str) -> str:
        config = GenerateContentConfig(
            system_instruction=self.SYSTEM_PROMPT,
            temperature=0.3,
            max_output_tokens=400,
        )
        response = await self.client.aio.models.generate_content(
            model=self.model,
            contents=prompt,
            config=config,
        )
        text = self._extract_text(response)
        return self._normalize_question_answer(text)

    async def run(self, data: Dict[str, Any]) -> Dict[str, Any]:
        prompt = self._build_pipeline_prompt(data)
        try:
            result = await self._call_gemini_json(prompt)
            return result.model_dump(exclude_none=False)
        except Exception as e:
            logger.error("[ZELTA Co-Pilot] Error: %s", e)
            return self._fallback_result()

    async def answer_question(self, question: str, context: Dict[str, Any]) -> str:
        """
        Answer a question using LangChain ChatPromptTemplate and memory.
        This is the only method that uses LangChain; _call_gemini_json remains unchanged.
        """
        try:
            # Build context string
            stress = context.get("stress", {})
            bias = context.get("bias", {})
            kelly = context.get("allocation") or context.get("kelly", {})
            decision = context.get("decision", {})
            bayse = context.get("bayse", {})

            invest_ngn = kelly.get("invest_ngn", 0)
            save_ngn = kelly.get("save_ngn", 0)
            hold_ngn = kelly.get("hold_ngn", 0)

            market_title = bayse.get("market_title", "Market")
            stress_level = stress.get("level", "MODERATE")
            verdict = decision.get("verdict", "HOLD")
            bias_name = bias.get("bias", "Rational")

            context_str = (
                f"Market: {market_title} ({stress_level})\n"
                f"ZELTA recommendation: {verdict}\n"
                f"Safe to invest: ₦{invest_ngn:,.0f}\n"
                f"Save: ₦{save_ngn:,.0f} | Buffer: ₦{hold_ngn:,.0f}\n"
                f"Active habit: {bias_name}"
            )

            # Create ChatPromptTemplate
            prompt_template = ChatPromptTemplate.from_messages([
                ("system", self.SYSTEM_PROMPT),
                MessagesPlaceholder(variable_name="chat_history"),
                ("human", (
                    "A student just asked you a question. Reply like a calm smart friend.\n\n"
                    "The student asked: \"{question}\"\n\n"
                    "Their current situation:\n{context_str}\n\n"
                    "INSTRUCTIONS:\n"
                    "- Answer the question directly and simply.\n"
                    "- Use plain text only.\n"
                    "- Do NOT use JSON formatting.\n"
                    "- Do NOT use backticks or markdown.\n"
                    "- Keep it under 100 words.\n"
                    "- End with a clear action involving the Naira amounts."
                )),
            ])

            # Format prompt with memory
            inputs = {
                "question": question,
                "context_str": context_str,
                "chat_history": self.memory.chat_memory.messages,
            }

            # Invoke the chain
            chain = prompt_template | self.langchain_llm
            response = await chain.ainvoke(inputs)

            # Extract answer
            answer = response.content if hasattr(response, "content") else str(response)

            # Update memory
            self.memory.chat_memory.add_user_message(question)
            self.memory.chat_memory.add_ai_message(answer)

            # Normalize answer
            answer = self._normalize_question_answer(answer)

            if not answer:
                return "Unable to answer right now. Check dashboard."

            return answer

        except Exception as e:
            logger.error("[ZELTA Co-Pilot] Question error: %s", e)
            return "Unable to answer right now. Check dashboard."
