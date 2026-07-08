// components/home/HeroSection.tsx
'use client'

import { motion } from 'framer-motion'
import { ArrowRight, Shield, Brain, Clock, HeartPlus } from 'lucide-react'
import Image from 'next/image'

export default function HeroSection() {
  return (
    <section className="relative max-w-7xl mx-auto  flex items-center justify-center overflow-hidden lg:pt-28 pt-25 ">
      {/* Background Glow */}
      <div className="absolute inset-0 hero-glow pointer-events-none" />
      
      <div className=" px-4 md:px-6 lg:px-4 py-20 relative z-10">
        <div className="">
        
          <div
          className='flex flex-col justify-center items-center w-full'
          >
            <motion.div
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: 0.1, duration: 0.2 }}
              className="inline-flex items-center gap-2 py-1 rounded-full glass mb-6"
            >
              <HeartPlus className="w-4 h-4 text-[#8c52f1]" />
              <span className="text-xs text-gray-300  tracking-wide dark:text-foreground/70">AI-Powered Financial Companion</span>
            </motion.div>
            
            <motion.h1
              initial={{ opacity: 0, x: 0 }}
              animate={{ opacity: 1, x: 4 }}
              transition={{ delay: 0.1, duration: 0.3 }}
              className="text-2xl lg:text-4xl md:text-3xl text-center font-bold tracking-tight mb-6 dark:text-[#160a2a]/90"
            >
              Before You Spend,<br className='md:flex hidden' />{' '}
              <span className="text-gradient">Ask <span className='font-serif tracking-wider text-amber-500'> Zelta. </span></span>
            </motion.h1>
            
            <motion.p
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.2, duration: 0.4 }}
              className="md:text-[15px] text-[14px] tracking-wide  dark:text-foreground/90 leading-6 text-gray-300 mb-8 max-w-lg text-center "
              
            >
              An AI financial survival system helping students make smarter money decisions, 
              protect their cash, and stay financially secure throughout university.
            </motion.p>

   <div className='w-full '>      
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.5, duration: 0.6 }}
              className="flex flex-col sm:flex-row justify-center gap-4 mt-2  "
            >
              <button className="group px-8 py-4 rounded-full cursor-pointer bg-[#8c52f1] text-white font-semibold md:text-[16px] text-sm transition-all duration-300 shadow-lg dark:shadow-xs shadow-purple-500/25 flex items-center justify-center gap-2 ">
                Get Started
                <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
              </button>
              <button className="px-10 py-4 rounded-full cursor-pointer dark:text-[#8c52f1] text-white font-semibold md:text-[16px] text-sm shadow-2xl dark:shadow-none dark:bg-transparent dark:border dark:border-[#8c52f1]/40 bg-neutral-800/40 transition-all duration-300">
                Watch Demo
              </button>
            </motion.div>
   </div>         
          </div>
        </div>
      </div>
      

    </section>
  )
}