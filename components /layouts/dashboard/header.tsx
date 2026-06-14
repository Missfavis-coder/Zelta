"use client";

import { usePathname } from "next/navigation";
import { LogOut, Settings, Bell } from "lucide-react";
import Link from "next/link";
import { Button } from "@/components /ui/button";
import { SidebarTrigger } from "@/components /ui/sidebar";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuGroup,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components /ui/dropdown-menu";
import { Avatar, AvatarFallback } from "@/components /ui/avatar";

/* ---------------- PAGE META ---------------- */
const pageMeta: Record<string, { title: string; description: string }> = {
  dashboard: {
    title: "Dashboard",
    description: "Your AI overview of student survival status in Lagos",
  },
  chat: {
    title: "Chat with AI",
    description: "Let Zelta AI help you make financial decisions",
  },
  simulations: {
    title: "What If",
    description: "See how a financial decision affects your future before you make it.",
  },
  gigs: {
    title: "Gigs",
    description: "Need extra cash? No panic.",
  },
  vaults: {
    title: "My Savings",
    description: "Build a cushion for emergencies, goals, and unexpected expenses.",
  },
  notification: {
    title: "Notifications",
    description: "Updates from your AI survival system",
  },
};

/* ---------------- HEADER ---------------- */

function HeaderSkeleton() {
  return (
    <header className="sticky top-0 z-50 flex h-14 items-center border-b bg-background px-4 lg:px-6">
      <div className="flex w-full items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="h-6 w-6 bg-neutral-200/10 rounded animate-pulse" />
          <div className="h-4 w-24 bg-neutral-200/10 rounded animate-pulse" />
        </div>

        <div className="flex items-center gap-4">
          <div className="h-8 w-8 bg-neutral-200/10 rounded-full animate-pulse" />
          <div className="h-8 w-8 bg-neutral-200/10 rounded-full animate-pulse" />
        </div>
      </div>
    </header>
  );
}

export function SiteHeader() {
  const path = usePathname();

  const lastSegment =
    path.split("/").filter(Boolean).pop() || "dashboard";

  const meta = pageMeta[lastSegment];

  return (
    <header className=" top-0 z-50 flex md:pt-3.5 pt-3 items-center px-4 lg:px-6 pb-2">
      <div className="flex w-full items-center justify-between">

        {/* LEFT */}
        <div className="flex items-center gap-3">
          <SidebarTrigger className="-ml-1 md:hidden text-white hover:bg-purple-700 flex cursor-pointer bg-purple-600" />

          <div className="flex flex-col leading-tight">
            <h1 className="md:text-[20px] text-[16px] font-semibold text-foreground">
              {meta?.title || "Dashboard"}
            </h1>

            <p className="md:text-sm text-xs tracking-wider text-neutral-400">
              {meta?.description}
            </p>
          </div>
        </div>

        {/* RIGHT */}
        <div className="flex items-center gap-4">

          {/* NOTIFICATION */}
          <Link href="#">
            <Button variant="ghost" className="relative h-8 w-8 rounded-full hover:bg-neutral-800/30 cursor-pointer">
              <Bell className="h-5 w-5 text-white" />

              <span className="absolute -top-1 -right-1 flex h-5 min-w-5 items-center justify-center rounded-full bg-red-500 px-1 text-[10px] font-semibold text-white">
                1
              </span>
            </Button>
          </Link>

          {/* USER MENU */}
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button variant="ghost" className="h-8 w-8 rounded-full cursor-pointer">
                <Avatar className="h-8 w-8">
                  <AvatarFallback className="text-xs font-semibold">
                    OA
                  </AvatarFallback>
                </Avatar>
              </Button>
            </DropdownMenuTrigger>

            <DropdownMenuContent className="w-56" align="end">
              <DropdownMenuLabel>
                <p className="text-xs font-medium uppercase">Ojo Adeshola</p>
              </DropdownMenuLabel>

              <DropdownMenuSeparator />

              <DropdownMenuGroup>
                <DropdownMenuItem asChild>
                  <Link href="/dashboard/settings">
                    <Settings className="mr-2 h-4 w-4 cursor-pointer" />
                    Settings
                  </Link>
                </DropdownMenuItem>
              </DropdownMenuGroup>

              <DropdownMenuSeparator />

              <DropdownMenuItem className="text-red-400 cursor-pointer">
                <LogOut className="mr-2 h-4 w-4" />
                Log out
              </DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>

        </div>
      </div>
    </header>
  );
}