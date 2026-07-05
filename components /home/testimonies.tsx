"use client";

import { motion } from "framer-motion";
import { Quote } from "lucide-react";

const testimonials = [
  {
    quote:
      "I didn't realize I was spending over ₦40k monthly on snacks until ZELTA pointed it out.",
    name: "Computer Engineering Student",
  },
  {
    quote:
      "The budgeting suggestions actually fit my allowance instead of giving unrealistic advice.",
    name: "200 Level Student",
  },
  {
    quote:
      "I asked where my money was going and got a breakdown in seconds. That was impressive.",
    name: "Law Student",
  },
];

export default function Testimonies() {
  return (
    <section className="md:px-6 px-3 pt-20 pb-10">
      <div className="mx-auto max-w-6xl">
        {/* Heading */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          viewport={{ once: true }}
          className="mx-auto max-w-2xl text-center"
        >
          <h2 className="text-2xl md:text-3xl font-semibold dark:text-[#160a2a]">
            Loved by <span className="text-[#8c52f1]  font-serif tracking-wider">Most</span> Students.
          </h2>

          <p className="mt-3 text-sm text-gray-300 dark:text-foreground/70">
             See what our users are saying about Zelta AI
          </p>
        </motion.div>

        {/* Cards */}
        <div className="mt-14 grid gap-6 md:grid-cols-3">
          {testimonials.map((item, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, y: 25 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{
                duration: 0.45,
                delay: index * 0.15,
              }}
              viewport={{ once: true }}
              className="rounded-2xl border border-neutral-900 dark:border-neutral-200 p-6"
            >
              <Quote className="h-5 w-5 text-amber-500" />

              <p className="mt-4 text-sm leading-7 text-gray-300 dark:text-foreground/80">
                "{item.quote}"
              </p>

              <div className="mt-6 border-t border-neutral-900 dark:border-neutral-200 pt-4">
                <p className="text-sm font-medium dark:text-[#160a2a]">{item.name}</p>
              </div>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}