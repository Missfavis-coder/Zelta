"use client";

import {
  Briefcase,
  GraduationCap,
  Laptop,
  MapPin,
  ShieldCheck,
  Sparkles,
  TrendingUp,
  Wallet,
} from "lucide-react";


type Gig = {
  title: string;
  location: string;
  earnings: string;
  commitment: string;
  description: string;
};

type Category = {
  title: string;
  icon: React.ElementType;
  earnings: string;
  items: string[];
};

type TutorGig = {
  title: string;
  skill: string;
  earnings: string;
};


const categories: Category[] = [
  {
    title: "Academic Gigs",
    icon: GraduationCap,
    earnings: "₦2,000 - ₦20,000",
    items: [
      "Tutorials",
      "Assignment Help",
      "Exam Coaching",
      "Project Guidance",
    ],
  },
  {
    title: "Tech Gigs",
    icon: Laptop,
    earnings: "₦5,000 - ₦100,000+",
    items: [
      "Frontend Development",
      "UI/UX Design",
      "Graphics Design",
      "Video Editing",
    ],
  },
  {
    title: "Quick Cash Tasks",
    icon: Briefcase,
    earnings: "₦1,000 - ₦15,000",
    items: [
      "Typing Notes",
      "Data Entry",
      "Printing Services",
      "Event Assistance",
    ],
  },
  {
    title: "Local Opportunities",
    icon: MapPin,
    earnings: "₦2,000 - ₦20,000",
    items: [
      "Errands",
      "Deliveries",
      "Cleaning",
      "Personal Assistance",
    ],
  },
];

const featuredGigs: Gig[] = [
  {
    title: "Mathematics Tutor",
    location: "200 Level Engineering Students",
    earnings: "₦15,000 - ₦40,000",
    commitment: "2 - 3 hrs weekly",
    description:
      "Help junior students understand difficult concepts and earn while doing it.",
  },
  {
    title: "Frontend Website Fixes",
    location: "Students & Small Businesses",
    earnings: "₦10,000 - ₦60,000",
    commitment: "Flexible",
    description:
      "Fix websites, create landing pages, and earn from your tech skills.",
  },
  {
    title: "Assignment Formatting",
    location: "Campus-wide",
    earnings: "₦2,000 - ₦15,000",
    commitment: "Flexible",
    description:
      "Help students organize projects, reports, and presentations.",
  },
];

const tutorOpportunities: TutorGig[] = [
  {
    title: "Web Development Tutor",
    skill: "HTML, CSS, JavaScript",
    earnings: "₦5,000 - ₦30,000/month",
  },
  {
    title: "Mathematics Tutor",
    skill: "Engineering Mathematics",
    earnings: "₦10,000 - ₦40,000/month",
  },
];



function HeroSection() {
  return (
    <div className="">

      <div className="mt-5 p-4 rounded-2xl bg-[#8c52f1]/10 ">
        <p className="text-sm md:text-sm tracking-wide">
          ⚠️ Your financial runway is getting shorter.
          Instead of cutting feeding completely, consider earning
          ₦5,000 - ₦30,000 through trusted opportunities around you.
        </p>
      </div>
    </div>
  );
}

function CategoryCard({
  title,
  icon: Icon,
  earnings,
  items,
}: Category) {
  return (
    <div className="bg-neutral-800/30 rounded-2xl p-5">
      <Icon className="text-[#8c52f1] mb-3" size={24} />

      <h3 className="font-semibold mb-2">{title}</h3>

      <ul className="text-sm text-neutral-300 space-y-1">
        {items.map((item) => (
          <li key={item}>• {item}</li>
        ))}
      </ul>

      <p className="mt-4 text-xs text-amber-400">
        {earnings}
      </p>
    </div>
  );
}

function GigCard({ gig }: { gig: Gig }) {
  return (
    <div className="bg-neutral-800/30 rounded-3xl p-5">
      <h3 className="font-semibold text-lg">
        {gig.title}
      </h3>

      <p className="text-sm text-neutral-400 mt-2">
        📍 {gig.location}
      </p>

      <p className="text-sm text-amber-400 mt-2">
        {gig.earnings}
      </p>

      <p className="text-sm text-neutral-400 mt-1">
        {gig.commitment}
      </p>

      <p className="text-sm text-neutral-300 mt-4 tracking-wide">
        {gig.description}
      </p>

      <button className="mt-5 w-full bg-[#8c52f1] hover:bg-purple-600 py-3 rounded-xl text-sm font-bold transition cursor-pointer">
        View Opportunity
      </button>
    </div>
  );
}

function TutorCard({ tutor }: { tutor: TutorGig }) {
  return (
    <div className="bg-neutral-800/30 rounded-2xl p-5">
      <h3 className="font-semibold text-sm">
        {tutor.title}
      </h3>

      <p className="text-sm text-neutral-400 mt-2">
        {tutor.skill}
      </p>

      <p className="text-amber-400 text-sm mt-2">
        {tutor.earnings}
      </p>

      <button className="mt-4 bg-[#8c52f1] px-4 py-2 rounded-xl text-sm font-bold cursor-pointer">
        Start Teaching
      </button>
    </div>
  );
}

/* ==========================================
   PAGE
========================================== */

export default function GigsPage() {
  return (
    <div className="min-h-screen text-white p-4 md:p-6">
      <div className="space-y-6">

        <HeroSection />

        <div className="grid md:grid-cols-2 xl:grid-cols-4 gap-4">
          {categories.map((category) => (
            <CategoryCard
              key={category.title}
              {...category}
            />
          ))}
        </div>

        <div className=" ">
          <div className="flex items-center gap-2 mb-3">
            <h2 className="font-semibold uppercase text-sm">
             From Zelta
            </h2>
          </div>

          <p className="text-neutral-300 leading-relaxed text-sm">
            Omo, things fit tight sometimes.
            Running low on cash no mean say you don fail.
            Plenty students dey survive by tutoring,
            offering tech services, helping with assignments,
            and doing small gigs around campus.
          </p>
        </div>

        <div>
          <div className="flex items-center gap-2 mb-5">
            <h2 className="md:text-x1 text-[16px] font-bold uppercase">
              Recommended Opportunities
            </h2>
          </div>

          <div className="grid lg:grid-cols-3 gap-4">
            {featuredGigs.map((gig) => (
              <GigCard
                key={gig.title}
                gig={gig}
              />
            ))}
          </div>
        </div>

        <div className="">
          <h2 className="md:text-xl text-[16px] font-bold mb-3 uppercase">
            Become a Tutor
          </h2>

          <p className="text-neutral-300 text-sm mb-5">
            Good for students who understand a subject
            well and want to earn consistently.
          </p>

          <div className="grid md:grid-cols-2 gap-4">
            {tutorOpportunities.map((tutor) => (
              <TutorCard
                key={tutor.title}
                tutor={tutor}
              />
            ))}
          </div>
        </div>

        <div className="bg-neutral-800/30 rounded-3xl p-6">
          <div className="flex items-center gap-2 mb-3">
            <ShieldCheck
              className="text-green-400"
              size={20}
            />

            <h2 className="font-semibold">
              Stay Safe
            </h2>
          </div>

          <ul className="space-y-3 text-neutral-300 text-sm">
            <li>• Avoid gigs requiring upfront payments.</li>
            <li>• Be careful with unrealistic promises.</li>
            <li>• Never share sensitive banking information.</li>
            <li>• Meet safely for physical jobs.</li>
            <li>• Report suspicious opportunities.</li>
          </ul>
        </div>

      </div>
    </div>
  );
}