"use client";

import * as React from "react";
import { Area, AreaChart, CartesianGrid, XAxis, YAxis } from "recharts";

import { useIsMobile } from "@/hooks/use-mobile";
import {
  Card,
  CardAction,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import {
  ChartContainer,
  ChartTooltip,
  ChartTooltipContent,
  type ChartConfig,
} from "@/components/ui/chart";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { ToggleGroup, ToggleGroupItem } from "@/components/ui/toggle-group";

export const description =
  "TapPay Wallet Activity shows your income vs spending over time in ₦.";

const chartData = [
  { date: "2026-01-01", income: 25000, expense: 12000 },
  { date: "2026-01-03", income: 0, expense: 8000 },
  { date: "2026-01-05", income: 12000, expense: 6000 },
  { date: "2026-01-07", income: 0, expense: 4500 },
  { date: "2026-01-10", income: 30000, expense: 18000 },
  { date: "2026-01-12", income: 0, expense: 9000 },
  { date: "2026-01-15", income: 5000, expense: 3000 },
  { date: "2026-01-18", income: 0, expense: 7000 },
  { date: "2026-01-20", income: 15000, expense: 11000 },
  { date: "2026-01-22", income: 0, expense: 5000 },
  { date: "2026-01-25", income: 40000, expense: 25000 },

  { date: "2026-02-01", income: 0, expense: 10000 },
  { date: "2026-02-05", income: 20000, expense: 12000 },
  { date: "2026-02-10", income: 0, expense: 9000 },
  { date: "2026-02-15", income: 35000, expense: 21000 },
  { date: "2026-02-20", income: 0, expense: 14000 },
  { date: "2026-02-25", income: 18000, expense: 13000 },

  { date: "2026-03-01", income: 42000, expense: 26000 },
  { date: "2026-03-05", income: 0, expense: 9000 },
  { date: "2026-03-10", income: 30000, expense: 20000 },
  { date: "2026-03-15", income: 0, expense: 15000 },
  { date: "2026-03-20", income: 25000, expense: 18000 },
  { date: "2026-03-25", income: 50000, expense: 32000 },
  { date: "2026-03-29", income: 12000, expense: 40000 },
];

const formatKobo = (kobo: number) => {
  return new Intl.NumberFormat("en-NG", {
    style: "currency",
    currency: "NGN",
    maximumFractionDigits: 0,
  }).format(kobo / 100);
};

const chartConfig = {
  income_kobo: {
    label: "Income",
    color: "var(--color-income)",
  },
  expense_kobo: {
    label: "Expenses",
    color: "var(--color-expense)",
  },
} satisfies ChartConfig;

export function ChartAreaInteractive() {
  const isMobile = useIsMobile();
  const [timeRange, setTimeRange] = React.useState("90d");

  const [loading, setLoading] = React.useState(true);

  React.useEffect(() => {
    const t = setTimeout(() => setLoading(false), 1500);
    return () => clearTimeout(t);
  }, []);

  React.useEffect(() => {
    if (isMobile) setTimeRange("90d");
  }, [isMobile]);

  const filteredData = chartData.filter((item) => {
    const date = new Date(item.date);
    const referenceDate = new Date();

    let days = 90;
    if (timeRange === "30d") days = 30;
    if (timeRange === "7d") days = 7;

    const start = new Date(referenceDate);
    start.setDate(start.getDate() - days);

    return date >= start;
  });
    if (loading) return <ChartSkeleton />

  return (
    <Card className="@container/card mt-4 px-2">
      <CardHeader>
        <CardTitle className="font-bold text-neutral-300 ">
          TapPay Wallet Activity
        </CardTitle>
        <CardDescription>Income vs Expenses</CardDescription>

        <CardAction>
          <ToggleGroup
            type="single"
            value={timeRange}
            onValueChange={setTimeRange}
            variant="outline"
            className="hidden @[767px]/card:flex"
          >
            <ToggleGroupItem value="90d">3 Months</ToggleGroupItem>
            <ToggleGroupItem value="30d">30 Days</ToggleGroupItem>
            <ToggleGroupItem value="7d">7 Days</ToggleGroupItem>
          </ToggleGroup>

          <Select value={timeRange} onValueChange={setTimeRange}>
            <SelectTrigger className="flex w-40 @[767px]/card:hidden" size="sm">
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="90d">3 Months</SelectItem>
              <SelectItem value="30d">30 Days</SelectItem>
              <SelectItem value="7d">7 Days</SelectItem>
            </SelectContent>
          </Select>
        </CardAction>
      </CardHeader>

      <CardContent className="px-2 pt-4 sm:px-6 sm:pt-6">
        <ChartContainer config={chartConfig} className="h-[320px] w-full">
          <AreaChart data={filteredData}>
            <defs>
              <linearGradient id="incomeFill" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#00CF7B" stopOpacity={0.9} />
                <stop offset="95%" stopColor="#00CF7B" stopOpacity={0.05} />
              </linearGradient>

              <linearGradient id="expenseFill" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#0F9D58" stopOpacity={0.7} />
                <stop offset="95%" stopColor="#0F9D58" stopOpacity={0.05} />
              </linearGradient>
            </defs>

            <CartesianGrid vertical={false} strokeDasharray="3 3" />

            <XAxis
              dataKey="date"
              tickLine={false}
              axisLine={false}
              tickMargin={10}
              tickFormatter={(val) =>
                new Date(val).toLocaleDateString("en-NG", {
                  month: "short",
                  day: "numeric",
                })
              }
            />

            <ChartTooltip
              cursor={false}
              content={
                <ChartTooltipContent
                  labelFormatter={(val) =>
                    new Date(val).toLocaleDateString("en-NG", {
                      month: "short",
                      day: "numeric",
                    })
                  }
                  formatter={(value) => formatKobo(Number(value))}
                  indicator="dot"
                />
              }
            />

            <Area
              dataKey="income"
              type="natural"
              fill="url(#expenseFill)"
              stroke="var(--color-expense)"
            />

            <Area
              dataKey="expense"
              type="natural"
              fill="url(#incomeFill)"
              stroke="var(--color-income)"
            />
          </AreaChart>
        </ChartContainer>
      </CardContent>
    </Card>
  );
}

function ChartSkeleton() {
  return (
    <Card className="@container/card mt-4">
      <CardHeader>
        <div className="h-5 w-40 bg-neutral-800 rounded animate-pulse" />
        <div className="h-3 w-28 bg-neutral-800 rounded animate-pulse mt-2" />

        <div className="mt-4 flex gap-2">
          <div className="h-8 w-24 bg-neutral-800 rounded animate-pulse" />
          <div className="h-8 w-24 bg-neutral-800 rounded animate-pulse" />
          <div className="h-8 w-24 bg-neutral-800 rounded animate-pulse" />
        </div>
      </CardHeader>

      <CardContent className="px-2 pt-4 sm:px-6 sm:pt-6">
        <div className="h-[320px] w-full bg-white/5 rounded-lg animate-pulse" />
      </CardContent>
    </Card>
  );
}
