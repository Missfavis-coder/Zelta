"use client";

import * as React from "react";
import {
  Banknote,
  Brain,
  Briefcase,
  Home,
  Laptop,
  LayoutDashboardIcon,
  LineChart,
  MessageSquareCode,
  Shield,
  ShieldAlert,
  Spade,
  Sparkles,
  Star,
  Wallet,
  X,
  Zap,
} from "lucide-react";
import { Sidebar, SidebarContent, SidebarFooter, SidebarHeader, SidebarMenu, SidebarMenuButton, SidebarMenuItem, useSidebar } from "@/components /ui/sidebar";
import { NavMain } from "./nav-mains";
import NavSettings from "./nav-footer";
import { Button } from "@/components /ui/button";
import Link from "next/link";

// Plain, human-friendly names with the direct AI chat directory added
const baseNavMain = [
  {
    title: "Home",
    url: "/dashboard",
    icon: Home,
  },
  {
    title: "Chat with AI",
    url: "/dashboard/chat",
    icon: Sparkles,
  },
  {
    title: "What If",
    url: "/dashboard/simulations",
    icon: Laptop,
  },
  {
    title: "Gigs",
    url: "/dashboard/gigs",
    icon: Briefcase,
  },
  {
    title: "My Savings",
    url: "/dashboard/vaults",
    icon: Wallet,
  },
];

const adminNavItem = {
  title: "Admin",
  url: "/dashboard/admin",
  icon: Shield,
};

export function AppSidebar({ ...props }: React.ComponentProps<typeof Sidebar>) {
  const { state, isMobile, setOpenMobile } = useSidebar();
  const isCollapsed = state === "collapsed";

  return (
    <Sidebar
      className="border-r border-neutral-900 dark:border-neutral-200   overflow-hidden fixed  "
      collapsible="icon"
      {...props}
    >
      <div
        className="absolute inset-0 w-full h-full mix-blend-overlay pointer-events-none opacity-[0.05]"
        style={{
          backgroundImage: "url(/images/backgrounds/noise.svg)",
          backgroundSize: "200px 200px",
        }}
      />
      <SidebarHeader className="relative z-10  px-3">
        <div className="flex items-center justify-between">
          <SidebarMenu className="flex-1 ">
            <SidebarMenuItem className="flex items-center py-2 justify-center">
              <SidebarMenuButton className=" " asChild>
                <div className="flex items-center gap-1 cursor-pointer">
                  {/* ICON CHANGES WHEN COLLAPSED */}
                  <div className="text-[#8c52f1] ">
                    {isCollapsed ? (
                      <Spade size={21} />
                    ) : (
                      <Spade size={21} />
                    )}
                  </div>

                  {/* TEXT ONLY WHEN EXPANDED */}
                  {!isCollapsed && (
                    <Link href="/" className="text-xl font-extrabold text-[#8c52f1] ">ZELTA</Link>
                  )}
                </div>
              </SidebarMenuButton>
            </SidebarMenuItem>
          </SidebarMenu>
          {isMobile && (
            <Button
              variant="ghost"
              size="icon"
              className="h-8 w-8 text-white hover:bg-sidebar-accent hover:text-white cursor-pointer"
              onClick={() => setOpenMobile(false)}
            >
              <X className="h-6 w-6" />
              <span className="sr-only">Close sidebar</span>
            </Button>
          )}
        </div>
      </SidebarHeader>
      
      <SidebarContent className="relative z-10 px-2 mt-4">
        <NavMain items={baseNavMain} />
      </SidebarContent>

      <SidebarFooter className="relative z-10 p-4">
        <NavSettings />
      </SidebarFooter>
    </Sidebar>
  );
}
