'use client';
import React from "react";
import { Card } from "./ui/card";

export default function TrendsPanel() {
  return (
    <Card className="bg-white text-black dark:bg-gray-900 dark:text-white p-6 flex flex-col gap-2 border-l-4 border-purple-700 dark:border-purple-500">
      <h3 className="text-base font-bold text-purple-700 dark:text-purple-400 mb-2">Trends & Insights</h3>
      <ul className="list-disc list-inside text-sm space-y-1 mt-1">
        <li>Luka Dončić has hit his Points + Assists prop in 15 of the last 18 games.</li>
        <li>Average of 35.1 Points + Assists over the last 12 games.</li>
        <li>Hit Rate of 77% this season.</li>
        <li>AI Insight: "High probability to exceed 30 PA in next game."</li>
      </ul>
    </Card>
  );
} 