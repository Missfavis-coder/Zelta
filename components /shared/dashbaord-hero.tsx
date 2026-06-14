export function DashboardHero({
    runwayDays,
  }: {
    runwayDays: number;
  }) {
    return (
      <div className="relative overflow-hidden">
  
        <div className="relative z-10 flex flex-col md:flex-row md:items-center justify-between gap-6">
  
          <div className="flex flex-col gap-4">

            {/* allowance flex */}
            <div className="flex flex-wrap items-center gap-3">
  
              <div className="flex items-center gap-2 text-xs">
                <span className="text-neutral-200">
                  Allowance:
                </span>
  
                <span className="font-semibold text-white">
                  Monthly
                </span>
              </div>
  
              <div className="w-1 h-1 rounded-full bg-neutral-700" />
  
              <div className="flex items-center gap-2 text-xs">
                <span className="text-neutral-200">
                  Average:
                </span>
  
                <span className="font-semibold text-[#8c52f1]">
                  ₦85,000
                </span>
              </div>
  
              <div className="w-1 h-1 rounded-full bg-neutral-700" />
  
              <div className="flex items-center gap-2 text-xs">
                <span className="text-neutral-200">
                  Next payment:
                </span>
  
                <span className="font-semibold text-white">
                  12 days
                </span>
              </div>
  
            </div>
  
          </div>
  
          <div className="flex items-center gap-3 bg-[#8c52f1]/10  px-4 py-3 rounded-full">
            <div className="relative flex h-2 w-2">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-[#8c52f1] opacity-75" />
              <span className="relative inline-flex rounded-full h-2 w-2 bg-[#8c52f1]" />
            </div>
  
            <div>
              <p className="text-xs font-semibold">
                AI Active
              </p>
            </div>
          </div>
  
        </div>

        
      </div>
    );
  }