"use client";

import React from "react";
import {
  Wallet,
  ClipboardList,
  ShoppingBag,
  Brain,
  TriangleAlert,
  RefreshCcw,
  BriefcaseBusiness,
  ChartColumn,
  ArrowDown,
  HeartPlus,
} from "lucide-react";

const flow = [
  {
    title: "Your Money",
    steps: [
      {
        icon: Wallet,
        label: "Receive allowance",
        description: "Money enters your wallet.",
      },
      {
        icon: ClipboardList,
        label: "Create spending plan",
        description: "Set limits before spending.",
      },
      {
        icon: ShoppingBag,
        label: "Spend normally",
        description: "Go about your daily expenses.",
      },
    ],
  },
  {
    title: "ZELTA Intelligence",
    steps: [
      {
        icon: Brain,
        label: "Tracks spending patterns",
        description: "Learns your financial habits.",
      },
      {
        icon: TriangleAlert,
        label: "Warns before overspending",
        description: "Alerts you before your budget breaks.",
      },
      {
        icon: RefreshCcw,
        label: "Suggests better choices",
        description: "Offers smarter alternatives instantly.",
      },
    ],
  },
  {
    title: "Support",
    steps: [
      {
        icon: BriefcaseBusiness,
        label: "Recommends campus gigs",
        description: "Extra income whenever needed.",
      },
    ],
  },
  {
    title: "Results",
    steps: [
      {
        icon: ChartColumn,
        label: "Monthly financial recap",
        description: "Clear insights into your spending.",
      },
    ],
  },
];

export default function WhatZeltaDoesPage() {
  return (
    <main className="min-h-screen  py-20  mt-12 px-6">
      <div className="mx-auto max-w-4xl">
        {/* Header */}
        <div className="my-14">

          <h1 className="text-2xl lg:text-3xl md:text-3xl text-center font-bold tracking-tight mb-2 dark:text-[#160a2a]/90 text-white">
            Your money.
            <br />
           <span className="font-serif tracking-widest text-amber-500">ZELTA </span> handles the thinking.
          </h1>

          <p className="mt-4 md:text-[15px] text-sm max-w-3xl mx-auto text-gray-300 dark:text-foreground/80 text-center">
            Plan your spending once. ZELTA quietly monitors your habits,
            predicts problems early and helps you stay financially healthy.
          </p>
        </div>

        {/* Flow */}
        <div className="space-y-10">
          {flow.map((section, sectionIndex) => (
            <div key={section.title}>
              {/* Section title */}
              <div className="mb-5 flex items-center gap-3">
                <div className="h-px flex-1 bg-neutral-900 dark:bg-neutral-200" />

                <span className="text-xs font-semibold uppercase tracking-[0.2em] text-[#8c52f1]">
                  {section.title}
                </span>

                <div className="h-px flex-1 bg-neutral-900 dark:bg-neutral-200" />
              </div>

              {/* Cards */}
              <div className="space-y-3">
                {section.steps.map((step) => {
                  const Icon = step.icon;

                  return (
                    <div
                      key={step.label}
                      className="group flex items-center gap-5 rounded-3xl bg-neutral-800/40 dark:bg-[#8c52f1]/[0.06] p-5 transition-all duration-200 hover:shadow-xs"
                    >
                      <div className="flex h-12 w-12 items-center justify-center rounded-md bg-amber-500/10 text-amber-500">
                        <Icon size={18} strokeWidth={2} />
                      </div>

                      <div className="flex-1">
                        <h3 className="md:text-base text-sm font-semibold dark:text-foreground text-white">
                          {step.label}
                        </h3>

                        <p className="mt-1 md:text-sm text-xs text-gray-300 dark:text-foreground/70">
                          {step.description}
                        </p>
                      </div>
                    </div>
                  );
                })}
              </div>

              {/* Arrow */}
              {sectionIndex !== flow.length - 1 && (
                <div className="my-8 flex justify-center">
                  <div className="flex h-10 w-10 items-center justify-center rounded-full border border-[#8c52f1]/20 bg-[#8c52f1]/20 dark:text-foreground/90 text-white">
                    <ArrowDown size={18} />
                  </div>
                </div>
              )}
            </div>
          ))}
        </div>

        {/* Footer */}
        <div className="mt-16 border-t border-neutral-800 dark:border-neutral-200 pt-6 flex items-center justify-between">
          <p className="text-sm text-white dark:text-foreground">
            8 steps • Intelligent student finance
          </p>

          <span className="inline-flex gap-1 items-center  px-3 py-1 text-xs font-medium text-violet-600">
            <HeartPlus size={14}/>
            ZELTA AI
          </span>
        </div>
      </div>
    </main>
  );
}