"use client";

import {
  Card,
  CardHeader,
  CardTitle,
  CardDescription,
} from "@/components/ui/card";
import { TooltipProvider } from "@/components/ui/tooltip";
import { Landmark, ArrowDownLeft, ArrowUpRight } from "lucide-react";
import { formatToKobo } from "@/lib/utils";
import { cn } from "@/lib/utils";

import { useWalletBalance } from "@/lib/hooks/use-dashboard";

function StatCardSkeleton() {  return (
    <Card className="relative overflow-hidden rounded-xl border  border-neutral-700 bg-neutral-900 backdrop-blur-md">
      <CardHeader className="p-4">
        <div className="flex justify-between items-start">
          <div className="h-3 w-24 bg-neutral-800 rounded animate-pulse" />
          <div className="h-8 w-8 bg-neutral-800 rounded-lg animate-pulse" />
        </div>

        <div className="mt-3 h-6 w-32 bg-neutral-800 rounded animate-pulse" />

        <div className="mt-3 space-y-2">
          <div className="h-2 w-full bg-neutral-800 rounded animate-pulse" />
        </div>
      </CardHeader>
    </Card>
  );
}

export function StatsCards() {
  const { data, isLoading } = useWalletBalance();

  const wallet = data?.data?.wallet;

  const availableBalance = Number(wallet?.balance ?? 0);

  const incomingFunds = 0;
  const totalSpent = 0;

  return (
    <TooltipProvider>
      <div className="grid grid-cols-1 gap-6 lg:grid-cols-3 px-2">
        {isLoading ? (
          <StatCardSkeleton />
        ) : (
          <StatCard
            title="Available Balance"
            value={formatToKobo(availableBalance)}
            description="Spendable wallet balance across all payment modes"
            type="cash"
          />
        )}

        {/* INCOMING */}
        {isLoading ? (
          <StatCardSkeleton />
        ) : (
          <StatCard
            title="Incoming Transfers"
            value={formatToKobo(incomingFunds)}
            description="Pending and processing payments"
            type="incoming"
          />
        )}

        {/* SPENT */}
        {isLoading ? (
          <StatCardSkeleton />
        ) : (
          <StatCard
            title="Today’s Spending"
            value={formatToKobo(totalSpent)}
            description="Real-time outflow across all transactions"
            type="outflow"
          />
        )}
      </div>
    </TooltipProvider>
  );
}

function StatCard({
  title,
  value,
  description,
  type,
}: {
  title: string;
  value: string;
  description: string;
  type: "cash" | "incoming" | "outflow";
}) {
  const config = {
    cash: {
      icon: Landmark,
      text: "text-cyan-400",
      glow: "from-cyan-500/15",
    },
    incoming: {
      icon: ArrowDownLeft,
      text: "text-green-400",
      glow: "from-green-500/15",
    },
    outflow: {
      icon: ArrowUpRight,
      text: "text-rose-400",
      glow: "from-rose-500/15",
    },
  }[type];

  const Icon = config.icon;

  return (
    <Card
      className={cn(
        "relative overflow-hidden rounded-xl border backdrop-blur-md",
        "border-white/10 bg-black/40 text-white",
        "transition-all duration-200 hover:-translate-y-1 hover:shadow-2xl group",
      )}
    >
      <div
        className={cn(
          "absolute inset-0 opacity-0 group-hover:opacity-100 transition",
          `bg-gradient-to-br ${config.glow} via-transparent to-transparent`,
        )}
      />

      <CardHeader className="p-4 relative z-10">
        <div className="flex justify-between items-start">
          <CardDescription className="text-[11px] uppercase tracking-widest text-neutral-300 font-semibold">
            {title}
          </CardDescription>

          <div className={cn("p-2 rounded-lg bg-white/5", config.text)}>
            <Icon size={18} />
          </div>
        </div>

        <CardTitle className="text-2xl font-bold tracking-tight">
          {value}
        </CardTitle>

        <p className="text-[11px] text-neutral-500 mt-2">{description}</p>
      </CardHeader>

      <div
        className={cn(
          "absolute -right-10 -bottom-10 opacity-[0.04]",
          config.text,
        )}
      >
        <Icon size={160} />
      </div>
    </Card>
  );
}
