'use client';

import React, { useEffect, useState } from "react";
import { Card } from "./ui/card";

function useAnimatedNumber(target: number, duration = 1000) {
  const [value, setValue] = useState(0);
  useEffect(() => {
    let start = 0;
    const step = () => {
      start += (target / (duration / 16));
      if (start < target) {
        setValue(Math.round(start));
        requestAnimationFrame(step);
      } else {
        setValue(target);
      }
    };
    step();
  }, [target, duration]);
  return value;
}

export default function AnimatedStatsPanel() {
  const points = useAnimatedNumber(32);
  const assists = useAnimatedNumber(11);
  const rebounds = useAnimatedNumber(8);

  return (
    <Card className="bg-white text-black dark:bg-gray-900 dark:text-white p-6 border-l-4 border-purple-700 dark:border-purple-500 flex flex-col gap-2 items-center">
      <h3 className="text-base font-bold text-purple-700 dark:text-purple-400 mb-2">Animated Stats</h3>
      <div className="flex gap-8 text-center">
        <div>
          <div className="text-3xl font-bold text-purple-700 dark:text-purple-300">{points}</div>
          <div className="text-xs text-gray-700 dark:text-gray-300">Points</div>
        </div>
        <div>
          <div className="text-3xl font-bold text-purple-700 dark:text-purple-300">{assists}</div>
          <div className="text-xs text-gray-700 dark:text-gray-300">Assists</div>
        </div>
        <div>
          <div className="text-3xl font-bold text-purple-700 dark:text-purple-300">{rebounds}</div>
          <div className="text-xs text-gray-700 dark:text-gray-300">Rebounds</div>
        </div>
      </div>
    </Card>
  );
} 