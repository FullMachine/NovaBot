import React, { useState } from 'react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, ReferenceLine, LabelList } from 'recharts';

// Sample player data (replace with real data/fetch later)
const samplePlayers = {
  'luka-doncic': {
    name: 'Luka Dončić',
    team: 'Lakers',
    position: 'PG',
    nationality: 'Slovenian',
    birth: 'Feb 28, 1999',
    hometown: 'Ljubljana',
    photo: 'https://cdn.nba.com/headshots/nba/latest/1040x760/1629029.png',
    bio: 'NBA superstar, playmaker, and triple-double machine.',
    social: {
      twitter: '#',
      instagram: '#',
    },
    stats: {
      regular: 32.1,
      postseason: 29.8,
      career: 27.5,
    },
    upcoming: {
      home: 'Lakers',
      away: 'Warriors',
      date: 'May 10, 2025',
      time: '7:30 PM',
      homeLogo: 'https://cdn.nba.com/logos/nba/1610612747/primary/L/logo.svg',
      awayLogo: 'https://cdn.nba.com/logos/nba/1610612744/primary/L/logo.svg',
    },
    news: [
      { title: 'Dončić drops 40 in playoff win', img: '', date: 'May 8, 2025' },
      { title: 'Luka leads Lakers to Finals', img: '', date: 'May 5, 2025' },
    ],
    recent: [
      { date: '5/8/25', opp: 'GSW', result: 'W 120-115', pts: 40, ast: 12, reb: 9 },
      { date: '5/5/25', opp: 'DEN', result: 'W 110-108', pts: 32, ast: 10, reb: 8 },
      { date: '5/2/25', opp: 'PHX', result: 'L 99-104', pts: 28, ast: 8, reb: 7 },
    ],
  },
};

interface PlayerProfilePageProps {
  params: { playerId: string };
}

export default function PlayerProfilePage({ params }: PlayerProfilePageProps) {
  const playerId = params?.playerId?.toLowerCase() || 'luka-doncic';
  const player = (samplePlayers as any)[playerId] || samplePlayers['luka-doncic'];
  const [imgSrc, setImgSrc] = useState(player.photo);

  // Mock data for chart and supporting stats
  const chartData = [
    { date: '5/1', value: 32, color: '#22c55e' },
    { date: '4/15', value: 28, color: '#f87171' },
    { date: '4/30', value: 35, color: '#22c55e' },
    { date: '3/10', value: 40, color: '#22c55e' },
    { date: '2/25', value: 29, color: '#22c55e' },
  ];
  const supportingStats = [
    { label: 'Minutes', value: 36 },
    { label: 'Field Goals', value: 12 },
    { label: '3pts', value: 5 },
    { label: 'Fouls', value: 2 },
    { label: 'Turnovers', value: 3 },
    { label: 'Free Throws', value: 8 },
  ];
  const gameLog = [
    { player: 'Luka Dončić', result: 38, line: 28.5, odds: '20/21', hit: true },
    { player: 'Luka Dončić', result: 30, line: 28.5, odds: '20/21', hit: true },
    { player: 'Luka Dončić', result: 27, line: 28.5, odds: '20/21', hit: false },
    { player: 'Luka Dončić', result: 35, line: 28.5, odds: '20/21', hit: true },
  ];

  return (
    <div className="min-h-screen w-full bg-gray-100 text-gray-900">
      <div className="flex flex-row w-full min-h-screen">
        {/* Left column (empty/sidebar) */}
        <div className="hidden lg:block w-1/6"></div>
        {/* Center column: main player panel */}
        <div className="flex-1 max-w-2xl flex flex-col gap-4 py-8 px-2 mx-auto">
          {/* Header Card */}
          <div className="bg-white rounded-2xl shadow p-6 flex flex-col items-center gap-2">
            <img src={imgSrc} alt={player.name} className="w-20 h-20 object-cover rounded-full border-4 border-white shadow mb-2" onError={() => setImgSrc('/default-avatar.png')} />
            <div className="text-2xl font-bold mb-1 text-center">{player.name}</div>
            <div className="text-base text-gray-500 mb-1">{player.team} | {player.position} - PTS</div>
            <div className="flex gap-2 w-full justify-center mb-2">
              {['H2H', 'L5', 'L10', 'L20', '2024', '2023'].map((tab, i) => (
                <div key={tab} className={`flex flex-col items-center px-2 ${i === 0 ? 'text-purple-600' : i % 2 === 0 ? 'text-green-600' : 'text-red-500'}`}>
                  <span className="text-xs font-bold">{tab}</span>
                  <span className="text-xs">{['20%', '30%', '40%', '50%', '60%', '70%'][i]}</span>
                </div>
              ))}
            </div>
          </div>
          {/* Stat Type Tabs */}
          <div className="flex gap-2 overflow-x-auto bg-white rounded-xl shadow p-2">
            {['PTS', 'AST', 'REB', '3PM', 'STL', 'BLK'].map(type => (
              <button key={type} className="px-4 py-2 rounded-full text-sm font-semibold whitespace-nowrap bg-purple-600 text-white hover:bg-purple-700 transition">{type}</button>
            ))}
          </div>
          {/* Chart Card */}
          <div className="bg-white rounded-xl shadow p-6 flex flex-col items-center">
            <div className="w-full h-48">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={chartData} barCategoryGap={20}>
                  <XAxis dataKey="date" tick={{ fill: '#888', fontSize: 12 }} />
                  <YAxis tick={{ fill: '#888', fontSize: 12 }} />
                  <Tooltip />
                  <ReferenceLine y={32} stroke="#a855f7" strokeDasharray="3 3" />
                  <Bar dataKey="value" radius={[4, 4, 0, 0]} fill="#22c55e">
                    <LabelList dataKey="value" position="top" fill="#222" />
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            </div>
            <div className="flex w-full justify-between mt-2 text-xs text-gray-500">
              <span>Statistics</span>
              <span>Avg 32.8 | Median 32</span>
            </div>
          </div>
          {/* Supporting Stats */}
          <div className="bg-white rounded-xl shadow p-4 flex flex-wrap gap-4 items-center justify-center">
            <div className="font-bold text-green-600 mb-2 w-full text-center">Supporting Stats</div>
            {supportingStats.map(stat => (
              <div key={stat.label} className="bg-gray-100 rounded px-3 py-1 text-xs text-gray-700 m-1">{stat.label}: <span className="font-bold text-gray-900">{stat.value}</span></div>
            ))}
            <div className="flex gap-2 w-full justify-center mt-2">
              <button className="bg-gray-200 text-gray-900 px-3 py-1 rounded-full text-xs">Average</button>
              <button className="bg-gray-200 text-gray-900 px-3 py-1 rounded-full text-xs">Median</button>
            </div>
          </div>
          {/* ALT LINES Button */}
          <div className="flex justify-center">
            <button className="bg-purple-600 hover:bg-purple-700 text-white font-bold px-8 py-2 rounded-xl shadow transition">ALT LINES</button>
          </div>
          {/* Game Log Card */}
          <div className="bg-white rounded-xl shadow p-4">
            <div className="font-bold text-gray-900 mb-2">Game Log</div>
            <table className="w-full text-xs rounded-xl overflow-hidden">
              <thead>
                <tr className="text-purple-600">
                  <th className="p-2">Player</th>
                  <th className="p-2">Result</th>
                  <th className="p-2">Line</th>
                  <th className="p-2">Odds</th>
                  <th className="p-2">Hit?</th>
                </tr>
              </thead>
              <tbody>
                {gameLog.map((g, i) => (
                  <tr key={i} className="text-center">
                    <td className="p-2 text-blue-600 font-bold">{g.player}</td>
                    <td className="p-2">{g.result}</td>
                    <td className="p-2">{g.line}</td>
                    <td className="p-2">{g.odds}</td>
                    <td className="p-2">{g.hit ? <span className="text-green-600">✔</span> : <span className="text-red-500">✗</span>}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
        {/* Right column: info cards */}
        <div className="hidden lg:flex flex-col gap-4 w-1/4 py-8 pr-8">
          {/* Line movement */}
          <div className="bg-white rounded-xl shadow p-4">
            <div className="font-bold text-sm text-gray-700 mb-2">Line movement</div>
            <div className="flex flex-col gap-1 text-xs">
              <div className="flex justify-between"><span>8:48 AM Today</span><span>1.5 <span className="text-green-600">+1</span></span></div>
              <div className="flex justify-between"><span>8:25 AM Today</span><span>0.5 <span className="text-gray-400">Open</span></span></div>
            </div>
            <div className="text-blue-400 text-xs mt-2 cursor-pointer">Show more</div>
          </div>
          {/* Matchup defense */}
          <div className="bg-white rounded-xl shadow p-4">
            <div className="font-bold text-sm text-gray-700 mb-2">Key OKC Assists defense</div>
            <div className="flex flex-col gap-1 text-xs">
              <div className="flex justify-between"><span>Assists</span><span className="font-bold">24.6</span></div>
              <div className="flex justify-between text-gray-400"><span>Rank</span><span>4</span></div>
            </div>
          </div>
          {/* Team rankings */}
          <div className="bg-white rounded-xl shadow p-4">
            <div className="font-bold text-sm text-gray-700 mb-2">Team Rankings (2024)</div>
            <div className="flex flex-col gap-1 text-xs">
              <div className="flex justify-between"><span>Effective FG%</span><span>56 (7th) vs 54.2 (16th)</span></div>
              <div className="flex justify-between"><span>Turnover %</span><span>11.4 (1st) vs 12.5 (27th)</span></div>
              <div className="flex justify-between"><span>Offensive Rebound %</span><span>24.2 (21st) vs 21.2 (22st)</span></div>
              <div className="flex justify-between"><span>Free Throw Rate</span><span>0.22 (28th) vs 0.22 (22nd)</span></div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
} 