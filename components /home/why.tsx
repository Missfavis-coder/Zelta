'use client'

import { motion } from 'framer-motion'
import {
  Brain,
  Wallet,
  GraduationCap,
  HeartPlus
} from 'lucide-react'
import Image from 'next/image'
import { useRouter } from 'next/navigation'

const cards = [
  {
    icon: Brain,
    title: 'Think First',
    description: 'Pause. Plan. Spend.'
  },
  {
    icon: Wallet,
    title: 'Stay on Budget',
    description: 'Track where money goes.'
  },
  {
    icon: GraduationCap,
    title: 'Made for Students',
    description: 'Campus finances simplified.'
  },
  {
    icon: HeartPlus,
    title: 'Build Better Habits',
    description: 'Small decisions matter.'
  }
]

export default function WhySection() {
  const router = useRouter();
  return (
    <section className="relative overflow-hidden mt-6 border-t border-b border-white/10 bg-black dark:bg-[#8c52f1] ">
      {/* Grid Background */}
      <div
        className="
          absolute inset-0
          bg-[linear-gradient(to_right,rgba(255,255,255,0.04)_1px,transparent_1px),linear-gradient(to_bottom,rgba(255,255,255,0.04)_1px,transparent_1px)]
          bg-[size:80px_80px]
          opacity-60
        "
      />

      {/* Glow */}
      <div className="absolute left-1/2 top-0 h-[500px] w-[500px] -translate-x-1/2 rounded-full bg-[#8c52f1]/10 blur-[140px]" />

      <div className="relative z-10 lg:mx-auto lg:max-w-6xl  border-l-2 border-r-2 border-dashed  mx-4 border-neutral-800 dark:border-neutral-400 ">

      <div className='border-b border-white/10'>
      <div className="grid grid-cols-1 lg:grid-cols-4 sm:grid-cols-2">
            {cards.map((card, index) => {
              const Icon = card.icon

              return (
                <motion.div
                  key={index}
                  initial={{ opacity: 0, y: 30 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  viewport={{ once: true }}
                  transition={{
                    duration: 0.5,
                    delay: index * 0.1
                  }}
                  className="
                    group
                    relative
                   md:min-h-[160px]
                    overflow-hidden
                    sm:not-last:border-r
                    border-b
                    border-white/10
                    p-8
                  "
                >
                  {/* Hover Glow */}
                  <div
                    className="
                      absolute inset-0
                      opacity-0
                      transition-all
                      duration-500
                      group-hover:opacity-100
                    "
                  >
                    <div className="absolute inset-0 bg-gradient-to-br from-[#8c52f1]/20 via-[#8c52f1]/10 to-transparent" />
                  </div>

                  <div className="relative z-10 flex h-full flex-col items-center justify-center">
                    <div className='flex flex-col items-center justify-center'>
                      <div
                        className="
                          mb-2
                          flex h-14 w-14
                          items-center justify-center
                          
                        "
                      >
                        <Icon className="h-6 w-6 text-[#8c52f1] dark:text-white" />
                      </div>

                      <h3 className="md:text-xl text-[15px] font-bold text-white">
                        {card.title}
                      </h3>
                    </div>

                    <p className="text-sm text-gray-300 ">
                      {card.description}
                    </p>
                  </div>
                </motion.div>
              )
            })}
          </div>
      </div>            


        <div className="">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.7 }}
            className=" "
          >
            <div className='flex relative flex-col justify-center items-center mt-8 min-h-[200px]'>
            <div className="absolute left-0 -bottom-[50%]  h-[250px] w-full md:w-[400px] md:h-[220px] -z-10">
            <Image
            src={"/images/ribbon.png"}
            alt=""
            fill
            />
         </div>

              <h2 className="text-xl md:text-3xl font-semibold font-serif uppercase tracking-[0.2em] text-amber-500 text-center">
                Financial clarity
                <br />
                for students.
              </h2>

            </div>


          </motion.div>


        </div>
      </div>
    </section>
  )
}