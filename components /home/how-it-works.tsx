"use client";

import { motion } from "framer-motion";
import { UserPlus, MessageSquare, Sparkles, CloudUpload } from "lucide-react";
import { Button } from "../ui/button";
import { useRouter } from "next/navigation";

const steps = [
  {
    icon: UserPlus,
    title: "Create an account",
    description: "Sign up in seconds and access your dashboard.",
  },
  {
    icon: CloudUpload,
    title: "Upload CSV",
    description: "Upload your bank transaction history in CSV format.",
  },
  {
    icon: MessageSquare,
    title: "Chat with ZELTA",
    description: "Tell ZELTA about your finances, goals, or concerns.",
  },
  {
    icon: Sparkles,
    title: "Get results",
    description: "Receive personalized insights, budgets, and smart recommendations.",
  },
];

export default function HowItWorks() {
  const router = useRouter();
  return (
    <section className="px-6 py-20">
      <div className="mx-auto max-w-5xl mt-8 flex flex-col justify-center items-center">
        {/* Heading */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          viewport={{ once: true }}
          className="mx-auto max-w-2xl text-center"
        >
          <h2 className="text-2xl md:text-3xl dark:text-[#160a2a] font-semibold ">
            How It Works
          </h2>
          <p className="mt-3 text-gray-300 dark:text-foreground/80 text-[14px]">
            Four simple steps. No app download required.
          </p>
        </motion.div>

        <div className="mt-14 flex flex-col lg:flex-row items-center justify-center">
  {steps.map((step, index) => {
    const Icon = step.icon;

    return (
      <div
        key={step.title}
        className="flex flex-col md:flex-row items-center"
      >
        <motion.div
          initial={{ opacity: 0, y: 25 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.45, delay: index * 0.15 }}
          viewport={{ once: true }}
          className="flex flex-col items-center text-center md:w-50 w-60"
        >
          <div className="flex h-12 w-12 items-center justify-center rounded-full border border-neutral-900 dark:border-border/10 shadow-2xl">
            <Icon className="h-5 w-5 text-[#8c52f1]" />
          </div>

          <h3 className="mt-4 font-semibold dark:text-[#2e1b4d]">{step.title}</h3>

          <p className="mt-1 text-xs text-gray-300 dark:text-foreground/70">
            {step.description}
          </p>
        </motion.div>

        {index !== steps.length - 1 && (
          <>
            {/* Desktop connector */}
            <div className="hidden lg:block h-px w-12 dark:bg-[#381f62]/20 bg-neutral-800 mx-4" />

            {/* Mobile connector */}
            <div className="block lg:hidden h-12 w-px dark:bg-[#381f62]/20 bg-neutral-800 my-5" />
          </>
        )}
      </div>
    );
  })}

</div>
<Button 
onClick={()=>(router.push("auth/login"))}
className="mt-20 px-8 py-6 bg-amber-500 text-white font-bold rounded-full cursor-pointer">Get Started</Button>
      </div>
    </section>
  );
}