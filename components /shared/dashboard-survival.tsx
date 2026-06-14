export function DashboardSurvival() {
    return (
      <section className="grid grid-cols-1 lg:grid-cols-2 gap-6">
  
        <div className="rounded-3xl border border-emerald-400/10 bg-emerald-400/5 p-6 backdrop-blur-xl">
          <div className="space-y-3">
  
            <div className="inline-flex items-center rounded-full border border-emerald-400/20 bg-emerald-400/10 px-3 py-1 text-xs text-emerald-300">
              Safe Spending Prediction
            </div>
  
            <h3 className="text-2xl font-bold text-white">
              ₦2,300 Safe To Spend Today
            </h3>
  
            <p className="text-sm leading-relaxed text-zinc-400">
              Based on your current runway, academic schedule, and
              recent spending behavior, Zelta predicts this amount
              keeps you financially stable.
            </p>
  
          </div>
        </div>
  
        <div className="rounded-3xl border border-cyan-400/10 bg-cyan-400/5 p-6 backdrop-blur-xl">
          <div className="space-y-3">
  
            <div className="inline-flex items-center rounded-full border border-cyan-400/20 bg-cyan-400/10 px-3 py-1 text-xs text-cyan-300">
              Runway Projection
            </div>
  
            <h3 className="text-2xl font-bold text-white">
              Runway Extends To June 29
            </h3>
  
            <p className="text-sm leading-relaxed text-zinc-400">
              If your current spending pace remains stable, your
              available balance should safely sustain your lifestyle
              beyond this month.
            </p>
  
          </div>
        </div>
  
      </section>
    );
  }