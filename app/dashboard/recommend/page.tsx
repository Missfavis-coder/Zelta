"use client";

import { useState } from "react";
import { Sparkles, Loader2 } from "lucide-react";

type Recommendation = {
  rank: number;
  item_name: string;
  domain: string;
  category?: string;
  avg_rating: number;
  reason: string;
  survival_score: number;
};

export default function RecommendPage() {
  const [need, setNeed] = useState("");
  const [loading, setLoading] = useState(false);
  const [data, setData] = useState<Recommendation[]>([]);

  const persona = {
    student_level: "300L",
    field_of_study: "Computer Science",
    weekly_budget_ngn: 8000,
    urgency: "survival",
    location: "Lagos",
  };

  async function handleRecommend() {
    if (!need.trim()) return;

    setLoading(true);

    try {
      const res = await fetch("http://localhost:8000/recommend", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          persona,
          need,
          domains: ["amazon", "goodreads"],
        }),
      });

      const json = await res.json();
      setData(json.recommendations || []);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="p-6 md:p-10 space-y-8  min-h-screen">

      {/* HEADER */}
      <div>
        <h1 className="text-2xl font-bold text-[#142971]">
          Recommendations
        </h1>
        <p className="text-sm text-gray-500">
          AI-ranked survival essentials based on your student profile
        </p>
      </div>

      {/* NEED INPUT */}
      <div className="bg-white p-5 rounded-xl border shadow-sm">
        <p className="text-sm text-gray-500 mb-2">
          What do you need?
        </p>

        <div className="flex gap-2">
          <input
            value={need}
            onChange={(e) => setNeed(e.target.value)}
            placeholder="e.g. cheap study materials for exams"
            className="flex-1 px-4 py-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-[#142971]"
          />

          <button
            onClick={handleRecommend}
            className="bg-[#142971] text-white px-4 py-3 rounded-lg flex items-center gap-2 hover:opacity-90"
          >
            {loading ? (
              <Loader2 className="w-4 h-4 animate-spin" />
            ) : (
              <Sparkles className="w-4 h-4" />
            )}
            {loading ? "Thinking..." : "Recommend"}
          </button>
        </div>
      </div>

      {/* PERSONA CARD */}
      <div className="bg-white p-5 rounded-xl border shadow-sm">
        <p className="text-sm text-gray-500">Active Student Context</p>
        <h2 className="font-semibold text-[#142971] mt-1">
          {persona.student_level} • {persona.field_of_study}
        </h2>
        <p className="text-sm text-gray-600 mt-1">
          ₦{persona.weekly_budget_ngn}/week • {persona.location}
        </p>
      </div>

      {/* RESULTS */}
      <div className="space-y-4">
        {data.length > 0 && (
          <h2 className="text-lg font-semibold text-[#142971]">
            Ranked Results
          </h2>
        )}

        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">

          {data.map((item) => (
            <div
              key={item.rank}
              className="bg-white p-4 rounded-xl border shadow-sm"
            >
              {/* RANK */}
              <p className="text-xs font-semibold text-green-600">
                Rank #{item.rank}
              </p>

              {/* TITLE */}
              <h3 className="font-semibold mt-1 text-[#142971]">
                {item.item_name}
              </h3>

              {/* META */}
              <p className="text-xs text-gray-500 mt-1">
                {item.domain} • ⭐ {item.avg_rating}
              </p>

              {/* SCORE */}
              <div className="mt-3">
                <div className="flex justify-between text-xs">
                  <span>Survival Score</span>
                  <span>{item.survival_score.toFixed(2)}</span>
                </div>

                <div className="w-full bg-gray-100 h-2 rounded-full mt-1">
                  <div
                    className="bg-[#142971] h-2 rounded-full"
                    style={{
                      width: `${item.survival_score * 100}%`,
                    }}
                  />
                </div>
              </div>

              {/* REASON */}
              <p className="text-xs text-gray-600 mt-3">
                {item.reason}
              </p>
            </div>
          ))}
        </div>
      </div>

    </div>
  );
}