'use client'

import { AnimatePresence, motion } from "framer-motion";
import { useState, useEffect, useRef } from "react";
import { Button } from '../ui/button';
import { ArrowRight, ChevronLeft, ChevronRight } from 'lucide-react';
import Image from "next/image";

export default function Demo() {
  const [currentSlide, setCurrentSlide] = useState(0);
  const slides = [1, 2];

  const timerRef = useRef<NodeJS.Timeout | null>(null);
  
  const nextSlide = () => {
    setCurrentSlide((prev) => (prev + 1) % slides.length);
  };
  
  const prevSlide = () => {
    setCurrentSlide((prev) => (prev - 1 + slides.length) % slides.length);
  };

  useEffect(() => {
    timerRef.current = setInterval(() => {
      setCurrentSlide((prev) => (prev + 1) % slides.length);
    }, 6000); // every 6 seconds
  
    return () => {
      if (timerRef.current) clearInterval(timerRef.current);
    };
  }, []);

  const restartTimer = () => {
    if (timerRef.current) clearInterval(timerRef.current);
  
    timerRef.current = setInterval(() => {
      setCurrentSlide((prev) => (prev + 1) % slides.length);
    }, 6000);
  };
  
  const handleNext = () => {
    nextSlide();
    restartTimer();
  };
  
  const handlePrev = () => {
    prevSlide();
    restartTimer();
  };


  return (
    <section data-navbar="howitworks" className="relative text-white pb-20 px-4 py-28 ">


      {/* HERO */}
      <div className='mx-auto max-w-7xl'>

      <div className="relative flex items-center gap-4 md:gap-10 justify-center md:max-w-4xl mx-auto min-h-[400px] px-6 pt-12 pb-24 text-center bg-[#8c52f1] backdrop-blur-xl shadow-2xl dark:shadow-none rounded-md z-20" >
        <div onClick={handlePrev} className='md:flex hidden items-center justify-center shadow-2xl bg-amber-500 p-2 rounded-full mt-4 cursor-pointer'><ChevronLeft/></div>

        <div className="relative w-full ">  


    <AnimatePresence mode="wait">

    {currentSlide === 0 ? (

        <motion.div
            key="slide1"
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -30 }}
            transition={{ duration: .45 }}
            className=""
        >

            <p className="text-amber-400 text-sm font-semibold">
                Chat with ZELTA
            </p>

            <h1 className="mt-6 text-[16px] md:text-2xl font-semibold  mx-auto leading-tight">
                Your next financial
                decision shouldn't

                be a guess.
            </h1>

            <div className="flex justify-center mt-12">
                <Button className="bg-white text-[#8c52f1] rounded-full px-8 py-6 md:px-10 md:py-8 font-bold cursor-pointer">
                    Get Started
                    <ArrowRight />
                </Button>
            </div>
          <div className="absolute -bottom-[40%] right-0 h-[100px] w-[100px] md:h-[150px] md:w-[150px]  animate-pulse">
            <Image
            src={"/images/think-emoji.png"}
            alt=""
            fill
            />
          </div>
        </motion.div>

    ) : (

        <motion.div
            key="slide2"
            initial={{ opacity: 0, x: 80 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -80 }}
            transition={{ duration: .45 }}
            className="overflow-x-hidden scrollbar-hide "
        >

            <p className="text-amber-400 text-sm font-semibold mb-6">
                Makes you make better financial choice and recommend gigs when necessary.
            </p>

            <div className="space-y-4 text-left">

                <motion.div
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: .1 }}
                    className=""
                >
                    <p className="mt-6 text-[16px] md:text-2xl font-semibold  mx-auto leading-tight text-center">
                      Most times, Student are caught up lamenting 
                       " Omo... I don broke 😭
                        Allowance don finish and month never end."
                    </p>
                </motion.div>

            </div>

            <div className="flex justify-center mt-12">
                <Button className="bg-white text-[#8c52f1] rounded-full px-8 py-6 md:px-10 md:py-8 font-bold cursor-pointer">
                    Get Started
                    <ArrowRight />
                </Button>
            </div>

            <div className="absolute -bottom-[30%] md:-left-[10%] left-0 h-[100px] w-[100px] md:h-[150px] md:w-[150px]  animate-pulse">
            <Image
            src={"/images/cry-emoji.png"}
            alt=""
            fill
            />
          </div>
        </motion.div>

    )}

</AnimatePresence>

       </div>

        <div onClick={handleNext} className='md:flex hidden items-center justify-center shadow-2xl bg-amber-500 p-2 rounded-full mt-4 cursor-pointer'><ChevronRight/></div>

      </div>

      </div>


    </section>
  )
}
