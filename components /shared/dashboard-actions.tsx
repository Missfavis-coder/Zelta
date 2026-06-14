import {
    ArrowUpRight,
    Brain,
    MessageSquareCode,
    Zap,
  } from "lucide-react";
  
  import Link from "next/link";
  
  const actions = [
    {
      title: "Chat with AI",
      description: "Ask for financial guidance",
      href: "/dashboard/chat",
      icon: MessageSquareCode,
      color: "text-[#8c52f1]",
    },
    {
      title: "Business Simulator",
      description: "Validate campus hustle ideas",
      href: "/dashboard/simulator",
      icon: Brain,
      color: "text-blue-400",
    },
    {
      title: "Opportunity Gigs",
      description: "Find quick earning opportunities",
      href: "/dashboard/gigs",
      icon: Zap,
      color: "text-amber-400",
    },
  ];
  
  export function DashboardActions() {
    return (
      <div>
  
        <div className="mb-4">
          <h2 className="text-lg font-bold">
            Quick Actions
          </h2>
  
          <p className="text-sm text-neutral-500 mt-1">
            Access Zelta intelligence tools instantly.
          </p>
        </div>
  
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
  
          {actions.map((action) => {
            const Icon = action.icon;
  
            return (
              <Link
                key={action.title}
                href={action.href}
                className="group rounded-3xl border border-neutral-900 bg-[#0b0b0b] p-6 hover:border-neutral-700 transition-all duration-300 hover:-translate-y-1"
              >
  
                <div className={`w-fit rounded-2xl bg-neutral-900 p-3 ${action.color}`}>
                  <Icon size={20} />
                </div>
  
                <div className="mt-10 flex items-end justify-between">
                  <div>
                    <h3 className="font-semibold">
                      {action.title}
                    </h3>
  
                    <p className="text-sm text-neutral-500 mt-1">
                      {action.description}
                    </p>
                  </div>
  
                  <ArrowUpRight
                    size={18}
                    className="text-neutral-600 group-hover:text-white transition-colors"
                  />
                </div>
  
              </Link>
            );
          })}
  
        </div>
      </div>
    );
  }