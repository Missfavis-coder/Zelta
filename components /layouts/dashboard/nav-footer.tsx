"use client";

import { Button } from "@/components /ui/button";
import { Card } from "@/components /ui/card";
import { useSidebar } from "@/components /ui/sidebar";
import { LogOut } from "lucide-react";


const NavSettings = () => {
  const { state } = useSidebar();

  if (state === "collapsed") {
    return (
      <div className="flex flex-col items-center gap-3 p-2">
        <div className="w-9 h-9 rounded-full bg-white/10 flex items-center justify-center text-sm font-medium">
OA
        </div>
      </div>
    );
  }

  return (
    <Card className="w-full p-4 bg-[#8c52f1] text-white ">

      <div className="space-y-1">
        <h1 className="font-bold text-sm">
Ojo Adeshola
        </h1>
        <p className="text-xs font-semibold tracking-wide">
ofavourmi55@gmail.com
        </p>
      </div>


      <div className=" border-t border-white/10">
        <Button

          variant="ghost"
          className="w-full font-bold justify-start cursor-pointer gap-2 text-[#8c52f1] hover:text-purple-800 dark:hover:bg-white bg-white"
        >
          <LogOut size={16} />
Logout
        </Button>
      </div>
    </Card>
  );
};

export default NavSettings;