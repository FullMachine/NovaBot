'use client';

import React from "react";
import { Card } from "./ui/card";

const edges = [
  {
    bet: "NBA: Jayson Tatum Over 7.5 Rebounds",
    edge: "+18% vs Market",
    reason: "Model projects 9.1 REB, market line is 7.5. Opponent allows 2nd most REB to SFs.",
  },
  {
    bet: "NFL: Travis Kelce Anytime TD",
    edge: "+14% vs Market",
    reason: "Model: 0.82 TD probability, market implied 0.68. Red zone usage up 20%.",
  },
  {
    bet: "MLB: Shohei Ohtani Over 1.5 Total Bases",
    edge: "+11% vs Market",
    reason: "Model: 1.9 TB, market line 1.5. Opposing pitcher allows .290 avg to LHBs.",
  },
];

export default function BettingEdgePanel() {
  return (
    <Card className="bg-white text-black dark:bg-gray-900 dark:text-white p-6 border-l-4 border-purple-700 dark:border-purple-500 flex flex-col gap-2">
      <h3 className="text-lg font-bold text-purple-700 dark:text-purple-400 mb-2">Betting Edge & Value Finder</h3>
      <ul className="text-sm space-y-3 mb-2">
        {edges.map((edge, i) => (
          <li key={i} className="mb-2">
            <div className="font-semibold text-purple-700 dark:text-purple-300">{edge.bet} <span className="ml-2 text-green-400">{edge.edge}</span></div>
            <div className="text-gray-300">{edge.reason}</div>
          </li>
        ))}
      </ul>
    </Card>
  );
} 