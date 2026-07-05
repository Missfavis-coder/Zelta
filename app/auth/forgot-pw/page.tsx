"use client";

import { useState } from "react";
import { Mail, Lock, EyeOff, Eye } from "lucide-react";
import { useRouter } from "next/navigation"
import Link from "next/link";



type InputChangeEvent = React.ChangeEvent<HTMLInputElement>;
export const dynamic = "force-dynamic";
export default function ForgotPasswordPage() {
  const router = useRouter();
  const [payload, setPayload] = useState({
    email: "",
    password: "",
  });

  //const { toastE, toastS } = toaster;
  const [showPassword, setShowPassword] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  function handleOnChange(e: InputChangeEvent) {
    const { name, value } = e.target;
    setPayload(prev => ({
      ...prev,
      [name]: value,
    }));
  }


  return (
    <div className="flex relative min-h-screen">

      <div className="w-full flex items-center justify-center p-6 lg:p-8 pt-24">
        <div className="w-full max-w-md relative">
          
          {/* Header */}
          <div className="mb-6 relative">
            <h1 className=" text-2xl font-bold  tracking-wider dark:text-[#160a2a]/90 text-white  mb-3 ">Forgot Password</h1>
            <p className="text-neutral-400 dark:text-foreground/70 text-sm">Enter your email address to retrieve your account.</p>
          </div>

        {/* Error Message */}
        {error && (
          <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-lg">
            <p className="text-red-600 text-sm">{error}</p>
          </div>
        )}

        {/* Sign In Form */}
          <form  className="space-y-6 mb-6" autoComplete="off">
            <div className="space-y-4">
            
              <div>
                 <div className="relative group">
                    <input
                     type="email"
                     placeholder="Enter your email"
                     className="h-12 pl-12 pr-4 w-full rounded-xl border border-neutral-900 text-white text-sm outline-none dark:border-neutral-300 dark:bg-transparent dark:focus:ring-neutral-200 dark:text-foreground focus:ring-1 focus:border-none focus:ring-[#8c52f1] transition-all duration-200 bg-neutral-800/40 "
                     autoComplete="off"
                     required
                     />
                    <Mail className="w-4 h-4 absolute left-4 top-1/2 -translate-y-1/2 text-neutral-400 group-focus-within:text-[#8c52f1] transition-colors" />
                </div>
               {/** {errors.email && (<p className="text-red-500 text sm mt-1">{errors.email.message}</p>)} */}
              </div>

            </div>



            <button
              type="submit"
              onClick={()=>{router.push("/dashboard")}}
              className="w-full h-12 flex items-center justify-center bg-[#8c52f1] hover:opacity-100 text-white font-semibold rounded-full transition-all duration-200 transform hover:scale-[1.02] active:scale-[0.98] cursor-pointer text-sm"
              disabled={isLoading}
            >
              {isLoading ? (
                <div className="flex items-center gap-2">
                  <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                  Retrieving...
                </div>
              ) : (
                "Send Email"
              )}
            </button>
          </form>



          <div className="mt-4 text-center text-sm flex items-center justify-center gap-1">
            <p className="text-neutral-400  dark:text-foreground/90">
              Remember Password?{" "}
              </p>
              <div 
              onClick={()=>{router.push("/auth/signup")}}
              className="text-neutral-300 dark:text-foreground/80 hover:text-[#8c52f1] font-semibold transition-colors cursor-pointer">
                Login
              </div>

          </div>
        </div>
      </div>

    </div>
  );
}