"use client";

import { type LucideIcon } from "lucide-react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import clsx from "clsx";
import { SidebarGroup, SidebarGroupContent, SidebarMenu, SidebarMenuButton, SidebarMenuItem, useSidebar } from "@/components /ui/sidebar";


export function NavMain({
  items,
}: {
  items: {
    title: string;
    url: string;
    icon?: LucideIcon;
  }[];
}) {
  const pathname = usePathname();
  const { state, isMobile, setOpenMobile } = useSidebar();

  const isCollapsed = state === "collapsed";
  const handleLinkClick = () => {
    if (isMobile) {
      setOpenMobile(false);
    }
  };

  return (
    <SidebarGroup>
      <SidebarGroupContent className="flex flex-col gap-2">
        <SidebarMenu>
          {items.map((item) => {
            const isActive = pathname === item.url;

            return (
              <SidebarMenuItem key={item.title}>
                <Link href={item.url} onClick={handleLinkClick}>
                <div className={clsx( isCollapsed && "-ml-5")}>
                    <SidebarMenuButton
                      isActive={isActive}
                      className={clsx(
                        "py-5 transition-all duration-200 flex items-center gap-3  rounded-lg mb-2 cursor-pointer !font-bold",
                        isActive
                          ? " !text-white !bg-[#8c52f1]/10 "
                          : "!text-white",
                      )}
                    >
                      {item.icon && (
                        <item.icon
                          className={clsx(
                            "size-5 transition-colors font-bold",
                            isActive ? "text-[#8c52f1] " : "",
                          )}
                        />
                      )}
                      {!isCollapsed && (
                        <span className="text-sm">{item.title}</span>
                      )}{" "}
                    </SidebarMenuButton>
                  </div>
                </Link>
              </SidebarMenuItem>
            );
          })}
        </SidebarMenu>
      </SidebarGroupContent>
    </SidebarGroup>
  );
}
