'use client';
import React from "react";
import { Card } from "./ui/card";

const hotStreaks = [
  { name: "Erling Haaland", streak: 3 },
  { name: "Karim Benzema", streak: 2 },
];
const coldStreaks = [
  { name: "Kevin De Bruyne", streak: 3 },
  { name: "Son Heung-min", streak: 2 },
];

export default function StreaksPanel() {
  return (
    <Card className="bg-white text-black dark:bg-gray-900 dark:text-white p-6 flex flex-col gap-2 border-l-4 border-purple-700 dark:border-purple-500">
      <h3 className="text-base font-bold text-purple-700 dark:text-purple-400 mb-2">Current Streaks</h3>
      <div className="flex gap-6">
        <div>
          <div className="font-semibold text-green-400 text-sm mb-1">Hot</div>
          <ul className="text-sm space-y-1">
            {hotStreaks.map((p) => (
              <li key={p.name}>{p.name} <span className="ml-1 text-xs text-gray-700 dark:text-gray-300">({p.streak})</span></li>
            ))}
          </ul>
        </div>
        <div>
          <div className="font-semibold text-red-400 text-sm mb-1">Cold</div>
          <ul className="text-sm space-y-1">
            {coldStreaks.map((p) => (
              <li key={p.name}>{p.name} <span className="ml-1 text-xs text-gray-700 dark:text-gray-300">({p.streak})</span></li>
            ))}
          </ul>
        </div>
      </div>
    </Card>
  );
} 