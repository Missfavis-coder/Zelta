"use client";
import { useRouter } from "next/navigation";
import { useState } from "react";
import { ArrowBigUp, Brain, LucideIcon, Target } from "lucide-react";
import Button from "./Button";
// import Auth from "../app/auth/page";
interface Intro {
  id: string;
  icon: LucideIcon;
  heading: string;
  details: string;
  buttonText: string;
}
const intro: Intro[] = [
  {
    id: "1",
    icon: Brain,
    heading: "Think Before You Spend",
    details:
      "Zelta analyzes your spending decisions before they happen and warns you when a purchase could hurt your financial runway.",
    buttonText: "Next",
  },

  {
    id: "2",
    icon: Target,
    heading: "Protect Your Financial Runway",
    details:
      "See how today's spending affects tomorrow. Run 'What If' simulations and understand the real impact of every money decision.",
    buttonText: "Next",
  },

  {
    id: "3",
    icon: ArrowBigUp,
    heading: "Earn, Save & Stay Ahead",
    details:
      "Discover campus gigs, build savings habits, and get personalized insights that help you survive and thrive financially as a student.",
    buttonText: "Get Started",
  },
];
export default function Home() {
  const navigate = useRouter();
  const [activeTab, setActiveTab] = useState(intro[0].id);

  //   derived states
  const current = intro.find((tab) => tab.id === activeTab);
  const currentIndex = intro.findIndex((tab) => tab.id === activeTab);
  // const currentButtonText = intro.filter(
  //   (tab) => tab.buttonText === "Get Started",
  // );

  const handleButtonClick = () => {
    if (currentIndex < intro.length - 1) {
      setActiveTab(intro[currentIndex + 1].id);
    }
    if (current?.buttonText === "Get Started") {
      navigate.push("/auth");
    }
  };

  return (
    <div className="space-y-6 h-screen flex items-center justify-center bg-black text-white">
      <div className="rounded-xl max-w-180 p-6 text-center flex flex-col justify-center items-center ">
        {current && (
          <>
            <current.icon className="h-10 w-10 stroke-1 text-purple-600" />
            <h2 className="mt-4 text-[20px] lg:text-[24px] max-w-80 font-bold">
              {current.heading}
            </h2>
            <p className="mt-2 text-neutral-300 text-[14px] max-w-90">
              {current.details}
            </p>

            <Button
              onClick={handleButtonClick}
              className="mt-6 rounded-xl w-[80%] bg-purple-500 text-white px-8 py-2 font-bold text-[14px]"
            >
              {current.buttonText}
            </Button>

            <Button
              className="mt-4 rounded-xl w-[80%]  bg-neutral-800/30   px-8 py-2 cursor-pointer text-[14px] font-bold"
              onClick={() => {
                navigate.push("/auth");
              }}
            >
              Skip
            </Button>
          </>
        )}
      </div>
    </div>
  );
}
