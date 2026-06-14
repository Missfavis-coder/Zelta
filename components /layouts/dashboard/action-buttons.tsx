"use client";

import { cn } from "@/lib/utils";
import {
  ScanLine,
  QrCode,
  User,
  Phone,
  Plus,
  ArrowDownToLine,
} from "lucide-react";
import Link from "next/link";
import { ScanModal } from "./scan";
import { useState } from "react";
import { FundWalletModal } from "./fund";
import { WithdrawModal } from "./withdraw";

const actions = [
  { label: "Tap", icon: ScanLine },
  { label: "Scan", icon: QrCode },
  { label: "Fund", icon: Plus },
  { label: "Withdraw", icon: ArrowDownToLine },
];

export function ActionRail() {
  const [openScan, setOpenScan] = useState(false);
  const [openFund, setOpenFund] = useState(false);
  const [openWithdraw, setOpenWithdraw] = useState(false);
  return (
    <div className="w-full overflow-x-auto px-2 mt-4">
      <div className="text-green-500 font-bold px-2">Quick Actions</div>
      <div className="flex gap-6 py-2">
        {actions.map((action) => {
          const Icon = action.icon;
          const isScan = action.label === "Scan";
          const isFund = action.label === "Fund";
          const isWithdraw = action.label === "Withdraw";

          return (
            <button
              key={action.label}
              onClick={() => {
                if (isScan) setOpenScan(true);
                if (isFund) setOpenFund(true);
                if (isWithdraw) setOpenWithdraw(true);
              }}
              className={cn(
                "flex flex-col items-center justify-center gap-2 mt-4",
                "min-w-[80px] px-4 py-3 rounded-md cursor-pointer",
                "bg-white/5 border border-white/10",
                "hover:bg-green-600/10 transition",
              )}
            >
              <Icon className="w-5 h-5 text-white/80" />
              <span className="text-[11px] text-neutral-300">
                {action.label}
              </span>
            </button>
          );
        })}
      </div>
      <ScanModal open={openScan} onClose={() => setOpenScan(false)} />
      <FundWalletModal open={openFund} onClose={() => setOpenFund(false)} />
      <WithdrawModal
        open={openWithdraw}
        onClose={() => setOpenWithdraw(false)}
      />
    </div>
  );
}

