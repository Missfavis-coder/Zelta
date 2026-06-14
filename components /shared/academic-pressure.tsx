import { CalendarDays } from "lucide-react";

interface Alert {
  id: number;
  title: string;
  description: string;
}

export function AcademicPressure({
  alerts,
}: {
  alerts: Alert[];
}) {
    return (
      <section className="rounded-3xl bg-neutral-800/30 p-6 backdrop-blur-xl">
        <div className="">
  
          <div className="space-y-3">

      <div className=" ">
        <div className="flex items-center justify-between gap-4 flex-wrap">

          <div>
            <p className="md:text-sm text-xs font-semibold text-neutral-500 uppercase">
              Academic Financial Intelligence
            </p>

            <h2 className="lg:text-[16px] text-[14px] font-semibold text-white mt-1">
              Help Zelta understand your semester pressure.
            </h2>
          </div>

          <button className="inline-flex items-center gap-2 rounded-md bg-purple-500/10 px-4 py-2 text-sm text-amber-400 transition hover:bg-cyan-400/20">
            <CalendarDays className="h-4 w-4" />
            Set Exam Date
          </button>

        </div>
      </div>
  
  <div className=" grid md:grid-cols-2 grid-cols-1 gap-4">
  <div className="bg-neutral-800/20 py-4 px-4 rounded-md">
  <div>
              <h2 className="text-[16px] font-bold text-purple-500">
                Exams in 11 Days
              </h2>
  
              <p className="mt-2 max-w-xl text-xs font-semibold leading-relaxed text-white">
                Zelta has automatically reduced your recommended weekly
                spending limit to protect your runway during exam season.
              </p>
            </div>
              
          <div className="w-full space-y-3 mt-2">
            <div className="flex items-center justify-between text-sm">
              <span className="text-white font-semibold">Stress Multiplier</span>
  
              <span className="font-medium text-purple-300">
                Increasing
              </span>
            </div>
  
            <div className="h-2 overflow-hidden rounded-full bg-white/10">
              <div className="h-full w-[72%] rounded-full bg-amber-400" />
            </div>
  
            <div className="flex items-center justify-between text-xs text-neutral-300">
              <span>Low Pressure</span>
              <span>High Pressure</span>
            </div>
          </div>
  </div>

  <div className="bg-neutral-800/20 py-4 px-4 rounded-md">
  <div className="text-purple-500 uppercase font-semibold md:text-sm text-xs mb-4">Notification to keep you on track</div>
  {alerts.map((alert) => (
          <div
            key={alert.id}
            className="flex items-start justify-between gap-6 "
          >
            <div className="space-y-1">

              <div className="flex items-center gap-2">
                <div className="h-2 w-2 rounded-full bg-amber-500" />

                <h3 className="font-semibold md:text-sm text-[15px] text-white">
                  {alert.title}
                </h3>
              </div>

              <p className="text-sm leading-relaxed text-neutral-300 pl-4">
                {alert.description}
              </p>

            </div>

            <span className="text-xs text-neutral-500 whitespace-nowrap">
              AI Insight
            </span>
          </div>
        ))}

  </div>
  </div>


  
          </div>


        </div>
      </section>
    );
  }