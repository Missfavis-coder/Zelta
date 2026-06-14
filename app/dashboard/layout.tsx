

import { AppSidebar } from "@/components /layouts/dashboard/app-sidebar";
import { SiteHeader } from "@/components /layouts/dashboard/header";
import { SidebarInset, SidebarProvider } from "@/components /ui/sidebar";
import { PropsWithChildren } from "react";

export default function Page({ children }: PropsWithChildren) {

  return (

      <SidebarProvider className="">
        <AppSidebar variant="sidebar" />
        <SidebarInset className=" flex flex-col h-svh overflow-hidden">
          <SiteHeader/>
          <main className="flex-1 overflow-y-auto overflow-x-hidden">
            {children}
          </main>
        </SidebarInset>
      </SidebarProvider>

  );
}
