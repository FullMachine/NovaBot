"use client";
import React, { useState } from "react";
import PlayerCard from '../../../components/PlayerCard';
import { fakePlayers } from '../../../data/fakePlayers';
import Link from 'next/link';

// Mock NBA teams data
const nbaTeams = [
  { name: "Los Angeles Lakers", abbr: "LAL", logo: "https://cdn.nba.com/logos/nba/1610612747/primary/L/logo.svg", conf: "West" },
  { name: "Boston Celtics", abbr: "BOS", logo: "https://cdn.nba.com/logos/nba/1610612738/primary/L/logo.svg", conf: "East" },
  { name: "Golden State Warriors", abbr: "GSW", logo: "https://cdn.nba.com/logos/nba/1610612744/primary/L/logo.svg", conf: "West" },
  { name: "Miami Heat", abbr: "MIA", logo: "https://cdn.nba.com/logos/nba/1610612748/primary/L/logo.svg", conf: "East" },
  { name: "Milwaukee Bucks", abbr: "MIL", logo: "https://cdn.nba.com/logos/nba/1610612749/primary/L/logo.svg", conf: "East" },
  { name: "Dallas Mavericks", abbr: "DAL", logo: "https://cdn.nba.com/logos/nba/1610612742/primary/L/logo.svg", conf: "West" },
  // ...add more teams as needed
];

// Mock NBA standings data
const nbaStandings = {
  All: [
    { team: "Boston Celtics", abbr: "BOS", conf: "East", wins: 62, losses: 20 },
    { team: "Denver Nuggets", abbr: "DEN", conf: "West", wins: 57, losses: 25 },
    { team: "Oklahoma City Thunder", abbr: "OKC", conf: "West", wins: 56, losses: 26 },
    { team: "Milwaukee Bucks", abbr: "MIL", conf: "East", wins: 54, losses: 28 },
    // ...add more teams
  ],
  East: [
    { team: "Boston Celtics", abbr: "BOS", conf: "East", wins: 62, losses: 20 },
    { team: "Milwaukee Bucks", abbr: "MIL", conf: "East", wins: 54, losses: 28 },
    // ...add more East teams
  ],
  West: [
    { team: "Denver Nuggets", abbr: "DEN", conf: "West", wins: 57, losses: 25 },
    { team: "Oklahoma City Thunder", abbr: "OKC", conf: "West", wins: 56, losses: 26 },
    // ...add more West teams
  ],
};

export default function NBADashboard() {
  const nbaPlayers = fakePlayers.filter(p => p.sport === 'NBA');
  const [search, setSearch] = useState("");
  const [standingsTab, setStandingsTab] = useState("All");
  const filteredPlayers = search
    ? nbaPlayers.filter(p => p.name.toLowerCase().includes(search.toLowerCase()))
    : nbaPlayers;

  return (
    <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 p-8 min-h-screen bg-gray-950">
      {/* Live Games */}
      <div className="lg:col-span-3 flex flex-col gap-6">
        <h2 className="text-2xl font-bold text-yellow-400 mb-2">Live NBA Games</h2>
        <div className="bg-gray-900 rounded-2xl shadow-xl p-4 flex flex-col gap-4">
          <div className="text-white">No live NBA games right now. Check back later!</div>
        </div>
        {/* All Teams Card */}
        <div className="bg-gray-900 rounded-2xl shadow-xl p-4 flex flex-col gap-4 mt-8">
          <h3 className="text-lg font-semibold text-blue-300 mb-2">All NBA Teams</h3>
          <div className="grid grid-cols-2 gap-3">
            {nbaTeams.map(team => (
              <div key={team.abbr} className="flex items-center gap-2 bg-gray-800 rounded-lg p-2">
                <img src={team.logo} alt={team.abbr} className="w-8 h-8 object-contain bg-white rounded-full" onError={e => e.currentTarget.src = 'https://via.placeholder.com/32'} />
                <span className="text-white text-sm">{team.abbr}</span>
              </div>
            ))}
          </div>
        </div>
      </div>
      {/* NBA Leagues/News + Player Search + Standings */}
      <div className="lg:col-span-6 flex flex-col gap-6">
        {/* Player Search Card */}
        <div className="bg-gray-900 rounded-2xl shadow-xl p-4 flex flex-col gap-4 mb-4">
          <h3 className="text-lg font-semibold text-green-300 mb-2">Search NBA Players</h3>
          <input
            type="text"
            placeholder="Type a player name..."
            value={search}
            onChange={e => setSearch(e.target.value)}
            className="p-2 rounded-lg bg-gray-800 text-white focus:outline-none focus:ring-2 focus:ring-green-400"
          />
          {search && (
            <div className="bg-gray-800 rounded-lg p-2 max-h-40 overflow-y-auto">
              {filteredPlayers.length === 0 ? (
                <div className="text-gray-400">No players found.</div>
              ) : (
                filteredPlayers.slice(0, 8).map(player => {
                  // Create a slug for the player (e.g., luka-doncic)
                  const playerId = player.name.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/(^-|-$)/g, '');
                  return (
                    <Link key={player.name} href={`/sports/players/${playerId}`} className="flex items-center gap-2 py-1 border-b border-gray-700 last:border-b-0 hover:bg-gray-700/40 rounded cursor-pointer transition">
                      <img src={player.photo} alt={player.name} className="w-6 h-6 rounded-full object-cover bg-white" onError={e => e.currentTarget.src = 'https://via.placeholder.com/24'} />
                      <span className="text-white text-sm">{player.name}</span>
                      <span className="text-gray-400 text-xs ml-auto">{player.team}</span>
                    </Link>
                  );
                })
              )}
            </div>
          )}
        </div>
        {/* NBA Leagues/News */}
        <div className="bg-gray-900 rounded-2xl shadow-xl p-4 flex flex-col gap-4">
          <h2 className="text-2xl font-bold text-blue-400 mb-2">NBA Leagues & News</h2>
          <div className="text-white mb-2">NBA news and league standings below!</div>
          {/* Standings Tabs */}
          <div className="flex gap-2 mb-2">
            {['All', 'East', 'West'].map(tab => (
              <button
                key={tab}
                onClick={() => setStandingsTab(tab)}
                className={`px-3 py-1 rounded-full text-sm font-semibold ${standingsTab === tab ? 'bg-blue-500 text-white' : 'bg-gray-800 text-blue-200'} transition`}
              >
                {tab}
              </button>
            ))}
          </div>
          {/* Standings Table */}
          <div className="overflow-x-auto">
            <table className="min-w-full text-white text-sm">
              <thead>
                <tr className="bg-gray-800">
                  <th className="px-2 py-1 text-left">Team</th>
                  <th className="px-2 py-1">W</th>
                  <th className="px-2 py-1">L</th>
                  <th className="px-2 py-1">Conf</th>
                </tr>
              </thead>
              <tbody>
                {(nbaStandings as any)[standingsTab].map((row: any) => (
                  <tr key={row.abbr} className="border-b border-gray-700">
                    <td className="flex items-center gap-2 py-1">
                      <img src={`https://cdn.nba.com/logos/nba/16106127${row.abbr === 'BOS' ? '38' : row.abbr === 'DEN' ? '76' : row.abbr === 'OKC' ? '37' : row.abbr === 'MIL' ? '49' : '00'}/primary/L/logo.svg`} alt={row.abbr} className="w-6 h-6 object-contain bg-white rounded-full" onError={e => e.currentTarget.src = 'https://via.placeholder.com/24'} />
                      {row.team}
                    </td>
                    <td className="text-center">{row.wins}</td>
                    <td className="text-center">{row.losses}</td>
                    <td className="text-center">{row.conf}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
      {/* Top NBA Players */}
      <div className="lg:col-span-3 flex flex-col gap-6">
        <h2 className="text-2xl font-bold text-purple-400 mb-2">Top NBA Players</h2>
        <div className="flex flex-col gap-4">
          {nbaPlayers.slice(0, 5).map(player => (
            <PlayerCard key={player.name} player={player} isFavorite={false} isWatchlisted={false} onFavorite={() => {}} onWatchlist={() => {}} />
          ))}
        </div>
      </div>
    </div>
  );
} 