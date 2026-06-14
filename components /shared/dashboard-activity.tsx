import {
    ShieldCheck,
    Zap,
  } from "lucide-react";
  
  export function DashboardActivity({
    logs,
  }: {
    logs: {
      id: number;
      message: string;
      time: string;
      saved: boolean;
    }[];
  }) {
    return (
      <div className="rounded-3xl border border-neutral-900 bg-[#0b0b0b] p-6">
  
        <div className="mb-6">
          <h2 className="text-lg font-bold">
            AI Activity
          </h2>
  
          <p className="text-sm text-neutral-500 mt-1">
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
    );
  }