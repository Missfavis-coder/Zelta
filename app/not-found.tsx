"use client";

import { ArrowLeft, MapPinHouse } from "lucide-react";
import Link from "next/link";


export default function NotFound() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-black text-white px-4 relative overflow-hidden">
      <div
        className="relative z-10"
      >
        <div
          className="flex flex-col items-center gap-6"
        >

          <div className="text-center space-y-3 mt-2">
            <h2 className="font-instrument-serif text-2xl ">
              Page not found
            </h2>
            <p className=" max-w-md mx-auto">
              The page you&apos;re looking for doesn&apos;t exist or has been
              moved.
            </p>
          </div>

          <div className="flex flex-col sm:flex-row gap-4 justify-center items-center mt-4">
            <Link
              href="/dashboard"
              className="group inline-flex items-center justify-center gap-2 px-8 py-3 bg-primary text-primary-foreground rounded-full hover:opacity-90 transition-all duration-200"
            >
              <MapPinHouse className="w-4 h-4" />
              <span className="font-semibold text-sm">Return Home</span>
            </Link>
            <button
              onClick={() => window.history.back()}
              className="group inline-flex items-center justify-center gap-2 px-8 py-3  bg-[#8c52f1] rounded-3xl cursor-pointer transition-all duration-200"
            >
              <ArrowLeft className="w-4 h-4 group-hover:-translate-x-1 transition-transform" />
              <span className="font-semibold text-sm">Go back</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
