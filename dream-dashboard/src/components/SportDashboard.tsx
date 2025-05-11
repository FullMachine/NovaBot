"use client";
import React, { useState } from "react";
import PlayerCard from './PlayerCard';
import Link from 'next/link';
import { getSportTeams, getSportStandings, getSportPlayers } from '../data/sportData';

interface SportDashboardProps {
  sport: string;
}

export default function SportDashboard({ sport }: SportDashboardProps) {
  const teams = getSportTeams(sport);
  const standingsData = getSportStandings(sport);
  const players = getSportPlayers(sport);
  const [search, setSearch] = useState("");
  const [standingsTab, setStandingsTab] = useState(Object.keys(standingsData)[0]);
  const isMLB = sport === 'MLB';
  const filteredPlayers = search
    ? players.filter((p: any) => p.name.toLowerCase().includes(search.toLowerCase()))
    : players;

  return (
    <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 p-8 min-h-screen bg-gray-950">
      {/* Live Games */}
      <div className="lg:col-span-3 flex flex-col gap-6">
        <h2 className="text-2xl font-bold text-yellow-400 mb-2">Live {sport} Games</h2>
        <div className="bg-gray-900 rounded-2xl shadow-xl p-4 flex flex-col gap-4">
          <div className="text-white">No live {sport} games right now. Check back later!</div>
        </div>
        {/* All Teams Card */}
        <div className="bg-gray-900 rounded-2xl shadow-xl p-4 flex flex-col gap-4 mt-8">
          <h3 className="text-lg font-semibold text-blue-300 mb-2">All {sport} Teams</h3>
          <div className="grid grid-cols-2 gap-3">
            {teams.map((team: any) => (
              <div key={team.abbr} className="flex items-center gap-2 bg-gray-800 rounded-lg p-2">
                <div className="w-12 h-12 flex items-center justify-center bg-white rounded-full shadow" style={{ backgroundColor: '#fff' }}>
                  <img src={team.logo} alt={team.abbr} className="w-8 h-8 object-contain" onError={e => e.currentTarget.src = 'https://via.placeholder.com/32'} />
                </div>
                <span className="text-white text-sm">{team.abbr}</span>
              </div>
            ))}
          </div>
        </div>
      </div>
      {/* Leagues/News + Player Search + Standings */}
      <div className="lg:col-span-6 flex flex-col gap-6">
        {/* Player Search Card */}
        <div className="bg-gray-900 rounded-2xl shadow-xl p-4 flex flex-col gap-4 mb-4">
          <h3 className="text-lg font-semibold text-green-300 mb-2">Search {sport} Players</h3>
          <input
            type="text"
            placeholder={`Type a player name...`}
            value={search}
            onChange={e => setSearch(e.target.value)}
            className="p-2 rounded-lg bg-gray-800 text-white focus:outline-none focus:ring-2 focus:ring-green-400"
          />
          {search && (
            <div className="bg-gray-800 rounded-lg p-2 max-h-40 overflow-y-auto">
              {filteredPlayers.length === 0 ? (
                <div className="text-gray-400">No players found.</div>
              ) : (
                filteredPlayers.slice(0, 8).map((player: any) => {
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
        {/* Leagues/News */}
        <div className="bg-gray-900 rounded-2xl shadow-xl p-4 flex flex-col gap-4">
          <h2 className="text-2xl font-bold text-blue-400 mb-2">{sport} Leagues & News</h2>
          <div className="text-white mb-2">{sport} news and league standings below!</div>
          {/* Standings Tabs */}
          <div className="flex gap-2 mb-2">
            {Object.keys(standingsData).map(tab => (
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
            {Array.isArray(standingsData[standingsTab]) ? (
              <table className="min-w-full text-white text-sm">
                <thead>
                  <tr className="bg-gray-800">
                    <th className="px-2 py-1 text-left">Team</th>
                    <th className="px-2 py-1">W</th>
                    <th className="px-2 py-1">L</th>
                    <th className="px-2 py-1">Conf/Div</th>
                  </tr>
                </thead>
                <tbody>
                  {standingsData[standingsTab].map((row: any) => (
                    <tr key={row.abbr} className="border-b border-gray-700">
                      <td className="flex items-center gap-2 py-1">
                        <div className="w-10 h-10 flex items-center justify-center bg-white rounded-full shadow" style={{ backgroundColor: '#fff' }}>
                          <img src={row.logo} alt={row.abbr} className="w-7 h-7 object-contain" onError={e => e.currentTarget.src = 'https://via.placeholder.com/24'} />
                        </div>
                        {row.team}
                      </td>
                      <td className="text-center">{row.wins}</td>
                      <td className="text-center">{row.losses}</td>
                      <td className="text-center">{row.conf || row.div}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            ) : (
              <div className="text-gray-400 text-center py-4">No standings available for this sport.</div>
            )}
          </div>
        </div>
      </div>
      {/* Top Players */}
      <div className="lg:col-span-3 flex flex-col gap-6">
        <h2 className="text-2xl font-bold text-purple-400 mb-2">Top {sport} Players</h2>
        <div className="flex flex-col gap-4">
          {players.slice(0, 5).map((player: any) => (
            <PlayerCard key={player.name} player={player} isFavorite={false} isWatchlisted={false} onFavorite={() => {}} onWatchlist={() => {}} />
          ))}
        </div>
      </div>
    </div>
  );
} 