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
            <h1 className=" text-2xl font-bold dark:text-[#160a2a]/90 text-white mb-2">Signup.</h1>
            <p className="text-neutral-400 dark:text-foreground/70 text-sm">Create your account to access our seamless services.</p>

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
                    className="h-12 pl-12 pr-4 w-full rounded-xl border border-neutral-900 text-white text-sm outline-none focus:ring-1 focus:border-none focus:ring-[#8c52f1] transition-all duration-200 bg-neutral-800/40 dark:border-neutral-200 dark:bg-transparent dark:focus:ring-neutral-200 dark:text-foreground "
                    maxLength={30}
                    autoComplete="off"
                    required
                  />
                  <User className="w-4 h-4 absolute left-4 top-1/2 -translate-y-1/2 text-neutral-400 dark:text-neutral-300 dark:group-focus-within:text-[#8c52f1] group-focus-within:text-[#8c52f1] transition-colors" />
                </div>
             </div>
             {/**Last name */}
             <div> 
                <div className="relative group">
                  <input
                    placeholder="Last name"
                    className="h-12 pl-12 pr-4 w-full rounded-xl border border-neutral-900 text-white text-sm outline-none focus:ring-1 focus:border-none focus:ring-[#8c52f1] transition-all duration-200 bg-neutral-800/40 dark:border-neutral-200 dark:bg-transparent dark:focus:ring-neutral-200 dark:text-foreground "
                    maxLength={30}
                    autoComplete="off"
                    required
                    
                  />
                  <User className="w-4 h-4 absolute left-4 top-1/2 -translate-y-1/2 text-neutral-400 dark:text-neutral-300 dark:group-focus-within:text-[#8c52f1] group-focus-within:text-[#8c52f1] transition-colors" />
                </div>

              </div>
              {/**Email */}
              <div> 
              <div className="relative group">
                <input
                  type="email"
                  placeholder="Enter your email"
                  className="h-12 pl-12 pr-4 w-full rounded-xl border border-neutral-900 text-white text-sm outline-none focus:ring-1 focus:border-none focus:ring-[#8c52f1] transition-all duration-200 bg-neutral-800/40 dark:border-neutral-200 dark:bg-transparent dark:focus:ring-neutral-200 dark:text-foreground "
                  autoComplete="off"
                  required
                  
                />
                <Mail className="w-4 h-4 absolute left-4 top-1/2 -translate-y-1/2 text-neutral-400 dark:text-neutral-300 dark:group-focus-within:text-[#8c52f1] group-focus-within:text-[#8c52f1] transition-colors" />
              </div>

              </div>

              {/**password */}
              <div>
              <div className="relative group">
                <input
                  type={showPassword ? "text" : "password"}
                  placeholder="Create a password"
                  className="h-12 pl-12 pr-4 w-full rounded-xl border border-neutral-900 text-white text-sm outline-none focus:ring-1 focus:border-none focus:ring-[#8c52f1] transition-all duration-200 bg-neutral-800/40 dark:border-neutral-200 dark:bg-transparent dark:focus:ring-neutral-200 dark:text-foreground "
                  autoComplete="new-password"
                  required
                  
                />
                <Lock className="w-4 h-4 absolute left-4 top-1/2 -translate-y-1/2 text-neutral-400 dark:text-neutral-300 dark:group-focus-within:text-[#8c52f1] group-focus-within:text-[#8c52f1] transition-colors" />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute right-4 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600 transition-colors"
                >
                  {showPassword ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                </button>
              </div>

              </div>

             
            <div className="flex items-start space-x-2 text-sm">
              <input type="checkbox" className="w-4 h-4 mt-0.5 accent-foreground"  />
              <span className="text-neutral-300 dark:text-foreground ">
                I agree to the{" "}
                <span className="text-neutral-500 dark:text-foreground/70 hover:text-[#8c52f1]/30 font-medium cursor-pointer">
                  Terms of Service
                </span>
                {" "}and{" "}
                <Link href="/privacy" className="text-neutral-500 dark:text-foreground/70 hover:text-[#8c52f1] font-medium">
                  Privacy Policy
                </Link>
              </span>
            </div>

            <button
              type="submit"
              className="w-full h-12 flex items-center justify-center bg-[#8c52f1]  hover:opacity-90 text-white font-semibold rounded-full transition-all duration-200 transform hover:scale-[1.02] active:scale-[0.98] cursor-pointer"
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

          <div className="mt-4 text-sm text-center flex items-center justify-center gap-1">
            <p className="text-neutral-400 dark:text-foreground/70">
              Already have an account?{" "}
            </p>
              <div onClick={()=>{router.push("login")}} className="text-neutral-500 dark:text-foreground hover:text-[#8c52f1] font-semibold transition-colors cursor-pointer">
                Login
              </div>
           
          </div>
        </div>
      </div>
    </div>
  );
}