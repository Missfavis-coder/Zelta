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
      color: "text-[#8c52f1] bg-[#8c52f1]/10",
    },
    {
      title: "Business Simulator",
      description: "Validate campus hustle ideas",
      href: "/dashboard/simulator",
      icon: Brain,
      color: "text-blue-400 bg-blue-400/10",
    },
    {
      title: "Opportunity Gigs",
      description: "Find quick earning opportunities",
      href: "/dashboard/gigs",
      icon: Zap,
      color: "text-amber-400 bg-amber-400/10",
    },
  ];
  
  export function DashboardActions() {
    return (
      <div>
  
        <div className="mb-4">
          <h2 className="text-lg font-bold dark:text-[#160a2a]/90">
            Quick Actions
          </h2>
  
          <p className="text-sm text-neutral-400 dark:text-foreground/80 mt-1">
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
                className="group rounded-md bg-neutral-800/20 dark:bg-neutral-200/30 p-6 hover:border-neutral-700 transition-all duration-300 hover:-translate-y-1"
              >
  
                <div className={`w-fit rounded-2xl  p-3 ${action.color}`}>
                  <Icon size={20} />
                </div>
  
                <div className="mt-10 flex items-end justify-between">
                  <div>
                    <h3 className="font-semibold dark:text-[#160a2a]/90" >
                      {action.title}
                    </h3>
  
                    <p className="text-sm text-neutral-500 dark:text-foreground/70 mt-1">
                      {action.description}
                    </p>
                  </div>
  
                  <ArrowUpRight
                    size={18}
                    className="text-neutral-600 dark:text-foreground dark:group-hover:text-[#160a2a]/90 group-hover:text-white transition-colors"
                  />
                </div>
  
              </Link>
            );
          })}
  
        </div>
      </div>
    );
  }