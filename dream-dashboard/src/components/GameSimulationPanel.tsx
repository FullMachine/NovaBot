'use client';
import React from "react";
import { Card } from "./ui/card";
import { Button } from "./ui/button";

export default function GameSimulationPanel() {
  return (
    <Card className="bg-white text-black dark:bg-gray-900 dark:text-white p-6 flex flex-col items-center border-l-4 border-purple-500">
      <h3 className="text-base font-bold text-purple-700 dark:text-purple-400 mb-3">Game Simulation</h3>
      <div className="flex items-center gap-4 mb-3">
        <span className="text-4xl">🏀</span>
        <span className="text-lg font-bold text-purple-700 dark:text-purple-300">Possible</span>
        <span className="text-4xl">🏀</span>
      </div>
      <div className="text-2xl font-bold mb-2 text-purple-700 dark:text-purple-200">125 - 118</div>
      <Button className="bg-purple-600 hover:bg-purple-700 w-full" onClick={() => window.alert('Game simulation feature coming soon!')}>Compare matchup...</Button>
    </Card>
  );
} 