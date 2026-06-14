"use client";

import { useState } from "react";
import { Mail, Lock, User, Eye, EyeOff } from "lucide-react";
import { useRouter } from "next/navigation";
import Link from "next/link";

type InputChangeEvent = React.ChangeEvent<HTMLInputElement>;



export default function SignupPage() {

  const router = useRouter();
  const [payload, setPayload] = useState({
    firstName: "",
    lastName: "",
    email: "",
    password: "",
    confirmPassword: "",
  });

  //const { error, setError } = useState();
  const [isLoading, setIsLoading] = useState(false);
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState<string | null>(null);



  return (
    <div className="flex min-h-screen">
      <div className="w-full flex flex-col items-center justify-center p-6 lg:p-8 pt-24 lg:mt-2 mt-0">
      
        <div className="w-full max-w-md ">
          
          {/* Header */}
          <div className="mb-10 relative">
            <h1 className=" text-2xl font-bold tracking-widest text-neutral-900 dark:text-white mb-2">Signup.</h1>
            <p className="text-neutral-600 dark:text-neutral-400 text-sm">Create your account to access our seamless services.</p>

          </div>

          {/* Error Message */}
          {error && (
            <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-lg">
              <p className="text-red-600 text-sm">{error}</p>
            </div>
          )}

          {/* Sign Up Form */}
          <form className="space-y-6 mb-8" autoComplete="off">
            <div className="space-y-4 text-[14px]">

              {/**First name */}
              <div>
                <div className="relative group">
                  <input
                    type="text"

                    placeholder="First name"
                    className="h-12 pl-12 pr-4 w-full rounded-xl border border-gray-300 dark:border-neutral-700 text-neutral-500 dark:text-white text-sm outline-none focus:ring-1 focus:border-none focus:ring-cyan-500 transition-all duration-200 bg-white/10 "
                    maxLength={30}
                    autoComplete="off"
                    required
                  />
                  <User className="w-4 h-4 absolute left-4 top-1/2 -translate-y-1/2 text-neutral-400 group-focus-within:text-cyan-500 transition-colors" />
                </div>
                {/**{errors.first_name && (
                   <p className="text-red-500 text-sm">{errors.first_name.message}</p>
                )}*/}
             </div>
             {/**Last name */}
             <div> 
                <div className="relative group">
                  <input
                    placeholder="Last name"
                    className="h-12 pl-12 pr-4 w-full rounded-xl border border-gray-300 dark:border-neutral-700 text-neutral-500 dark:text-white text-sm outline-none focus:ring-1 focus:border-none focus:ring-cyan-500 transition-all duration-200 bg-white/10"
                    maxLength={30}
                    autoComplete="off"
                    required
                    
                  />
                  <User className="w-4 h-4 absolute left-4 top-1/2 -translate-y-1/2 text-neutral-400 group-focus-within:text-cyan-500 transition-colors" />
                </div>
                {/**{errors.last_name && (
                   <p className="text-red-500 text-sm">{errors.last_name.message}</p>
                )}*/}
              </div>
              {/**Email */}
              <div> 
              <div className="relative group">
                <input
                  type="email"
                  placeholder="Enter your email"
                  className="h-12 pl-12 pr-4 w-full rounded-xl border border-gray-300 text-neutral-500 dark:border-neutral-700 dark:text-white text-sm outline-none focus:ring-1 focus:border-none focus:ring-cyan-500 transition-all duration-200 bg-white/10"
                  autoComplete="off"
                  required
                  
                />
                <Mail className="w-4 h-4 absolute left-4 top-1/2 -translate-y-1/2 text-neutral-400 group-focus-within:text-cyan-500 transition-colors" />
              </div>
              {/**{errors.email && (
                <p className="text-red-500 text-sm">{errors.email.message}</p>
                )}*/}
              </div>

              {/**password */}
              <div>
              <div className="relative group">
                <input
                  type={showPassword ? "text" : "password"}
                  placeholder="Create a password"
                  className="h-12 pl-12 pr-4 w-full rounded-xl border border-gray-300 dark:border-neutral-700 text-neutral-500 dark:text-white text-sm outline-none focus:ring-1 focus:border-none focus:ring-cyan-500 transition-all duration-200 bg-white/10"
                  autoComplete="new-password"
                  required
                  
                />
                <Lock className="w-4 h-4 absolute left-4 top-1/2 -translate-y-1/2 text-neutral-400 group-focus-within:text-cyan-500 transition-colors" />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute right-4 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600 transition-colors"
                >
                  {showPassword ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                </button>
              </div>
              {/**{errors.password && (
                <p className="text-red-500 text-sm">{errors.password.message}</p>
                )}**/}
              </div>

             
            <div className="flex items-start space-x-2 text-sm">
              <input type="checkbox" className="w-4 h-4 mt-0.5"  />
              <span className="text-gray-600 dark:text-neutral-400">
                I agree to the{" "}
                <span className="text-neutral-900 dark:text-white hover:text-yellow-700 font-medium">
                  Terms of Service
                </span>
                {" "}and{" "}
                <Link href="/privacy" className="text-neutral-900 dark:text-white hover:text-yellow-700 font-medium">
                  Privacy Policy
                </Link>
              </span>
            </div>

            <button
              type="submit"
              className="w-full h-12 flex items-center justify-center bg-gradient-to-r from-cyan-500 to-slate-800 hover:opacity-90 text-white font-semibold rounded-full transition-all duration-200 transform hover:scale-[1.02] active:scale-[0.98] cursor-pointer"
              disabled={isLoading}
              onClick={()=>{router.push("about-you")}}
            >
              {isLoading ? (
                <div className="flex items-center gap-2">
                  <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                  Creating account...
                </div>
              ) : (
                <div>Create Account</div>
                
              )}
            </button>
          </div>
          </form>

          <div className="mt-4 text-sm text-center">
            <p className="text-gray-600 dark:text-neutral-400">
              Already have an account?{" "}
              <Link href="/login" className="text-neutral-800 hover:text-neutral-600/90 dark:text-white font-semibold transition-colors">
                Login
              </Link>
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}