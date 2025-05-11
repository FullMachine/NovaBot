'use client';

import React, { useState } from "react";
import { useRouter } from "next/navigation";
import { fakePlayers } from "../data/fakePlayers";
import { slugify } from "../lib/utils";

export default function QuickSearchBar() {
  const [query, setQuery] = useState("");
  const router = useRouter();
  const results = query.length > 0
    ? fakePlayers.filter(p =>
        p.name.toLowerCase().includes(query.toLowerCase()) ||
        p.team.toLowerCase().includes(query.toLowerCase()) ||
        (p.sport && p.sport.toLowerCase().includes(query.toLowerCase()))
      )
    : [];

  return (
    <div className="w-full mb-8 relative">
      <div className="flex items-center bg-white dark:bg-gray-800 border-2 border-purple-700 rounded-xl px-5 py-3 shadow">
        <span className="text-purple-700 dark:text-purple-400 mr-3 text-2xl">🔍</span>
        <input
          className="bg-transparent outline-none text-black dark:text-white flex-1 placeholder:text-gray-400 text-base"
          type="text"
          placeholder="Quick search players, teams, games..."
          value={query}
          onChange={e => setQuery(e.target.value)}
        />
      </div>
      {results.length > 0 && (
        <ul className="absolute left-0 right-0 bg-white dark:bg-gray-900 border border-purple-700 dark:border-purple-500 rounded-b-xl mt-1 z-40 shadow-lg">
          {results.map((p: any, i: number) => (
            <li
              key={i}
              className="px-4 py-2 text-black dark:text-white hover:bg-purple-100 dark:hover:bg-purple-800 cursor-pointer flex items-center gap-3"
              onClick={() => router.push(`/sports/players/${slugify(p.name)}`)}
            >
              <img src={p.photo} alt={p.name} className="w-7 h-7 rounded-full object-cover border border-purple-300" onError={e => { e.currentTarget.onerror = null; e.currentTarget.src = '/default-avatar.png'; }} />
              <span className="font-bold">{p.name}</span>
              <span className="text-xs text-gray-500">{p.team}</span>
              <span className="text-xs text-purple-700 dark:text-purple-400 ml-auto">{p.sport}</span>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
} 