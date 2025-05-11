'use client';

import React from "react";
import ThemeSwitcher from "./ThemeSwitcher";
import Link from 'next/link';
import { defaultAvatar, getSafeImage } from '../lib/utils';

const sports = [
  { name: "NBA", icon: "🏀" },
  { name: "NFL", icon: "🏈" },
  { name: "MLB", icon: "⚾" },
  { name: "Soccer", icon: "⚽" },
  { name: "Tennis", icon: "🎾" },
  { name: "Esports", icon: "🎮" },
  { name: "Hockey", icon: "🏒" },
  { name: "Golf", icon: "⛳" },
];

type SidebarProps = {
  selectedSport?: string | null;
  setSelectedSport?: (sport: string) => void;
};

export default function Sidebar({ selectedSport = null, setSelectedSport = () => {} }: SidebarProps) {
  return (
    <aside className="h-screen min-h-screen flex flex-col items-center py-6 bg-gradient-to-b from-gray-900 to-gray-950 border-r border-gray-800 shadow-2xl z-50 w-20">
      <div className="mb-8 flex flex-col items-center justify-center">
        <Link href="/sports">
          <img
            src="https://images.unsplash.com/photo-1517649763962-0c623066013b?auto=format&fit=facearea&w=256&h=256&facepad=2&q=80"
            alt="Company Logo"
            className="w-14 h-14 rounded-full bg-gray-800 border-4 border-yellow-400 shadow mb-2 cursor-pointer hover:scale-105 transition"
            style={{ objectFit: 'cover' }}
          />
        </Link>
      </div>
      <nav className="flex flex-col items-center gap-6 flex-1 justify-center w-full">
        {sports.map(sport => (
          <Link
            key={sport.name}
            href={`/sports/${sport.name.toLowerCase()}`}
            className={`flex items-center justify-center w-12 h-12 rounded-xl transition-all duration-200 focus:outline-none
              ${selectedSport === sport.name ? 'bg-yellow-400 text-black shadow-lg scale-110' : 'text-gray-400 hover:bg-gray-800 hover:text-white'}`}
            title={sport.name}
            aria-label={sport.name}
          >
            <span className="text-2xl">{sport.icon}</span>
          </Link>
        ))}
      </nav>
      <div className="flex flex-col items-center justify-end w-full pb-8 mt-auto">
        <ThemeSwitcher />
      </div>
    </aside>
  );
} 