import {
  CloudUpload,
    Wallet,
  } from "lucide-react";
import { Button } from "../ui/button";
import Link from "next/link";
import { useRef } from "react";
import { Input } from "../ui/input";
import { useRouter } from "next/navigation";
  
  export function DashboardMetrics({ financialStatus }: {financialStatus: {
      availableBalance: string;
      safeLockedBalance: string;
      sapaRisk: string;
    };}) {

    const fileInputRef = useRef<HTMLInputElement>(null);
    const router = useRouter();

    const handleUploadClick = () => {
      fileInputRef.current?.click();
    };
    
    const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
      const file = e.target.files?.[0];
    
      if (!file) return;
    
      console.log(file);
    
      // Upload to backend here
    };
    return (
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
  
        <div className="rounded-md border-2 dark:border-none border-neutral-900 dark:border-foreground/10 bg-[#0b0b0b] dark:bg-neutral-200/30 p-6">
          <div className="flex items-center justify-between text-neutral-500 dark:text-foreground/90 lg:text-sm text-xs font-semibold tracking-wide">
            <span>AVAILABLE BALANCE</span>
            <Wallet size={16} />
          </div>
  
          <h2 className="lg:text-2xl text-xl font-bold mt-4 tracking-tight dark:text-foreground">
            {financialStatus.availableBalance}
          </h2>

          <div className=" w-full mt-6">
            <Button
            onClick={()=>(router.push("/dashboard/chat"))}
             className="w-full py-5.5 bg-[#d98825] font-bold cursor-pointer text-white">Chat with Zelta</Button>
          </div>

          <div className="mt-4">
            <p className="text-sm text-neutral-500 dark:text-foreground hover:text-neutral-500 ">Talk to Zelta AI before making another purchase on impulse</p>
          </div>
  
        </div>
  
        <div className="rounded-md border-2 dark:border-none border-neutral-900 bg-[#0b0b0b] dark:bg-neutral-200/30 dark:border-foreground/10 p-5">

        <div className="mb-6">
          <span className="text-neutral-500 dark:text-foreground/90 lg:text-sm text-xs font-semibold uppercase tracking-wide">
            Upload Details
          </span>

         <p className="text-sm text-neutral-400 dark:text-foreground/90 mt-1">
           All files to be uploaded must be in CSV format
         </p>
        </div>

        <div className="flex flex-col items-center justify-center min-h-30 border rounded-md border-dashed border-neutral-800 dark:border-neutral-300 dark:text-foreground/80">
        <Input ref={fileInputRef}
         type="file"
         accept=".csv"
         className="hidden"
         onChange={handleFileChange}
        />

        <div 
        onClick={handleUploadClick}
        className="bg-[#8c52f1]/10 p-4 rounded-3xl cursor-pointer hover:text-[#8c52f1]">
           <CloudUpload/>

        </div>
           <p className="mt-3 text-sm text-neutral-400 dark:text-foreground/90">
             Click to upload a CSV file
           </p>

           <p className="text-xs text-neutral-500">
             or drag and drop
           </p>
        </div>

        </div>
  
      </div>
    );
  }