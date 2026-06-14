"use client";

import {
  Wallet,
  Shield,
  Lock,
  Sparkles,
  TrendingUp,
  Plus,
  AlertTriangle,
} from "lucide-react";

/* ==========================================
   TYPES
========================================== */

type SavingsGoal = {
  id: number;
  title: string;
  target: number;
  saved: number;
};

type Activity = {
  id: number;
  amount: string;
  date: string;
};

type HealthStatus = "STRONG" | "FAIR" | "VULNERABLE";

/* ==========================================
   DATA (replace with API later)
========================================== */

const goals: SavingsGoal[] = [
  {
    id: 1,
    title: "Emergency Fund",
    target: 50000,
    saved: 35000,
  },
  {
    id: 2,
    title: "New Laptop",
    target: 250000,
    saved: 40000,
  },
  {
    id: 3,
    title: "School Fees Backup",
    target: 100000,
    saved: 55000,
  },
];

const activities: Activity[] = [
  {
    id: 1,
    amount: "+ ₦2,000 Saved",
    date: "Yesterday",
  },
  {
    id: 2,
    amount: "+ ₦5,000 Saved",
    date: "3 days ago",
  },
  {
    id: 3,
    amount: "+ ₦1,500 Saved",
    date: "Last week",
  },
];

/* ==========================================
   COMPONENTS
========================================== */

function HeroCard() {
  return (

    <div className="bg-neutral-800/30 rounded-3xl p-6 md:p-8">


      <div className="grid md:grid-cols-2 gap-4">
        <div className="bg-neutral-800/20 rounded-md p-6">
          <p className="text-sm text-neutral-400 uppercase font-bold">
            Current Savings
          </p>

          <h2 className="text-xl font-bold mt-2">
            ₦45,000
          </h2>
        </div>

        <div className="bg-neutral-800/20 rounded-md p-6">
          <p className="text-sm text-neutral-400 uppercase font-bold">
            Progress This Month
          </p>

          <h2 className="text-xl font-bold mt-2 text-amber-400">
            +₦8,500
          </h2>
        </div>
      </div>

      <button className="mt-6 cursor-pointer font-bold bg-[#8c52f1] hover:bg-purple-700 px-5 py-3 rounded-xl text-sm font-medium transition">
        Add Savings
      </button>
    </div>
  );
}

function SavingsHealth({
  status,
}: {
  status: HealthStatus;
}) {
  const styles = {
    STRONG: "bg-green-500/20 text-green-400",
    FAIR: "bg-yellow-500/20 text-yellow-400",
    VULNERABLE: "bg-red-500/20 text-red-400",
  };

  return (
    <div className="bg-neutral-800/30 rounded-3xl p-6">
      <div className="flex items-center gap-2 mb-4">
        <Shield className="text-[#8c52f1]" />

        <h2 className="font-semibold">
          Savings Health
        </h2>
      </div>

      <div
        className={`inline-flex px-4 py-2 rounded-full text-sm font-medium ${styles[status]}`}
      >
        {status}
      </div>

      <p className="text-neutral-300 mt-4">
        You currently have enough savings
        to cover approximately 14 days of expenses.
      </p>
    </div>
  );
}

function GoalCard({
  title,
  target,
  saved,
}: SavingsGoal) {
  const percentage = Math.min(
    (saved / target) * 100,
    100
  );

  return (
    <div className="bg-neutral-800/30 rounded-3xl p-5">
      <h3 className="font-semibold">
        {title}
      </h3>

      <div className="mt-4">
        <p className="text-sm text-neutral-400">
          Goal
        </p>

        <p className="font-semibold">
          ₦{target.toLocaleString()}
        </p>
      </div>

      <div className="mt-3">
        <p className="text-sm text-neutral-400">
          Saved
        </p>

        <p className="font-semibold">
          ₦{saved.toLocaleString()}
        </p>
      </div>

      <div className="mt-4">
        <div className="w-full h-2 bg-neutral-700/30 rounded-full">
          <div
            className="h-2 rounded-full bg-amber-400"
            style={{
              width: `${percentage}%`,
            }}
          />
        </div>

        <p className="text-xs text-neutral-400 mt-2">
          {Math.round(percentage)}%
        </p>
      </div>
    </div>
  );
}

function LockedSavingsCard() {
  return (
    <div className="bg-neutral-800/30 rounded-3xl p-6">
      <div className="flex items-center gap-2 mb-4">
        <h2 className="font-semibold uppercase">
          Locked Protection Fund
        </h2>
      </div>

      <p className="text-neutral-400 text-sm">
        Amount Locked
      </p>

      <h3 className="text-xl font-bold mt-2">
        ₦20,000
      </h3>

      <p className="text-neutral-400 text-sm mt-4">
        Unlock Date
      </p>

      <p className="font-bold">
        August 30, 2026
      </p>

      <p className="text-sm text-neutral-300 mt-4">
        Money here is mentally protected
        from impulse spending.
      </p>

      <button className="mt-5 bg-[#8c52f1] px-4 py-2 rounded-xl cursor-pointer font-bold text-sm">
        Lock More Money
      </button>
    </div>
  );
}

function ActivityCard() {
  return (
    <div className="bg-neutral-800/30 rounded-3xl p-6">
      <h2 className="font-semibold mb-4 uppercase">
        Recent Activity
      </h2>

      <div className="space-y-4">
        {activities.map((activity) => (
          <div
            key={activity.id}
            className="flex items-center justify-between"
          >
            <p className="text-amber-400 text-sm">{activity.amount}</p>

            <span className="text-xs text-neutral-400">
              {activity.date}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}

function EmergencyCard() {
  return (
    <div className="bg-red-600/10 rounded-3xl p-6">
      <div className="flex items-center gap-2 mb-3">
        <AlertTriangle
          className="text-red-400"
          size={18}
        />

        <h2 className="font-semibold">
          Emergency Recommendation
        </h2>
      </div>

      <p className="text-neutral-300">
        Your runway is below 7 days.
      </p>

      <ul className="mt-4 space-y-2 text-sm text-neutral-300">
        <li>• Avoid non-essential spending.</li>
        <li>• Consider campus gigs.</li>
        <li>• Delay impulse purchases.</li>
        <li>• Use emergency savings wisely.</li>
      </ul>
    </div>
  );
}

function MotivationCard() {
  return (
    <div className="bg-neutral-800/30 rounded-3xl p-6">
      <div className="flex items-center gap-2 mb-3">
        <Sparkles
          className="text-[#8c52f1]"
          size={18}
        />

        <h2 className="font-semibold">
          A Note From Zelta
        </h2>
      </div>

      <p className="text-neutral-300 leading-relaxed">
        Saving isn't about being rich.
        It's about giving yourself options.

        <br />
        <br />

        The student who has ₦10,000 saved
        is often less stressed than the student
        with ₦0.

        <br />
        <br />

        No matter how small the amount,
        consistency beats intensity.

        <br />
        <br />

        Omo, small small... e go reach. 💜
      </p>
    </div>
  );
}

/* ==========================================
   PAGE
========================================== */

export default function SavingsPage() {
  return (
    <div className="min-h-screen text-white p-4 md:p-6">
      <div className="space-y-6">

        <HeroCard />


        <div>
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-xl font-bold">
              Savings Goals
            </h2>

            <button className="flex items-center gap-2 bg-[#8c52f1] px-4 py-2 rounded-xl text-sm">
              <Plus size={16} />
              Create Goal
            </button>
          </div>

          <div className="grid md:grid-cols-2 xl:grid-cols-3 gap-4">
            {goals.map((goal) => (
              <GoalCard
                key={goal.id}
                {...goal}
              />
            ))}
          </div>
        </div>

        <LockedSavingsCard />

        <ActivityCard />

        <EmergencyCard />



      </div>
    </div>
  );
}