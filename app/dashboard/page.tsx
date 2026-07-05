
"use client";

import { AcademicPressure } from "@/components /shared/academic-pressure";
import { DashboardHero } from "@/components /shared/dashbaord-hero";
import { DashboardActions } from "@/components /shared/dashboard-actions";
import { DashboardActivity } from "@/components /shared/dashboard-activity";
import { DashboardAlerts } from "@/components /shared/dashboard-alerts";
import { DashboardMetrics } from "@/components /shared/dashboard-metrics";
import { DashboardSurvival } from "@/components /shared/dashboard-survival";


export default function Page() {
  const financialStatus = {
    runwayDays: 14,
    availableBalance: "₦18,500",
    safeLockedBalance: "₦35,000",
    sapaRisk: "Low",
    mode: "Normal",
  };

  const recentIntercepts = [
    {
      id: 1,
      type: "warning",
      message: "Stopped an impulsive ₦12,000 transfer on Sunday night.",
      time: "2 hours ago",
    },
    {
      id: 2,
      type: "gig",
      message: "Found a delivery job on campus matching your free hours.",
      time: "5 hours ago",
    },
  ];

  const alerts = [
    {
      id: 1,
      title: "Exams are 11 days away",
      description:
        "Zelta has reduced your recommended weekly spend by 18%.",
    },
    {
      id: 2,
      title: "Your runway is stable",
      description:
        "You can safely maintain current spending for 14 days.",
    },
  ];

  return (
    <main className="min-h-screen text-white">
      <div className=" md:px-6 px-4 py-6 space-y-6">

        <DashboardHero
          runwayDays={financialStatus.runwayDays}
        />
                <DashboardMetrics  financialStatus={financialStatus} />
        <AcademicPressure alerts={alerts} logs={recentIntercepts}  />
          <DashboardActions />


      </div>
    </main>
  );
}