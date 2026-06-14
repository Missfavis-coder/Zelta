"use client";

import { useState } from "react";
import {
  AlertTriangle,
  Wallet,
  Calendar,
  TrendingDown,
  Sparkles,
  X,
  ScanEye,
} from "lucide-react";

type SimulationResult = {
    riskLevel: "LOW" | "MEDIUM" | "HIGH";
    remainingBalance: number;
    runwayBefore: number;
    runwayAfter: number;
    daysLost: number;
    recommendation: string;
  };
export default function WhatIfPage() {
  const [query, setQuery] = useState("");
  const [loading, setLoading] = useState(false);
  const [showDialog, setShowDialog] = useState(false);
const [activeTab, setActiveTab] = useState<
  "overview" | "insights" | "alternatives"
>("overview");

  const [result, setResult] = useState<SimulationResult | null>(null);

  const handleSimulation = async () => {
    if (!query.trim()) return;

    setLoading(true);

    try {
      const response = await fetch("/api/simulation", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          query,
        }),
      });

      const data = await response.json();

      setResult(data);
    } catch (error) {
      console.error(error);
      setShowDialog(true)
      // Demo data
      setResult({
        riskLevel: "HIGH",
        remainingBalance: 60000,
        runwayBefore: 23,
        runwayAfter: 15,
        daysLost: 8,
        recommendation:
          "Delay this purchase until your next allowance.",
      });
    }

    setLoading(false);
  };

  const riskColor =
    result?.riskLevel === "HIGH"
      ? "bg-red-600"
      : result?.riskLevel === "MEDIUM"
      ? "bg-yellow-500"
      : "bg-green-500";

  return (
    <div className="min-h-screen text-white md:p-6 p-4">
      <div className="">

        {/* Overview Cards */}

        <div className="grid md:grid-cols-2 gap-4 mb-8">
          <div className=" rounded-2xl p-5  bg-neutral-800/30">
            <div className="flex items-center gap-3">
              <Calendar size={18} className="text-purple-500" />
              <span className="text-neutral-500 md:text-[14px] text-sm font-semibold uppercase">
                Current Runway
              </span>
            </div>

            <h2 className="md:text-xl text-[16px] font-bold mt-3">
              23 Days
            </h2>
          </div>

          <div className="rounded-2xl p-5  bg-neutral-800/30">
            <div className="flex items-center gap-3">
              <Wallet size={18} className="text-purple-500" />
              <span className="text-neutral-500 md:text-[14px] text-sm font-semibold uppercase">
                Current Balance
              </span>
            </div>

            <h2 className="md:text-xl text-[16px] font-bold mt-3">
              ₦85,000
            </h2>
          </div>
        </div>

        {/* Input Area */}

        <div className="bg-neutral-800/30 rounded-2xl md:p-6 p-5">
          <h3 className="text-xl font-semibold mb-3">
            What are you thinking of doing?
          </h3>

          <p className="text-neutral-300 text-sm mb-4">
            Example:
            <br />
            • Buy a ₦25,000 sneaker
            <br />
            • Travel home this weekend
            <br />
            • Spend ₦15,000 on a birthday
          </p>

          <textarea
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            rows={4}
            placeholder="What if I buy a ₦25,000 sneaker this week?"
            className="w-full rounded-xl border border-neutral-900 p-4 outline-none focus:border-amber-500 text-sm"
          />

          <div className="text-sm text-amber-400/40">Ensure to enter the amount of whatever purchase you want to make</div>

          <button
            onClick={handleSimulation}
            disabled={loading}
            className="mt-4 bg-[#8c52f1] hover:bg-purple-700 px-6 py-3 rounded-xl font-semibold transition text-sm cursor-pointer"
          >
            {loading
              ? "Running Simulation..."
              : "Run Simulation"}
          </button>
        </div>


        {/* Results */}
        {showDialog && result && (
  <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40 backdrop-blur-sm p-4">
    <div className="w-full max-w-3xl rounded-3xl bg-neutral-900  overflow-hidden">

      {/* Header */}

      <div className="flex items-center justify-between p-5 ">
        <div>
          <h2 className="font-bold text-[18px] uppercase ">
            Simulation Result
          </h2>

          <div
            className={`${riskColor} inline-flex items-center gap-2 px-3 py-1 rounded-full text-xs font-semibold mt-2`}
          >
            <AlertTriangle size={14} />
            {result.riskLevel} RISK
          </div>
        </div>

        <button
          onClick={() => setShowDialog(false)}
          className="text-neutral-400 hover:text-white text-xl cursor-pointer"
        >
          <X/>
        </button>
      </div>

      {/* Tabs */}

      <div className="flex border-b border-neutral-800 ">
        <button
          onClick={() => setActiveTab("overview")}
          className={`px-5 py-3 text-sm font-medium cursor-pointer ${
            activeTab === "overview"
              ? "text-white border-b-2 border-[#8c52f1]"
              : "text-neutral-400"
          }`}
        >
          Overview
        </button>

        <button
          onClick={() => setActiveTab("insights")}
          className={`px-5 py-3 text-sm font-medium cursor-pointer ${
            activeTab === "insights"
              ? "text-white border-b-2 border-[#8c52f1]"
              : "text-neutral-400"
          }`}
        >
          Insights
        </button>

        <button
          onClick={() => setActiveTab("alternatives")}
          className={`px-5 py-3 text-sm font-medium cursor-pointer ${
            activeTab === "alternatives"
              ? "text-white border-b-2 border-[#8c52f1]"
              : "text-neutral-400"
          }`}
        >
          Alternatives
        </button>
      </div>

      {/* Content */}
      <div className="py-4">
      <div className="p-4 max-h-[70vh] overflow-y-auto">

{activeTab === "overview" && (
  <div className="space-y-5">

    <div className="grid md:grid-cols-2 gap-4">

      <div className="bg-neutral-800/30 rounded-2xl p-5">
        <p className="text-neutral-400 text-sm uppercase">
          Remaining Balance
        </p>

        <h3 className="text-xl font-bold mt-2">
          ₦{result.remainingBalance.toLocaleString()}
        </h3>
      </div>

      <div className="bg-neutral-800/30 rounded-2xl p-5">
        <p className="text-neutral-400 text-sm uppercase">
          Days Lost
        </p>

        <h3 className="text-xl font-bold mt-2 text-red-400">
          {result.daysLost}
        </h3>
      </div>

      <div className="bg-neutral-800/30 rounded-2xl p-5">
        <p className="text-neutral-400 text-sm uppercase">
          Runway Before
        </p>

        <h3 className="text-xl font-bold mt-2">
          {result.runwayBefore} Days
        </h3>
      </div>

      <div className="bg-neutral-800/30 rounded-2xl p-5">
        <p className="text-neutral-400 text-sm uppercase">
          Runway After
        </p>

        <h3 className="text-xl font-bold mt-2">
          {result.runwayAfter} Days
        </h3>
      </div>

    </div>

    <div className="space-y-4">

      <div>
        <p className="mb-2 text-sm text-neutral-400">
          Before Purchase
        </p>

        <div className="w-full h-3 bg-neutral-800 rounded-full">
          <div className="w-full h-3 bg-[#8c52f1] rounded-full"></div>
        </div>
      </div>

      <div>
        <p className="mb-2 text-sm text-neutral-400">
          After Purchase
        </p>

        <div className="w-full h-3 bg-neutral-800 rounded-full">
          <div
            className="h-3 bg-red-600 rounded-full"
            style={{
              width: `${
                (result.runwayAfter /
                  result.runwayBefore) *
                100
              }%`,
            }}
          />
        </div>
      </div>

    </div>

  </div>
)}

{activeTab === "insights" && (
  <div className="bg-neutral-800/30 rounded-2xl p-5">
    <div className="flex items-center gap-2 mb-4">
      <Sparkles size={18} fill="#8c52f1" className="text-[#8c52f1]" />
      <h3 className="font-semibold">
        The best decision at the moment.
      </h3>
    </div>

    <p className="leading-relaxed text-sm text-neutral-300">
      {result.recommendation}
    </p>
  </div>
)}

{activeTab === "alternatives" && (
  <div className="bg-neutral-800/40 rounded-2xl p-5">
    <div className="flex items-center gap-2 mb-4">
      <ScanEye size={18} fill="" className=" text-[#8c52f1] " />
      <h3 className="font-semibold">
        Better Alternatives
      </h3>
    </div>

    <ul className="space-y-4 text-neutral-300 text-sm">
      <li>✓ Delay purchase until next allowance</li>
      <li>✓ Save weekly towards the goal</li>
      <li>✓ Find a lower-cost alternative</li>
      <li>✓ Take a campus gig to offset the cost</li>
    </ul>
  </div>
)}

</div>

      </div>


    </div>
  </div>
)}

      </div>
    </div>
  );
}