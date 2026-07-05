'use client'

import { motion } from 'framer-motion'
import {
  Sparkles,
  ArrowRight,
  MapPin,
  Clock,
  Briefcase,
  Calendar,
  ChevronRight
} from 'lucide-react'

export default function GigsPage() {
  return (
    <main className="min-h-screen text-white">

      <section className="relative z-10 max-w-7xl mx-auto px-4 md:px-6 lg:px-8 py-8">

        {/* Hero */}
        <motion.div
          initial={{ opacity: 0, y: 15 }}
          animate={{ opacity: 1, y: 0 }}
          className="max-w-4xl"
        >

          <h1 className="md:text-2xl text-xl dark:text-[#160a2a]/90 font-semibold leading-tight">
            12 gigs fit your
            schedule this week.
          </h1>

          <p className="text-neutral-400 dark:text-foreground/70 mt-2 max-w-xl text-sm">
            Based on your availability, location and earning goals,
            we've selected opportunities that actually fit your life.
          </p>
        </motion.div>

        {/* Featured Recommendation */}
        <motion.div
          initial={{ opacity: 0, y: 25 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: .1 }}
          className="
            mt-10
            rounded-md
            bg-neutral-900/40
            dark:bg-neutral-300/20
            overflow-hidden
          "
        >
          <div className="grid lg:grid-cols-2">
            {/* Left */}
            <div className="p-4 md:p-8">
              <div className="inline-flex items-center gap-2 text-amber-500 text-sm">
                <Sparkles className="w-4 h-4" />
                Best Match
              </div>

              <h2 className="md:text-2xl dark:text-[#160a2a]/80 text-xl font-bold mt-4">
                Campus Event Staff
              </h2>

              <p className="text-neutral-400 dark:text-foreground/70 mt-3 md:text-[15px] text-sm">
                Flexible weekend work with high earning potential
                and walking distance from campus.
              </p>

              <div className="grid grid-cols-3 gap-4 mt-6">
                <div>
                  <p className="text-neutral-500 dark:text-foreground/90 text-sm">
                    Pay
                  </p>

                  <p className="font-medium dark:text-[#160a2a]/90 mt-1">
                    ₦15,000
                  </p>
                </div>

                <div>
                  <p className="text-neutral-500 dark:text-foreground/90 text-sm">
                    Hours
                  </p>

                  <p className="font-medium dark:text-[#160a2a]/90 mt-1">
                    6 hrs
                  </p>
                </div>

                <div>
                  <p className="text-neutral-500 dark:text-foreground/90 text-sm">
                    Distance
                  </p>

                  <p className="font-medium dark:text-[#160a2a]/90 mt-1">
                    1.2km
                  </p>
                </div>
              </div>

              <button className="mt-10 px-6 py-3 rounded-full cursor-pointer bg-[#8c52f1] text-white font-semibold flex items-center gap-2">
                View Gig
                <ArrowRight className="w-4 h-4" />
              </button>
            </div>

            {/* Right Mockup */}
            <div className=" bg-gradient-to-br from-white/[0.04] to-transparent dark:bg-neutral-300/40 p-4 md:p-8">
              <div className="rounded-3xl bg-black/50 dark:bg-neutral-300/30 p-6">
                <div className="flex justify-between">
                  <span className="text-sm text-[#8c52f1] font-semibold">
                    Match Score
                  </span>

                  <span className="text-amber-500 font-medium">
                    92%
                  </span>
                </div>

                <div className="mt-8 space-y-5">
                  <div className="flex items-center gap-3">
                    <MapPin className="w-4 h-4 text-[#8c52f1] dark:text-foreground" />
                    <span className="text-sm dark:text-foreground/70">
                      Walking distance from campus
                    </span>
                  </div>

                  <div className="flex items-center gap-3">
                    <Clock className="w-4 h-4 text-[#8c52f1] dark:text-foreground" />
                    <span className="text-sm dark:text-foreground/70">
                      Fits weekend schedule
                    </span>
                  </div>

                  <div className="flex items-center gap-3">
                    <Briefcase className="w-4 h-4 text-[#8c52f1] dark:text-foreground" />
                    <span className="text-sm dark:text-foreground/70">
                      No prior experience required
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </motion.div>

        {/* Nearby */}
        <div className="mt-12">
          <div className="flex items-center justify-between">
            <h3 className="md:text-xl text-[18px] font-semibold dark:text-[#160a2a]/90">
              Nearby Opportunities
            </h3>

            <button className="flex items-center gap-2 text-sm text-neutral-400 cursor-pointer dark:text-black">
              View all
              <ChevronRight className="w-4 h-4" />
            </button>
          </div>

          <div className="flex gap-5 overflow-x-auto scrollbar-hide mt-4 pb-2">
            {[
              'Cafe Assistant',
              'Retail Helper',
              'Library Assistant',
              'Campus Ambassador'
            ].map((job) => (
              <div
                key={job}
                className="
                  min-w-[260px]
                  rounded-md
                  bg-white/[0.04]
                  dark:bg-neutral-300/20
                  p-4
                "
              >
                <p className="md:text-lg text-[16px] font-medium  dark:text-foreground/80">
                  {job}
                </p>

                <p className="text-neutral-500 dark:text-foreground/70 text-sm ">
                  800m away
                </p>

                <p className=" text-[#8c52f1] dark:text-[#160a2a]/90 text-sm">
                  ₦12,000/day
                </p>
              </div>
            ))}
          </div>
        </div>


      </section>
    </main>
  )
}