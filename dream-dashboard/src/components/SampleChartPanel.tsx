'use client';

import React from "react";
import { Card } from "./ui/card";
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts";
import dynamic from 'next/dynamic';

type BarChartProps = { data?: { name: string; value: number }[] };

const DynamicBarChart = dynamic<BarChartProps>(
  () => import('./_SampleBarChart'),
  { ssr: false, loading: () => <div className="flex items-center justify-center h-full text-gray-400">Loading chart...</div> }
);

export default function SampleChartPanel({ data = [] }: { data?: { name: string; value: number }[] }) {
  return (
    <Card className="bg-white text-black dark:bg-gray-900 dark:text-white p-6 border-l-4 border-purple-700 dark:border-purple-500">
      <h3 className="text-base font-bold text-purple-700 dark:text-purple-400 mb-3">Points + Assists (Last 6 Games)</h3>
      <div className="h-48 mt-1">
        {data.length > 0 ? (
          <DynamicBarChart data={data} />
        ) : (
          <div className="flex items-center justify-center h-full text-gray-400">No chart data for this sport yet.</div>
        )}
      </div>
    </Card>
  );
} 