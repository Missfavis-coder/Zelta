
'use client'

import { motion } from 'framer-motion'
import Link from 'next/link'
import { ArrowRight } from 'lucide-react'

export default function Footer() {
  return (
<footer className="relative overflow-hidden border-t border-white/10">
  {/* bg image */}
  <div
    className="absolute inset-0 bg-cover bg-center"
    style={{
      backgroundImage: "url('/images/footer-bg.jpg')",
    }}
  />



  <div className="relative z-10">
    {/* Huge Brand */}
    <div className="px-6 pt-24 md:px-12">
      <h2
        className="
        text-[22vw]
        font-black
        leading-none
        tracking-[-0.08em]
        text-white/10
        dark:text-[#8c52f1]/10
        select-none
        absolute
        left-[20%]
        top-[40%]
      "
      >
        ZELTA
      </h2>
    </div>

    {/* Footer Content */}
    <div className="mx-auto max-w-7xl px-6 pb-10 md:px-12">
      <div className="flex flex-col gap-12 md:flex-row md:justify-between">
        {/* Left */}
        <div className="max-w-md">
          <h3 className="text-xl font-bold text-white dark:text-[#1e0d3a]">
            Financial clarity
            for students.
          </h3>

          <p className="mt-4 text-sm text-neutral-400 dark:text-foreground/70">
            Helping students spend smarter,
            save better and reduce money stress.
          </p>
        </div>

        {/* Right */}
        <div className="flex gap-10 dark:text-[#160a2a]">
          <a
            href="#"
            className="text-neutral-400 hover:text-white  dark:text-foreground/70"
          >
            X
          </a>

          <a
            href="#"
            className="text-neutral-400 hover:text-white dark:text-foreground/70"
          >
            Instagram
          </a>

          <a
            href="#"
            className="text-neutral-400 hover:text-white dark:text-foreground/70"
          >
            LinkedIn
          </a>

          <a
            href="#"
            className="text-neutral-400 hover:text-white dark:text-foreground/70"
          >
            Contact
          </a>
        </div>
      </div>

      <div className="mt-20 flex items-center justify-between border-t dark:border-neutral-300 border-white/10 pt-6">
        <span className="text-xs text-neutral-500 dark:text-[#1e0d3a] ">
          © 2026 ZELTA
        </span>

        <span className="text-xs text-neutral-500 dark:text-[#1e0d3a]">
          Built for students.
        </span>
      </div>
    </div>
  </div>
</footer>
  )
}

