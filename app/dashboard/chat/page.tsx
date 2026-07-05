
"use client";

import React, { useEffect, useRef, useState } from "react";
import {
  Send,
  Sparkles,
  GraduationCap,
  User,
  Plus,
} from "lucide-react";

interface Message {
  id: string;
  sender: "user" | "assistant";
  text: string;
  timestamp: string;
  metadata?: {
    mode?: "NORMAL" | "SURVIVAL" | "EMERGENCY";
    bias?: string;
    impact?: string;
  };
}

export default function ZeltaCopilotChat() {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: "init",
      sender: "assistant",
      text: `You currently have ₦26,500 left for the month. Since your exams are 14 days away, I’ll help you avoid unnecessary spending and protect your financial runway.`,
      timestamp: "12:00 PM",
      metadata: {
        mode: "NORMAL",
        bias: "None detected",
        impact: "Stable runway",
      },
    },
  ]);

  const [inputMessage, setInputMessage] = useState("");
  const [isThinking, setIsThinking] = useState(false);

  const chatEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({
      behavior: "smooth",
    });
  }, [messages, isThinking]);

  const simulateAIResponse = async (prompt: string) => {
    setIsThinking(true);

    await new Promise((resolve) =>
      setTimeout(resolve, 1800)
    );

    let response =
      "That looks financially safe for now.";
    let mode: "NORMAL" | "SURVIVAL" | "EMERGENCY" =
      "NORMAL";
    let bias = "None detected";
    let impact = "Minimal impact";

    const lower = prompt.toLowerCase();

    if (
      lower.includes("shoe") ||
      lower.includes("sneaker") ||
      lower.includes("buy") ||
      lower.includes("spend")
    ) {
      response =
        "Spending ₦15,000 right now could reduce your remaining runway by more than 50%. Since your exams are close, I’d recommend delaying non-essential purchases for now.";

      mode = "SURVIVAL";
      bias = "Impulse spending";
      impact = "-56% runway";
    }

    if (
      lower.includes("book") ||
      lower.includes("exam") ||
      lower.includes("handout")
    ) {
      response =
        "Academic purchases are considered high-priority right now. This spending fits safely within your current financial plan.";

      mode = "NORMAL";
      bias = "Necessary spending";
      impact = "Safe allocation";
    }

    setMessages((prev) => [
      ...prev,
      {
        id: Date.now().toString(),
        sender: "assistant",
        text: response,
        timestamp: new Date().toLocaleTimeString([], {
          hour: "2-digit",
          minute: "2-digit",
        }),
        metadata: {
          mode,
          bias,
          impact,
        },
      },
    ]);

    setIsThinking(false);
  };

  const handleSend = (
    e: React.FormEvent<HTMLFormElement>
  ) => {
    e.preventDefault();

    if (!inputMessage.trim() || isThinking) return;

    const userMessage = inputMessage;

    setMessages((prev) => [
      ...prev,
      {
        id: Date.now().toString(),
        sender: "user",
        text: userMessage,
        timestamp: new Date().toLocaleTimeString([], {
          hour: "2-digit",
          minute: "2-digit",
        }),
      },
    ]);

    setInputMessage("");

    simulateAIResponse(userMessage);
  };

  return (
    <div className="max-h-[200px] text-white  relative p-2 md:p-6 w-full">

      <div className=" h-[80vh] shadow-black/40 overflow-hidden flex flex-col">

        {/* Messages */}
        <div className="flex-1 md:px-6 px-2 py-6 space-y-4 pb-40 overflow-y-auto scrollbar-none">
          {messages.map((msg) => (
            <div
              key={msg.id}
              className={`flex gap-3 ${
                msg.sender === "user"
                  ? "justify-end"
                  : "justify-start"
              }`}
            >
              {msg.sender === "assistant" && (
                <div className="h-9 w-9 rounded-xl bg-[#8c52f1]/10 border border-[#8c52f1]/20  items-center justify-center shrink-0 md:flex hidden">
                  <Sparkles className="h-4 w-4 text-[#8c52f1]" />
                </div>
              )}

              <div className="md:max-w-[55%] max-w-[80%]">
                <div
                  className={`rounded-2xl px-4 py-4 text-[13px] leading-relaxed font-extralight ${
                    msg.sender === "assistant"
                      ? "bg-neutral-800/30 dark:bg-neutral-300/30 dark:text-foreground/90  text-neutral-200 rounded-tl-sm"
                      : "bg-[#8c52f1]/10 dark:bg-[#8c52f1] text-neutral-200 rounded-tr-sm"
                  }`}
                >
                  {msg.text}
                </div>

                {msg.metadata &&
                  msg.sender === "assistant" && (
                    <div className="flex flex-wrap gap-2 mt-3 md:text-sm text-xs">
                      <div className="px-2 py-1 rounded-full bg-emerald-500/10 text-green-500 ">
                        {msg.metadata.mode}
                      </div>

                      <div className="px-2 py-1 rounded-full bg-amber-500/10 text-amber-300 dark:text-amber-500 ">
                        {msg.metadata.bias}
                      </div>

                      <div className="px-2 py-1 rounded-full bg-red-500/10 text-red-400 dark:text-red-500 ">
                        {msg.metadata.impact}
                      </div>
                    </div>
                  )}

                <span className="text-[10px] text-neutral-300 dark:text-black mt-2 block">
                  {msg.timestamp}
                </span>
              </div>

              {msg.sender === "user" && (
                <div className="h-9 w-9 rounded-xl bg-white/5 dark:bg-[#8c52f1]/10 border border-white/5 md:flex hidden items-center justify-center shrink-0">
                  <User className="h-4 w-4 text-neutral-300 dark:text-foreground/80" />
                </div>
              )}
            </div>
          ))}

          {/* Thinking State */}
          {isThinking && (
            <div className="flex items-center gap-3">
              <div className="h-9 w-9 rounded-xl bg-[#8c52f1]/10 border border-[#8c52f1]/20 flex items-center justify-center">
                <Sparkles className="h-4 w-4 text-[#8c52f1] animate-pulse" />
              </div>

              <div className=" px-4 py-4">
                <div className="flex gap-1">
                  <span className="h-2 w-2 rounded-full bg-[#8c52f1] animate-bounce" />
                  <span className="h-2 w-2 rounded-full bg-[#8c52f1] animate-bounce delay-100" />
                  <span className="h-2 w-2 rounded-full bg-[#8c52f1] animate-bounce delay-200" />
                </div>
              </div>
            </div>
          )}

          <div ref={chatEndRef} />
        </div>

        <form
       onSubmit={handleSend}
           className="fixed bottom-5 lg:left-[250px] left-0 right-0 z-50 px-4 pb-4 md:px-8"
   >
  <div className="max-w-4xl mx-auto">
    <div className="flex items-center gap-3 rounded-full bg-neutral-900 dark:bg-[#8c52f1]/90 backdrop-blur-lg px-6 py-3 shadow-xs">
    <div className="font-bold cursor-pointer"><Plus size={18}/></div>
      <input
        type="text"
        value={inputMessage}
        onChange={(e) =>
          setInputMessage(e.target.value)
        }
        placeholder="Ask Zelta anything..."
        disabled={isThinking}
        className="flex-1 bg-transparent outline-none text-sm text-white placeholder:text-white font-semi-bold"
      />

      <button
        type="submit"
        disabled={
          !inputMessage.trim() || isThinking
        }
        className="h-10 w-10 rounded-xl bg-[#d98825]  text-white flex items-center justify-center hover:scale-105 transition-all disabled:opacity-70 cursor-pointer"
      >
        <Send className="h-4 w-4" />
      </button>
    </div>
  </div>
</form>
      </div>
    </div>
  );
}

