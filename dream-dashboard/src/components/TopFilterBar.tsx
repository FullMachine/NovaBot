'use client';

import React, { useState } from "react";

const sports = ["NBA", "NFL", "MLB", "Soccer", "Tennis", "Esports"];
const statTypes = ["Points", "Assists", "Goals", "Wins", "KDA"];
const matchups = ["All", "Head-to-Head", "Division", "Playoffs"];

export default function TopFilterBar() {
  const [sport, setSport] = useState(sports[0]);
  const [statType, setStatType] = useState(statTypes[0]);
  const [matchup, setMatchup] = useState(matchups[0]);

  return (
    <div className="w-full flex flex-wrap gap-4 items-center mb-8 p-4 bg-white dark:bg-gray-900 rounded-xl shadow border border-purple-200 dark:border-purple-800">
      <select
        className="bg-gray-100 dark:bg-gray-800 text-purple-700 dark:text-purple-300 px-4 py-2 rounded-md border border-purple-200 dark:border-purple-700 font-medium focus:ring-2 focus:ring-purple-400 focus:outline-none"
        value={sport}
        onChange={e => setSport(e.target.value)}
      >
        {sports.map(s => <option key={s}>{s}</option>)}
      </select>
      <select
        className="bg-gray-100 dark:bg-gray-800 text-purple-700 dark:text-purple-300 px-4 py-2 rounded-md border border-purple-200 dark:border-purple-700 font-medium focus:ring-2 focus:ring-purple-400 focus:outline-none"
        value={statType}
        onChange={e => setStatType(e.target.value)}
      >
        {statTypes.map(s => <option key={s}>{s}</option>)}
      </select>
      <select
        className="bg-gray-100 dark:bg-gray-800 text-purple-700 dark:text-purple-300 px-4 py-2 rounded-md border border-purple-200 dark:border-purple-700 font-medium focus:ring-2 focus:ring-purple-400 focus:outline-none"
        value={matchup}
        onChange={e => setMatchup(e.target.value)}
      >
        {matchups.map(m => <option key={m}>{m}</option>)}
      </select>
    </div>
  );
} 