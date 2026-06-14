import {
    ShieldCheck,
    TrendingUp,
    Wallet,
    Zap,
  } from "lucide-react";
import { Button } from "../ui/button";
import Link from "next/link";
  
  export function DashboardMetrics({
    financialStatus,
    logs
  }: {
    financialStatus: {
      availableBalance: string;
      safeLockedBalance: string;
      sapaRisk: string;
    };
    logs: {
      id: number;
      message: string;
      time: string;
      saved: boolean;
    }[];
  }) {
    return (
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
  
        <div className="rounded-3xl  bg-[#0b0b0b] p-6">
          <div className="flex items-center justify-between text-neutral-500 lg:text-sm text-xs font-semibold tracking-wide">
            <span>AVAILABLE BALANCE</span>
            <Wallet size={16} />
          </div>
  
          <h2 className="lg:text-2xl text-xl font-bold mt-4 tracking-tight">
            {financialStatus.availableBalance}
          </h2>

          <div className="flex justify-between gap-2 w-full mt-6">
            <Button className="w-1/2 py-5.5 bg-[#d98825] font-bold cursor-pointer">Fund</Button>
            <Button className="w-1/2 py-5.5 bg-[#8c52f1]/20 font-bold cursor-pointer text-[#8c52f1]">Withdraw</Button>
          </div>

          <div className="mt-4">
            <Link href="/dashboard/chat" className="text-sm text-neutral-400 hover:text-neutral-500 ">Talk to Zelta AI before sending money on impulse</Link>
          </div>
  
        </div>
  
        <div className="rounded-3xl bg-[#0b0b0b] p-6">
  
  <div className="mb-6">
    <span className="text-neutral-500 lg:text-sm text-xs font-semibold uppercase">
      AI Activity
    </span>

    <p className="text-sm text-neutral-200 mt-1">
      Real-time financial protection and opportunities.
    </p>
  </div>

  <div className="divide-y divide-neutral-900">
    {logs.map((log) => (
      <div
        key={log.id}
        className="py-4 flex items-start gap-4 first:pt-0 last:pb-0"
      >

        <div
          className={`p-2 rounded-xl ${
            log.saved
              ? "bg-[#8c52f1]/10 text-[#8c52f1]"
              : "bg-amber-500/10 text-amber-400"
          }`}
        >
          {log.saved ? (
            <ShieldCheck size={16} />
          ) : (
            <Zap size={16} />
          )}
        </div>

        <div className="flex-1">
          <p className="text-sm text-neutral-200">
            {log.message}
          </p>

          <span className="text-xs text-neutral-500 mt-1 block">
            {log.time}
          </span>
        </div>

      </div>
    ))}
  </div>

</div>
  
      </div>
    );
  }