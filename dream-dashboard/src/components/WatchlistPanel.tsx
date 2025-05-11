'use client';

import React, { useState } from "react";
import { Card } from "./ui/card";
import { Button } from "./ui/button";

const initialWatchlist = [
  { type: "Player", name: "Luka Dončić" },
  { type: "Team", name: "Golden State Warriors" },
  { type: "Game", name: "Lakers vs. Celtics" },
];

export default function WatchlistPanel() {
  const [watchlist, setWatchlist] = useState(initialWatchlist);

  return (
    <Card className="bg-white text-black dark:bg-gray-900 dark:text-white p-6 border-l-4 border-purple-700 dark:border-purple-500 flex flex-col gap-2">
      <h3 className="text-base font-bold text-purple-700 dark:text-purple-400 mb-2">Watchlist</h3>
      <ul className="text-sm space-y-1 mb-2">
        {watchlist.map((item: any, i: number) => (
          <li key={i} className="flex items-center gap-2">
            <span className="text-purple-700 dark:text-purple-300 font-semibold text-sm">{item.type}:</span> <span className="text-sm">{item.name}</span>
          </li>
        ))}
      </ul>
      <Button className="bg-purple-700 dark:bg-purple-600 text-white w-full !opacity-100" disabled={false} onClick={() => window.alert('Add to Watchlist feature coming soon!')}>Add to Watchlist (UI only)</Button>
    </Card>
  );
} 