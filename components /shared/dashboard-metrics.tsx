import {
  FileUser,
    ShieldCheck,
    TrendingUp,
    Upload,
    Wallet,
    Zap,
  } from "lucide-react";
import { Button } from "../ui/button";
import Link from "next/link";
  
  export function DashboardMetrics({
    financialStatus,
  }: {
    financialStatus: {
      availableBalance: string;
      safeLockedBalance: string;
      sapaRisk: string;
    };
  }) {
    return (
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
  
        <div className="rounded-md border-2 dark:border-none border-neutral-900 dark:border-foreground/10 bg-[#0b0b0b] dark:bg-neutral-200/30 p-6">
          <div className="flex items-center justify-between text-neutral-500 dark:text-foreground/90 lg:text-sm text-xs font-semibold tracking-wide">
            <span>AVAILABLE BALANCE</span>
            <Wallet size={16} />
          </div>
  
          <h2 className="lg:text-2xl text-xl font-bold mt-4 tracking-tight dark:text-foreground">
            {financialStatus.availableBalance}
          </h2>

          <div className="flex justify-between gap-2 w-full mt-6">
            <Button className="w-1/2 py-5.5 bg-[#d98825] font-bold cursor-pointer text-white">Fund</Button>
            <Button className="w-1/2 py-5.5 bg-[#8c52f1]/20 font-bold cursor-pointer text-[#8c52f1]">Withdraw</Button>
          </div>

          <div className="mt-4">
            <Link href="/dashboard/chat" className="text-sm text-neutral-500 dark:text-foreground hover:text-neutral-500 ">Talk to Zelta AI before sending money on impulse</Link>
          </div>
  
        </div>
  
        <div className="rounded-md border-2 dark:border-none border-neutral-900 bg-[#0b0b0b] dark:bg-neutral-200/30 dark:border-foreground/10 p-5">

        <div className="mb-6">
          <span className="text-neutral-500 dark:text-foreground/90 lg:text-sm text-xs font-semibold uppercase tracking-wide">
            Upload Details
          </span>

         <p className="text-sm text-neutral-400 dark:text-foreground/90 mt-1">
           All files to be uploaded must be in CSV format
         </p>
        </div>

        <div className="flex items-center justify-center min-h-30 border rounded-md border-dashed border-neutral-800 dark:border-neutral-300 dark:text-foreground/80">
<FileUser/>
        </div>

        </div>
  
      </div>
    );
  }