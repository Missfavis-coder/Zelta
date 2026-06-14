import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}


export const formatToKobo = (
  amount: number,
  currency: string = "NGN"
) => {
  return new Intl.NumberFormat("en-NG", {
    style: "currency",
    currency,
  }).format(amount);
}; 

export const formatCurr = (
  amount: number,
  asset: "NGN" | "PTS",
  direction?: "IN" | "OUT"
) => {
  const value = asset === "NGN" ? amount / 100 : amount;

  const formatted = value.toLocaleString();

  const prefix = direction
    ? direction === "IN"
      ? "+"
      : "-"
    : "";

  const symbol = asset === "NGN" ? "₦" : "PTS ";

  return `${prefix}${symbol}${formatted}`;
};

export const formatCurrency = (amount: number, type: "CREDIT" | "DEBIT") => {
    const naira = amount / 100;
    const formatted = naira.toLocaleString();

    return type === "CREDIT" ? `+₦${formatted}` : `-₦${formatted}`;
  };

export  function formatDate(date: string | Date) {
    const d = typeof date === "string" ? new Date(date) : date;

    return d.toLocaleDateString("en-NG", {
      day: "numeric",
      month: "short",
      year: "numeric",
    });
  }

  export function formatNaira(amount: number): string {
    const value = Number.isFinite(amount) ? amount : 0;
    return new Intl.NumberFormat("en-NG", {
      style: "currency",
      currency: "NGN",
      minimumFractionDigits: 2,
      maximumFractionDigits: 2,
    }).format(value);
  }

  // Relative time: "Just now", "2 minutes ago", "Yesterday", "May 6"
  export function formatRelativeTime(date: string | Date | null | undefined) {
    if (!date) return "";
    const d = typeof date === "string" ? new Date(date) : date;
    if (Number.isNaN(d.getTime())) return "";

    const now = Date.now();
    const diffMs = now - d.getTime();
    const sec = Math.floor(diffMs / 1000);

    if (sec < 45) return "Just now";
    const min = Math.floor(sec / 60);
    if (min < 60) return `${min} minute${min === 1 ? "" : "s"} ago`;
    const hr = Math.floor(min / 60);
    if (hr < 24) return `${hr} hour${hr === 1 ? "" : "s"} ago`;

    const today = new Date();
    today.setHours(0, 0, 0, 0);
    const dDay = new Date(d);
    dDay.setHours(0, 0, 0, 0);
    const dayDiff = Math.round(
      (today.getTime() - dDay.getTime()) / (24 * 60 * 60 * 1000),
    );
    if (dayDiff === 1) return "Yesterday";
    if (dayDiff < 7) return `${dayDiff} days ago`;

    const months = [
      "Jan", "Feb", "Mar", "Apr", "May", "Jun",
      "Jul", "Aug", "Sep", "Oct", "Nov", "Dec",
    ];
    const sameYear = d.getFullYear() === new Date().getFullYear();
    return sameYear
      ? `${months[d.getMonth()]} ${d.getDate()}`
      : `${months[d.getMonth()]} ${d.getDate()}, ${d.getFullYear()}`;
  }

  // Spec format: MMM DD, YYYY  (e.g. "May 06, 2026")
  export function formatLongDate(date: string | Date | null | undefined) {
    if (!date) return "—";
    const d = typeof date === "string" ? new Date(date) : date;
    if (Number.isNaN(d.getTime())) return "—";
    const months = [
      "Jan", "Feb", "Mar", "Apr", "May", "Jun",
      "Jul", "Aug", "Sep", "Oct", "Nov", "Dec",
    ];
    const day = String(d.getDate()).padStart(2, "0");
    return `${months[d.getMonth()]} ${day}, ${d.getFullYear()}`;
  }

  type Transaction = {
    type: "CREDIT" | "DEBIT";
    amount: number; 
  };
  
  export const calculateStats = (transactions: Transaction[]) => {
    let income = 0;
    let expense = 0;
  
    transactions.forEach((txn) => {
      if (txn.type === "CREDIT") {
        income += txn.amount;
      } else {
        expense += txn.amount;
      }
    });
  
    return { income, expense };
  }