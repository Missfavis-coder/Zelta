"use client";

import { motion } from "framer-motion";
import Image from "next/image";

const BRANDS = [
  
  "/logo/openai.png",
  "/logo/goggle-logo.png",
  "/logo/gemi.png",
];

export default function Companies() {
  return (
    <section className="px-6 py-20">
      <div className="mx-auto max-w-6xl">
        {/* Heading */}
        <motion.div
          initial={{ opacity: 0, y: 40 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.7 }}
          viewport={{ once: true }}
          className="mx-auto max-w-3xl text-center"
        >
          <h2 className="text-xl md:text-3xl font-semibold tracking-tight dark:text-neutral-900">
            Powered by trusted technology
          </h2>

        </motion.div>

        {/* Logos */}
        <motion.div
          initial={{ opacity: 0 }}
          whileInView={{ opacity: 1 }}
          transition={{ delay: 0.2 }}
          viewport={{ once: true }}
          className="mt-4 flex flex-wrap items-center  justify-center gap-4"
        >
          {BRANDS.map((logo, index) => (
            <div
              key={index}
              className="relative md:h-[100px] md:w-[180px] h-[90px] w-[100px]  "
            >
              <Image
                src={logo}
                alt="Partner logo"
                fill
                className="object-contain"
              />
            </div>
          ))}
        </motion.div>
      </div>
    </section>
  );
}