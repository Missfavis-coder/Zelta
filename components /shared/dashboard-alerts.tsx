"use client";

import { CalendarDays } from "lucide-react";

interface Alert {
  id: number;
  title: string;
  description: string;
}

export function DashboardAlerts({
  alerts,
}: {
  alerts: Alert[];
}) {
  return (
    <section className="rounded-3xl border border-white/10 bg-white/5 backdrop-blur-xl overflow-hidden">

      <div className="border-b border-white/10 px-6 py-4">
        <div className="flex items-center justify-between gap-4 flex-wrap">

          <div>
            <p className="text-sm text-zinc-400">
              Academic Financial Intelligence
            </p>

            <h2 className="text-xl font-semibold text-white mt-1">
              Help Zelta understand your semester pressure.
            </h2>
          </div>

          <button className="inline-flex items-center gap-2 rounded-xl border border-cyan-400/20 bg-cyan-400/10 px-4 py-2 text-sm text-cyan-300 transition hover:bg-cyan-400/20">
            <CalendarDays className="h-4 w-4" />
            Set Exam Date
          </button>

        </div>
      </div>

      <div className="divide-y divide-white/5">

        {alerts.map((alert) => (
          <div
            key={alert.id}
            className="flex items-start justify-between gap-6 px-6 py-5"
          >
            <div className="space-y-1">

              <div className="flex items-center gap-2">
                <div className="h-2 w-2 rounded-full bg-emerald-400" />

                <h3 className="font-medium text-white">
                  {alert.title}
                </h3>
              </div>

              <p className="text-sm leading-relaxed text-zinc-400 pl-4">
                {alert.description}
              </p>

            </div>

            <span className="text-xs text-zinc-500 whitespace-nowrap">
              AI Insight
            </span>
          </div>
        ))}

      </div>

    </section>
  );
}