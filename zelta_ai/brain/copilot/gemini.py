"""
ZELTA Co-Pilot — Student Finance Edition

Gemini-backed AI guide for Nigerian university students.
All prompts use student_model as the single source of truth for
survival state. No investment language. No finance jargon.
"""

from __future__ import annotations

import json
import logging
import os
import re
from typing import Any, Dict, Optional

from google import genai
from google.genai import types
from pydantic import BaseModel, Field

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
    SYSTEM_PROMPT = """
You are ZELTA, a calm and friendly financial guide for Nigerian university students.

Your ONLY job: help students make their money last on campus.

You speak like a smart older student — warm, direct, no jargon.

Students you help worry about:
- Will my money last till month end?
- Can I afford to eat today?
- My parents sent ₦15,000 — what do I do first?
- Am I spending too much on data?
- My rent is due soon — am I safe?

You ALWAYS:
- Speak plain everyday English
- Use real Naira amounts (₦)
- Tie advice to campus life (hostel, food, transport, data, fees, levies)
- Give ONE clear action the student can take today
- Be warm and calm, never scary

You NEVER:
- Say "invest" — say "set aside" or "keep safe"
- Use words like "Kelly Criterion", "Bayesian", "Monte Carlo", "allocation"
- Sound like a bank or lecturer
- Give more than one recommendation at a time
- Be vague
""".strip()

    JSON_SYSTEM_PROMPT = """
Return ONLY valid JSON. No markdown fences. No commentary. No truncation.
Use double quotes. Unknown fields use null. Keep all text student-friendly.
""".strip()

    def __init__(
        self,
        model: Optional[str] = None,
        *,
        project: Optional[str] = None,
        location: Optional[str] = None,
        api_key: Optional[str] = None,
        use_vertexai: Optional[bool] = None,
    ):
        project = project or os.getenv("GOOGLE_CLOUD_PROJECT")
        location = location or os.getenv("GOOGLE_CLOUD_LOCATION", "global")
        api_key = api_key or os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")

        if use_vertexai is None:
            env_flag = os.getenv("GOOGLE_GENAI_USE_VERTEXAI")
            if env_flag is not None:
                use_vertexai = env_flag.strip().lower() in {"1", "true", "yes", "on"}
            else:
                use_vertexai = bool(project)

        http_options = types.HttpOptions(api_version="v1")

        if use_vertexai:
            if not project:
                raise ValueError("GOOGLE_CLOUD_PROJECT not set for Vertex AI mode.")
            self.client = genai.Client(
                vertexai=True,
                project=project,
                location=location,
                http_options=http_options,
            )
        else:
            if not api_key:
                raise ValueError("GOOGLE_API_KEY or GEMINI_API_KEY not set for Gemini API mode.")
            self.client = genai.Client(
                api_key=api_key,
                http_options=http_options,
            )

        self.model = model or os.getenv("VERTEX_GEMINI_MODEL", "gemini-2.0-flash")

    # ── response schema ───────────────────────────────────────────

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
        }

    # ── pipeline prompt ───────────────────────────────────────────

    def _build_pipeline_prompt(self, data: Dict[str, Any]) -> str:
        student_model = data.get("student_model", {})
        bias = data.get("bias", {})
        bayse = data.get("bayse", {})
        stress = data.get("stress", {})
        kelly = data.get("allocation", {})

        agent_mode = student_model.get("agent_mode", "NORMAL")
        survival_score = student_model.get("survival_score", 50)
        free_cash = student_model.get("free_cash", kelly.get("hold_ngn", 0))
        weeks_of_runway = student_model.get("weeks_of_runway", 30)
        weeks_to_fee = student_model.get("weeks_to_fee_deadline", 999)
        fee_amount = student_model.get("fee_amount_due", 0)
        fee_gap = student_model.get("fee_gap_ngn", 0)
        weekly_burn = student_model.get("weekly_burn_rate", 0)
        safe_discretionary = student_model.get("safe_discretionary_ngn", 0)
        status_message = student_model.get("status_message", "")
        behavioral = student_model.get("behavioral", {})
        primary_directive = behavioral.get("primary_directive", "")

        raw_verdict = kelly.get("verdict", "HOLD")
        verdict_map = {
            "INVEST": "SPEND SAFELY",
            "SPEND_SAFELY": "SPEND SAFELY",
            "SAVE": "PROTECT YOUR MONEY",
            "PROTECT": "PROTECT YOUR MONEY",
            "HOLD": "HOLD — DON'T SPEND",
        }
        verdict = verdict_map.get(raw_verdict, raw_verdict)
        spend_safe = kelly.get("invest_ngn", kelly.get("spend_safely_ngn", 0))
        protect = kelly.get("save_ngn", kelly.get("protect_ngn", 0))

        bias_name = bias.get("active_bias", bias.get("bias", "Rational"))
        bias_explain = bias.get("explanation", "")
        student_tip = bias.get("student_tip", "")
        stress_score = stress.get("score", 50)
        market_title = bayse.get("market_title", "Nigerian financial market")

        urgency_block = ""
        if agent_mode == "EMERGENCY":
            urgency_block = (
                f"🚨 URGENT: Student is in EMERGENCY mode — money runs out in "
                f"{weeks_of_runway:.1f} weeks."
            )
        elif agent_mode == "SURVIVAL":
            urgency_block = f"⚠️ SURVIVAL: Student may miss fee payment. Gap: ₦{fee_gap:,.0f}."

        return f"""
You are ZELTA, talking to a Nigerian university student.
Explain their money situation in simple, warm, honest English.

{urgency_block}

THEIR SITUATION ({agent_mode} MODE — Score: {survival_score}/100):
Status: {status_message}
Directive: {primary_directive}

MONEY DETAILS:
- Free cash right now: ₦{free_cash:,.0f}
- Weekly spending pace: ₦{weekly_burn:,.0f}/week
- Money lasts: {weeks_of_runway:.1f} weeks at current pace
- Safe to spend this week: ₦{safe_discretionary:,.0f}
- Upcoming fee/rent due: ₦{fee_amount:,.0f} (in {weeks_to_fee:.0f} weeks)
- Fee shortfall: ₦{fee_gap:,.0f}

MARKET & BEHAVIOUR:
- Financial environment stress: {stress_score}/100
- Nigerian market: "{market_title}"
- Student's current money habit: {bias_name}
- Why: {bias_explain}
- Student tip: {student_tip}

ZELTA RECOMMENDATION: {verdict}
- Safe to spend: ₦{spend_safe:,.0f}
- Protect: ₦{protect:,.0f}

HOW TO RESPOND:
- The "action" must be ONE sentence a student can act on today using the Naira amounts above
- Tie everything to real campus life — hostel, food, data, transport, levies
- Never say "invest" — say "set aside" or "keep safe"
- If EMERGENCY or SURVIVAL, be honest but calm
- Keep summary under 2 sentences

RETURN ONLY VALID JSON. No markdown. No backticks.
""".strip()

    # ── question prompt ───────────────────────────────────────────

    def _build_question_prompt(self, question: str, context: Dict[str, Any]) -> str:
        student_model = context.get("student_model", {})
        kelly = context.get("allocation", context)
        stress = context.get("stress", {})
        bias = context.get("bias", {})

        free_cash = student_model.get("free_cash", float(context.get("free_cash", 0)))
        runway = student_model.get("weeks_of_runway", 30)
        weekly_burn = student_model.get("weekly_burn_rate", float(context.get("weekly_burn_rate", 0)))
        fee_due = student_model.get("fee_amount_due", float(context.get("upcoming_obligations", 0)))
        safe_spend = student_model.get("safe_discretionary_ngn", 0)
        agent_mode = student_model.get("agent_mode", "NORMAL")
        protect = kelly.get("save_ngn", kelly.get("protect_ngn", 0))
        stress_score = stress.get("score", context.get("stress_index", 50))
        bias_name = bias.get("active_bias", bias.get("bias", "Rational"))

        raw_verdict = kelly.get("verdict", "HOLD")
        verdict_map = {
            "INVEST": "SPEND SAFELY",
            "SPEND_SAFELY": "SPEND SAFELY",
            "SAVE": "PROTECT YOUR MONEY",
            "PROTECT": "PROTECT YOUR MONEY",
            "HOLD": "HOLD — DON'T SPEND",
        }
        verdict = verdict_map.get(raw_verdict, raw_verdict)

        return f"""
You are ZELTA, a money guide for Nigerian university students.
A student asked: "{question}"

Their situation ({agent_mode} mode):
- Free cash: ₦{free_cash:,.0f}
- Money lasts: {runway:.1f} weeks at current pace
- Weekly spending rate: ₦{weekly_burn:,.0f}/week
- Upcoming fee/rent: ₦{fee_due:,.0f}
- Safe to spend this week: ₦{safe_spend:,.0f}
- Protect: ₦{protect:,.0f}
- ZELTA says: {verdict}
- Market stress: {stress_score}/100
- Current habit: {bias_name}

Instructions:
- Answer the question directly and simply — plain text only, NO JSON
- Under 100 words
- Use the actual ₦ amounts above
- End with one clear action they can take today
""".strip()

    # ── Gemini helpers ────────────────────────────────────────────

    @staticmethod
    def _extract_text(response: Any) -> str:
        text = getattr(response, "text", None)
        if text:
            return str(text).strip()

        parsed = getattr(response, "parsed", None)
        if parsed is not None:
            try:
                if isinstance(parsed, BaseModel):
                    return json.dumps(parsed.model_dump(), ensure_ascii=False)
                return json.dumps(parsed, ensure_ascii=False)
            except Exception:
                pass

        try:
            return response.candidates[0].content.parts[0].text.strip()
        except Exception:
            return ""

    @staticmethod
    def _strip_fences(text: str) -> str:
        text = text.strip()
        if text.startswith("```"):
            text = re.sub(r"^```(?:json)?\s*", "", text, flags=re.IGNORECASE)
            text = re.sub(r"\s*```$", "", text)
        return text.strip()

    @staticmethod
    def _extract_first_json(text: str) -> str:
        text = ZeltaCopilot._strip_fences(text)
        start = text.find("{")
        if start == -1:
            return ""

        depth = 0
        in_str = False
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
                in_str = not in_str
                continue
            if in_str:
                continue

            if ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
                if depth == 0:
                    return text[start : i + 1]

        return ""

    @staticmethod
    def _parse_json(text: str) -> CopilotResult:
        json_text = ZeltaCopilot._extract_first_json(text)
        if not json_text:
            raise ValueError("No JSON object found.")
        return CopilotResult.model_validate(json.loads(json_text))

    @staticmethod
    def _fallback() -> Dict[str, Any]:
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

    async def _call_json(self, prompt: str) -> CopilotResult:
        config = types.GenerateContentConfig(
            system_instruction=f"{self.SYSTEM_PROMPT}\n\n{self.JSON_SYSTEM_PROMPT}",
            temperature=0.2,
            max_output_tokens=2048,
            response_mime_type="application/json",
            response_schema=CopilotResult,
        )

        response = await self.client.aio.models.generate_content(
            model=self.model,
            contents=prompt,
            config=config,
        )

        text = self._extract_text(response)
        if not text and getattr(response, "parsed", None) is not None:
            try:
                parsed = response.parsed
                return parsed if isinstance(parsed, CopilotResult) else CopilotResult.model_validate(parsed)
            except Exception:
                pass

        if not text:
            return CopilotResult(confidence_note="AI explanation temporarily unavailable.")

        try:
            return self._parse_json(text)
        except Exception as e:
            logger.warning("[Copilot] JSON parse failed, retrying: %s", e)
            repair_cfg = types.GenerateContentConfig(
                system_instruction=f"{self.SYSTEM_PROMPT}\n\n{self.JSON_SYSTEM_PROMPT}",
                temperature=0.0,
                response_mime_type="application/json",
                response_schema=CopilotResult,
            )
            try:
                r2 = await self.client.aio.models.generate_content(
                    model=self.model,
                    contents=f"Fix this into valid JSON only:\n{text}",
                    config=repair_cfg,
                )

                if getattr(r2, "parsed", None) is not None:
                    parsed = r2.parsed
                    return parsed if isinstance(parsed, CopilotResult) else CopilotResult.model_validate(parsed)

                return self._parse_json(self._extract_text(r2))
            except Exception:
                return CopilotResult(confidence_note="AI explanation temporarily unavailable.")

    async def _call_text(self, prompt: str) -> str:
        config = types.GenerateContentConfig(
            system_instruction=self.SYSTEM_PROMPT,
            temperature=0.3,
            max_output_tokens=400,
        )

        response = await self.client.aio.models.generate_content(
            model=self.model,
            contents=prompt,
            config=config,
        )

        raw = self._extract_text(response).strip()
        if raw.startswith("{"):
            try:
                data = json.loads(self._extract_first_json(raw))
                return data.get("answer", raw)
            except Exception:
                pass
        return raw

    async def aclose(self) -> None:
        """Close the async client cleanly."""
        try:
            await self.client.aio.aclose()
        except Exception:
            pass

    # ── public entry points ───────────────────────────────────────

    async def run(self, data: Dict[str, Any]) -> Dict[str, Any]:
        prompt = self._build_pipeline_prompt(data)
        try:
            result = await self._call_json(prompt)
            return result.model_dump(exclude_none=False)
        except Exception as e:
            logger.error("[Copilot] run() failed: %s", e)
            return self._fallback()

    async def answer_question(self, question: str, context: Dict[str, Any]) -> str:
        prompt = self._build_question_prompt(question, context)
        try:
            answer = await self._call_text(prompt)
            return answer or "Unable to answer right now. Check your dashboard."
        except Exception as e:
            logger.error("[Copilot] answer_question() failed: %s", e)
            return "Unable to answer right now. Check your dashboard."


# Optional simple helper for direct use
async def run_copilot(data: Dict[str, Any]) -> Dict[str, Any]:
    copilot = ZeltaCopilot()
    try:
        return await copilot.run(data)
    finally:
        await copilot.aclose()


async def answer_copilot_question(question: str, context: Dict[str, Any]) -> str:
    copilot = ZeltaCopilot()
    try:
        return await copilot.answer_question(question, context)
    finally:
        await copilot.aclose()