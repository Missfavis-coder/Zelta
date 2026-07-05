// components/layout/Navbar.tsx
'use client'

import { useState, useEffect } from 'react'
import Link from 'next/link'
import { Menu, Spade, X, Moon, Sun } from 'lucide-react'
import { motion, AnimatePresence } from 'framer-motion'
import { usePathname, useRouter } from 'next/navigation'
import { useTheme } from 'next-themes'

const navLinks = [
  { name: 'What Zelta does', href: '/what-we-do' },
  { name: 'Privacy', href: '/privacy' },

]

export default function Navbar() {
  const { theme, setTheme } = useTheme();

  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false)
  const router = useRouter();
  const pathname = usePathname();
  const [navbarStyle, setNavbarStyle] = useState("default");

  // detect scroll
  const [hasScrolled, setHasScrolled] = useState(false);

   // PREVENT BODY SCROLL
   useEffect(() => {
    if (isMobileMenuOpen) {
      document.body.style.overflow = "hidden";
    } else {
      document.body.style.overflow = "auto";
    }

    return () => {
      document.body.style.overflow = "auto";
    };
  }, [isMobileMenuOpen]);

  // SCROLL DETECTION
  useEffect(() => {
    const handleScroll = () => {
      const scrollPosition = window.scrollY;

      // navbar bg after scroll
      setHasScrolled(scrollPosition > 40);

      // detect active sections
      const sections = document.querySelectorAll("[data-navbar]");

      let currentSection = "default";

      sections.forEach((section) => {
        const el = section as HTMLElement;

        const top = el.offsetTop - 150;

        if (scrollPosition >= top) {
          currentSection = el.dataset.navbar || "default";
        }
      });

      setNavbarStyle(currentSection);
    };

    handleScroll();

    window.addEventListener("scroll", handleScroll);

    return () => {
      window.removeEventListener("scroll", handleScroll);
    };
  }, []);

  // NAVBAR BACKGROUND STATES
  const navbarClasses = (() => {
    // TOP OF PAGE
    if (!hasScrolled) {
      return "bg-black/40 dark:bg-transparent backdrop-blur-3xl border border-neutral-900 dark:border-neutral-200 ";
    }

    switch (navbarStyle) {
      case "howitworks":
        return "bg-black dark:bg-white text-[#8c52f1] text-[#8c52f1]";

      default:
        return "bg-black/40 dark:bg-[#faf4fb] backdrop-blur-3xl border border-neutral-900 dark:border-neutral-200";
    }
  })();


  return (
    <>
      <motion.nav
        className={`fixed  top-6 left-6 right-6 z-50  max-w-5xl mx-auto rounded-md md:py-4 py-3.5 shadow-2xl dark:shadow-xs  ${navbarClasses}
        }`}
      >
        <div className="max-w-7xl mx-auto px-6 lg:px-8">
          <div className="flex items-center justify-between">
          <Link href={"/"} className="flex items-center gap-1 ">
                  <div className="text-[#8c52f1] ">   
                      <Spade size={21} />
                  </div>
                    <span className="text-xl font-extrabold text-[#8c52f1] ">ZELTA</span>
         </Link>

            {/* Desktop Navigation */}
            <div className="hidden md:flex items-center gap-8" >
              {navLinks.map((link) => {
                const active = pathname === link.href;

                return(
                <Link
                  key={link.name}
                  href={link.href}
                  className={`px-4 py-2 rounded-full text-sm font-semibold transition-all duration-200  ${
                    active
                      ? " text-white dark:text-black  hover:text-neutral-300"
                      : " hover:text-neutral-400  text-neutral-500 dark:text-[#160a2a]/70"
                  }`}
          
                >
                  {link.name}
                </Link>
                );
})}
            </div>

            <div className='md:flex hidden items-center gap-2'>
              <button 
               onClick={()=>{router.push("auth/login")}}
               className="px-5 py-2 hidden md:flex rounded-full bg-[#8c52f1] dark:text-white text-white text-sm transition-all duration-300 shadow-lg dark:shadow-xs  cursor-pointer font-bold">
                Get Started
              </button>
              <button
               onClick={() =>
               setTheme(theme === "dark" ? "light" : "dark")
               }
               className="rounded-lg border border-neutral-900 dark:border-neutral-300 p-2 cursor-pointer text-amber-500"
              >
                {theme === "light" ? (
                 <Sun  size={18} />
                 ) : (
                <Moon size={18} />
                )}
              </button>
            </div>


            {/* Mobile Menu Button */}
            <div className='flex items-center gap-2 md:hidden '>
            <button
             onClick={() =>
             setTheme(theme === "dark" ? "light" : "dark")
             }
             className="rounded-lg border border-neutral-900 dark:border-neutral-300 p-2 cursor-pointer dark:text-amber-500"
            >
             {theme === "dark" ? (
             <Sun  size={15} />
              ) : (
             <Moon size={15} />
             )}
           </button>
            <button
              onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
              className=" p-2 rounded-lg cursor-pointer text-white dark:text-neutral-900"
            >
              {isMobileMenuOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
            </button>

            </div>

          </div>
        </div>
      </motion.nav>

      {/* Mobile Menu */}
      <AnimatePresence>
        {isMobileMenuOpen && (
          <motion.div
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            transition={{ duration: 0.3 }}
            className="fixed inset-x-0 top-[90px] h-full z-100 bg-background md:hidden"
          >
            <div className="flex flex-col justify-center items-center p-6 gap-4 mt-6">
              {navLinks.map((link) => {
                  const active = pathname === link.href;
return(
                <Link
                  key={link.name}
                  href={link.href}
                  onClick={() => setIsMobileMenuOpen(false)}
                  className={`w-full rounded-md px-6 py-3 text-sm transition-all ${
                    active
                      ? "text-white dark:text-black  hover:text-neutral-300 dark:hover:bg-purple-500/10 hover:bg-neutral-800/40"
                      : "hover:text-white dark:text-[#160a2a]/70   text-neutral-300 hover:bg-neutral-800/40 dark:hover:bg-purple-500/10"
                  }`}
                >
                  {link.name}
                </Link>
);
})}
              <button onClick={()=>{router.push("auth/login")}} className="mt-2 px-5 py-3 rounded-full bg-gradient-to-r from-purple-500 to-purple-600 text-white font-semibold w-full cursor-pointer text-sm">
                Get Started
              </button>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </>
  )
}