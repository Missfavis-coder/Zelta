import { CalendarDays, ShieldCheck, Zap } from "lucide-react";

interface Alert {
  id: number;
  title: string;
  description: string;
}

export function AcademicPressure({
  alerts,
  logs
}: {
  alerts: Alert[];
  logs: {
    id: number;
    message: string;
    time: string;
    saved?: boolean;
  }[];
}) {
    return (
      <section className="rounded-md bg-neutral-800/20 dark:bg-neutral-200/30 md:p-6 p-4 ">
        <div className="">
           
          <div className="space-y-3">  


  
  <div className=" grid md:grid-cols-2 grid-cols-1 gap-4 space-y-8">

  <div className="">

  <div className="mb-6">
    <span className="text-neutral-500 dark:text-foreground/80 lg:text-sm text-xs font-semibold uppercase">
      AI Activity
    </span>

    <p className="text-sm text-neutral-300 dark:text-foreground/80 mt-1">
      Real-time financial protection and opportunities.
    </p>
  </div>

  <div className="divide-y divide-neutral-900 dark:divide-neutral-200">
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
          <p className="text-sm text-neutral-400 dark:text-foreground/70">
            {log.message}
          </p>

          <span className="text-xs text-neutral-500 dark:text-foreground mt-1 block">
            {log.time}
          </span>
        </div>

      </div>
    ))}
  </div>      

  </div>

  <div className="md:border-l border-neutral-800 dark:border-neutral-200 md:pl-6">
  <div className="text-neutral-500 dark:text-foreground/80 uppercase font-semibold md:text-sm text-xs mb-4">Notification to keep you on track</div>
  {alerts.map((alert) => (
          <div
            key={alert.id}
            className="flex items-start justify-between space-y-5 "
          >
            <div className="space-y-1">

              <div className="flex items-center gap-2">
                <div className="h-2 w-2 rounded-full bg-amber-500" />

                <h3 className="font-light text-sm dark:text-foreground/90 text-white">
                  {alert.title}
                </h3>
              </div>

              <p className="md:text-sm text-xs leading-relaxed dark:text-foreground/70 text-neutral-400 pl-4">
                {alert.description}
              </p>

            </div>

            <span className="text-xs text-neutral-500 dark:text-gray-800 whitespace-nowrap">
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