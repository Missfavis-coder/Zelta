"use client";

import {
  Wallet,
  Shield,
  Lock,
  Sparkles,
  TrendingUp,
  Plus,
  AlertTriangle,
  LucideIcon,
  FileStack,
  Moon,
  Check,
  FolderCheck,
  CheckCircle,
} from "lucide-react";

type SavingsGoal = {
  id: number;
  title: string;
  target: number;
  saved: number;
};

type Activity = {
  id: number;
  title: string;
  activity:string;
  description: string;
  icon: LucideIcon;
};




const activities: Activity[] = [
  {
    id: 1,
    title: "Total Goals Created",
    activity: "12 Goals",
    description: 'All savings goals created so far',
    icon:FolderCheck
  },
  {
    id: 2,
    title: " Goals In Progress",
    activity: "7 Active",
    description: 'Currently active and ongoing goals',
    icon:Moon
  },
  {
    id: 1,
    title: " Goals Completed",
    activity: "5 Completed",
    description: 'Successfully achieved goals',
    icon:CheckCircle
  },

];

function HeroCard() {
  return (

    <div className="">
        <div className="grid md:grid-cols-2 xl:grid-cols-3 gap-4 ">
            {activities.map((goal) => {
             const Icon = goal.icon
             return(
              <div className="bg-neutral-800/30 dark:bg-neutral-300/20 rounded-md md:p-5 p-4 ">
                <div className="flex justify-between items-center">
                  <div className="text-neutral-400 md:text-sm text-xs font-semibold dark:text-foreground/80">{goal.title}</div>
                  <div className="text-[#8c52f1]"> <Icon size={18}/> </div>
                </div>
                <div className="font-bold text-sm md:text-xl text-foreground">{goal.activity}</div>
                <div className="text-xs text-neutral-300 dark:text-foreground/70  tracking-widest ">{goal.description}</div>
              </div>
             )
           })}
        </div>
   
   
    </div>
  );
}


export default function SavingsPage() {
  return (
    <div className="min-h-screen text-white dark:text-black p-4 md:p-6">
      <div>Under Development</div>
      {/**
       *       <div className="space-y-6">

        <HeroCard />


        <div>
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-xl font-semibold dark:text-[#160a2a]/90">
             Total Savings
            </h2>

            <button className="flex items-center gap-2 bg-[#8c52f1] px-4 py-2 rounded-xl text-sm">
              <Plus size={16} />
              Create Goal
            </button>
          </div>

        </div>




      </div>
       */}

    </div>
  );
}