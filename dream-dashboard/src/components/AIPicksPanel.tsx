'use client';

import React from "react";
import { Card } from "./ui/card";
import { Button } from "./ui/button";

const picks = [
  {
    title: "NBA: Luka Dončić Over 28.5 Points",
    reason: "AI: Luka has exceeded 28.5 points in 12 of his last 15 games. Opponent allows 3rd most PPG to PGs.",
  },
  {
    title: "NFL: Patrick Mahomes Over 2.5 Passing TDs",
    reason: "AI: Mahomes averages 3.1 TDs vs this defense. Weather and matchup favorable.",
  },
  {
    title: "Soccer: Erling Haaland to Score",
    reason: "AI: Haaland has scored in 8 of last 10 matches. Opponent concedes 1.7 goals/game.",
  },
];

export default function AIPicksPanel() {
  return (
    <Card className="bg-white text-black dark:bg-gray-900 dark:text-white p-6 border-l-4 border-purple-700 dark:border-purple-500 flex flex-col gap-2">
      <h3 className="text-base font-bold text-purple-700 dark:text-purple-400 mb-2">AI Picks & Recommendations</h3>
      <ul className="text-sm space-y-3 mb-2">
        {picks.map((pick: any, i: number) => (
          <li key={i} className="mb-2">
            <div className="font-semibold text-purple-700 dark:text-purple-300 text-sm">{pick.title}</div>
            <div className="text-gray-700 dark:text-gray-300 text-sm">{pick.reason}</div>
          </li>
        ))}
      </ul>
      <Button className="bg-purple-700 dark:bg-purple-600 text-white w-full !opacity-100" onClick={() => window.alert('More AI Picks feature coming soon!')}>More AI Picks (UI only)</Button>
    </Card>
  );
} 