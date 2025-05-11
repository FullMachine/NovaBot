'use client';

import React, { useState } from "react";
import { Card } from "./ui/card";

const options = [
  "Luka Dončić",
  "Jayson Tatum",
  "Patrick Mahomes",
  "Shohei Ohtani",
  "Erling Haaland",
  "Iga Świątek",
  "Faker",
];

const playerStats = {
  "Luka Dončić": { sport: "NBA", stats: { PTS: 28.5, AST: 8.2, REB: 7.9 } },
  "Jayson Tatum": { sport: "NBA", stats: { PTS: 25.1, AST: 6.0, REB: 8.5 } },
  "Patrick Mahomes": { sport: "NFL", stats: { "PASS YDS": 4300, "PASS TD": 38, INT: 12 } },
  "Shohei Ohtani": { sport: "MLB", stats: { HR: 44, RBI: 95, AVG: ".304" } },
  "Erling Haaland": { sport: "Soccer", stats: { GOALS: 36, ASSISTS: 7, MATCHES: 32 } },
  "Iga Świątek": { sport: "Tennis", stats: { WINS: 55, LOSSES: 8, TITLES: 7 } },
  "Faker": { sport: "Esports", stats: { KDA: 4.2, WINS: 18, MATCHES: 25 } },
};

function getStatLabels(sport: string) {
  switch (sport) {
    case "NBA": return ["PTS", "AST", "REB"];
    case "NFL": return ["PASS YDS", "PASS TD", "INT"];
    case "MLB": return ["HR", "RBI", "AVG"];
    case "Soccer": return ["GOALS", "ASSISTS", "MATCHES"];
    case "Tennis": return ["WINS", "LOSSES", "TITLES"];
    case "Esports": return ["KDA", "WINS", "MATCHES"];
    default: return [];
  }
}

export default function ComparisonPanel() {
  const [left, setLeft] = useState(options[0]);
  const [right, setRight] = useState(options[1]);

  const leftStats = (playerStats as any)[left]?.stats || {};
  const rightStats = (playerStats as any)[right]?.stats || {};
  const leftLabels = getStatLabels((playerStats as any)[left]?.sport);
  const rightLabels = getStatLabels((playerStats as any)[right]?.sport);

  return (
    <Card className="bg-white text-black dark:bg-gray-900 dark:text-white p-6 border-l-4 border-purple-700 dark:border-purple-500 flex flex-col gap-4">
      <h3 className="text-xl font-bold text-purple-700 dark:text-purple-400 mb-4">Player/Team Comparison</h3>
      <div className="flex gap-4 items-center mb-2">
        <select className="bg-gray-800 text-purple-300 px-2 py-1 rounded" value={left} onChange={e => setLeft(e.target.value)}>
          {options.map(o => <option key={o}>{o}</option>)}
        </select>
        <span className="text-gray-400">vs</span>
        <select className="bg-gray-800 text-purple-300 px-2 py-1 rounded" value={right} onChange={e => setRight(e.target.value)}>
          {options.map(o => <option key={o}>{o}</option>)}
        </select>
      </div>
      <div className="flex gap-8 justify-between">
        <div className="flex-1 text-center">
          <div className="text-lg font-bold text-purple-700 dark:text-purple-300 mb-2">{left}</div>
          <div className="space-y-1">
            {leftLabels.map(label => (
              <div key={label} className="text-base"><span className="font-semibold text-lg">{leftStats[label]}</span> <span className="font-normal">{label}</span></div>
            ))}
          </div>
        </div>
        <div className="flex-1 text-center">
          <div className="text-lg font-bold text-purple-700 dark:text-purple-300 mb-2">{right}</div>
          <div className="space-y-1">
            {rightLabels.map(label => (
              <div key={label} className="text-base"><span className="font-semibold text-lg">{rightStats[label]}</span> <span className="font-normal">{label}</span></div>
            ))}
          </div>
        </div>
      </div>
    </Card>
  );
} 