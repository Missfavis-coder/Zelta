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
  CircleQuestionMark,
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
  const [showHowItWorks, setShowHowItWorks] = useState(false);
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
      ? "bg-red-500 "
      : result?.riskLevel === "MEDIUM"
      ? "bg-yellow-500"
      : "bg-green-500";

  return (
    <div className="min-h-screen text-white md:p-6 p-4">
      <div className="">

        {/* Overview Cards */}

        <div className="s mb-8">

          <div className="rounded-md p-5 bg-neutral-800/20 dark:bg-neutral-200/30 ">
            <div className="flex items-center gap-3">
              <Wallet size={18} className="text-foreground" />
              <span className="text-neutral-500 dark:text-foreground/90 md:text-[14px] md:text-sm text-xs font-semibold uppercase tracking-wide">
                 Balance
              </span>
            </div>

            <h2 className="md:text-xl text-[16px] dark:text-foreground font-bold mt-3">
              ₦85,000
            </h2>
          </div>
        </div>

        {/* Input Area */}

        <div >
          <div className="flex items-center justify-between">
          <h3 className=" text-sm dark:text-[#160a2a] font-light mb-3">
            What are you thinking of doing?
          </h3>

          <div 
          onClick={()=>{setShowHowItWorks(true)}}
          className="flex items-center gap-1 text-neutral-300 dark:text-foreground/80 dark:hover:text-foreground text-xs mb-4 cursor-pointer">
            <CircleQuestionMark size={12}/>
             <p>How it works</p>
          </div>
          </div>
{showHowItWorks && (
  <div className="fixed inset-0 z-50 flex items-center justify-center bg-neutral-800/20  dark:bg-white/40  p-4 ">
    <div className="w-full md:max-w-[40%] max-w-[80%]  rounded-md bg-neutral-900 dark:bg-background overflow-hidden shadow-2xl p-4">
      <div className="dark:text-black text-sm flex items-center justify-between">
      <h1>How Simulations Work</h1>
      <div className="cursor-pointer"> <X/> </div>
      </div>

    </div>
  </div>
)}
<div  >    
<textarea
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            rows={4}
            placeholder="What if I buy a ₦25,000 sneaker this week?"
            className="w-full rounded-xl border border-neutral-900 dark:border-foreground/20 p-4 outline-none dark:focus:border-amber-500 focus:border-amber-500 dark:text-foreground text-sm"
          />

          <div className="text-sm text-amber-400 dark:text-amber-500 font-extralight">Ensure to enter the amount of whatever purchase you want to make</div>

          <button
            onClick={handleSimulation}
            disabled={loading}
            className="mt-4 bg-[#8c52f1] hover:bg-purple-600 px-6 py-3 rounded-xl font-semibold transition text-sm cursor-pointer"
          >
            {loading
              ? "Running Simulation..."
              : "Run Simulation"}
          </button>
</div>

        </div>


        {/* Results */}
        {showDialog && result && (
  <div  className="fixed inset-0 z-50 flex items-center justify-center bg-neutral-800/20  dark:bg-neutral-300/10 backdrop-blur-sm p-4 ">
    <div className="w-full max-w-2xl  rounded-md bg-neutral-900 dark:bg-background overflow-hidden shadow-md">

      {/* Header */}

      <div className="flex items-center justify-between p-4 ">
        <div>
          <h2 className="font-semibold tracking-wide text-sm uppercase dark:text-[#160a2a]/90 ">
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
          className="text-neutral-400 dark:text-[#160a2a]/90 hover:text-white text-xl cursor-pointer"
        >
          <X size={18}/>
        </button>
      </div>

      {/* Tabs */}

      <div className="flex border-b border-neutral-800 dark:border-foreground/20 ">
        <button
          onClick={() => setActiveTab("overview")}
          className={`px-5 py-3 text-sm font-medium cursor-pointer ${
            activeTab === "overview"
              ? "text-white dark:text-foreground border-b-2 border-[#8c52f1]"
              : "text-neutral-400 dark:text-foreground/70"
          }`}
        >
          Overview
        </button>

        <button
          onClick={() => setActiveTab("insights")}
          className={`px-5 py-3 text-sm font-medium cursor-pointer ${
            activeTab === "insights"
              ? "text-white border-b-2 dark:text-foreground border-[#8c52f1]"
              : "text-neutral-400 dark:text-foreground/70"
          }`}
        >
          Insights
        </button>

        <button
          onClick={() => setActiveTab("alternatives")}
          className={`px-5 py-3 text-sm font-medium cursor-pointer ${
            activeTab === "alternatives"
              ? "text-white border-b-2 dark:text-foreground border-[#8c52f1]"
              : "text-neutral-400 dark:text-foreground/70"
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

      <div className="bg-neutral-800/30 dark:bg-neutral-300/20 rounded-xl p-4">
        <p className="text-neutral-400 dark:text-foreground/80 text-xs uppercase">
          Remaining Balance
        </p>

        <h3 className="md:text-xl text-[16px] dark:text-foreground font-bold mt-2">
          ₦{result.remainingBalance.toLocaleString()}
        </h3>
      </div>

      <div className="bg-neutral-800/30 dark:bg-neutral-300/20 rounded-xl p-4">
        <p className="text-neutral-400 dark:text-foreground/80 uppercase text-xs ">
          Days Lost
        </p>

        <h3 className="md:text-xl text-[16px] dark:text-foreground font-bold mt-2 text-white">
          {result.daysLost}
        </h3>
      </div>

      <div className="bg-neutral-800/30 dark:bg-neutral-300/20 rounded-xl p-4">
        <p className="text-neutral-400 text-xs dark:text-foreground/80 uppercase">
          Runway Before
        </p>

        <h3 className="md:text-xl text-[16px] dark:text-foreground font-bold mt-2">
          {result.runwayBefore} Days
        </h3>
      </div>

      <div className="bg-neutral-800/30 dark:bg-neutral-300/20 rounded-xl p-4">
        <p className="text-neutral-400 text-xs dark:text-foreground/80 uppercase">
          Runway After
        </p>

        <h3 className="md:text-xl text-[16px] font-bold dark:text-foreground mt-2">
          {result.runwayAfter} Days
        </h3>
      </div>

    </div>

  </div>
)}

{activeTab === "insights" && (
  <div className="bg-neutral-800/30 dark:bg-neutral-300/20 rounded-2xl p-5">
    <div className="flex items-center gap-2 mb-4">
      <Sparkles size={18} fill="#8c52f1" className="text-[#8c52f1]" />
      <h3 className="font-semibold dark:text-foreground">
        The best decision at the moment.
      </h3>
    </div>

    <p className="leading-relaxed text-sm text-neutral-300 dark:text-foreground/70">
      {result.recommendation}
    </p>
  </div>
)}

{activeTab === "alternatives" && (
  <div className="bg-neutral-800/40 dark:bg-neutral-300/20 rounded-2xl p-5">
    <div className="flex items-center gap-2 mb-4">
      <ScanEye size={18}  className=" text-[#8c52f1] " />
      <h3 className="font-semibold  dark:text-foreground">
        Better Alternatives
      </h3>
    </div>

    <ul className="space-y-4 text-neutral-300 dark:text-foreground/70 text-sm">
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