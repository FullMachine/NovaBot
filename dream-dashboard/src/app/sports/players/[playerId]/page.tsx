"use client";
import React, { useState, useMemo } from "react";
import { useParams, useRouter } from "next/navigation";
import { Card } from "../../../../components/ui/card";
import { Button } from "../../../../components/ui/button";
import { defaultAvatar, getSafeImage } from "../../../../lib/utils";

function slugify(name: string): string {
  return name.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/(^-|-$)/g, "");
}

function calculateAvg(stats: { value?: number }[]): number {
  if (!stats || stats.length === 0) return 0;
  const sum = stats.reduce((a: number, b: { value?: number }) => a + (b.value || 0), 0);
  const avg = stats.length > 0 ? sum / stats.length : 0;
  return isNaN(avg) || !isFinite(avg) ? 0 : parseFloat(avg.toFixed(1));
}
function calculateMedian(stats: { value?: number }[]): number {
  if (!stats || stats.length === 0) return 0;
  const values = stats.map((s: { value?: number }) => s.value !== undefined ? s.value : 0).sort((a: number, b: number) => a - b);
  const mid = Math.floor(values.length / 2);
  let median = 0;
  if (values.length % 2 !== 0) {
    median = values[mid];
  } else {
    median = (values[mid - 1] + values[mid]) / 2;
  }
  return isNaN(median) || !isFinite(median) ? 0 : parseFloat(median.toFixed(1));
}

// Define types for player data
interface StatEntry {
  date: string;
  value: number;
}
interface GameLogEntry {
  player: string;
  result: number;
  line: number;
  odds: string;
  hit: boolean;
}
interface SupportingStat {
  label: string;
  value: number;
}
interface StatsByTab {
  [tab: string]: {
    [statType: string]: StatEntry[];
  };
}
interface Player {
  name: string;
  team: string;
  position: string;
  photo?: string;
  statTabs: string[];
  statTypeTabs: string[];
  statsByTab: StatsByTab;
  line: number;
  overPercent: number;
  gameLog: GameLogEntry[];
  supportingStats: SupportingStat[];
}

function getAllPlayers(): Player[] {
  // Expanded fake data for demo
  // Make sure every player has a real, sport-appropriate photo URL
  // To update or add new player photos, set the 'photo' field to a real image URL
  const players = {
    NBA: [
      {
        name: 'Luka Dončić',
        team: 'Lakers',
        position: 'PG',
        // NBA headshot
        photo: 'https://cdn.nba.com/headshots/nba/latest/1040x760/1629029.png',
        statTabs: ['H2H', 'L5', 'L10', 'L20', '2024', '2023'],
        statTypeTabs: ['PTS', 'AST', 'REB', '3PM', 'STL', 'BLK'],
        statsByTab: {
          H2H: { PTS: [{ date: '5/1', value: 32 }, { date: '4/15', value: 28 }], AST: [{ date: '5/1', value: 10 }, { date: '4/15', value: 12 }] },
          L5: { PTS: [{ date: '5/6', value: 38 }, { date: '5/4', value: 30 }], AST: [{ date: '5/6', value: 12 }, { date: '5/4', value: 9 }] },
        },
        line: 28.5,
        overPercent: 80,
        gameLog: [
          { player: 'Luka Dončić', result: 38, line: 28.5, odds: '20/21', hit: true },
          { player: 'Luka Dončić', result: 30, line: 28.5, odds: '21/20', hit: true },
        ],
        supportingStats: [
          { label: 'Minutes', value: 36 },
          { label: 'Field Goals', value: 12 },
        ],
      },
    ],
    NFL: [
      {
        name: 'Patrick Mahomes',
        team: 'Chiefs',
        position: 'QB',
        // Official NFL headshot
        photo: 'https://static.www.nfl.com/image/upload/t_player_profile_landscape_2x/f_auto/league/qrdbvu4iqy7wkqg8jq8d',
        statTabs: ['L5', 'L10', '2023', '2022'],
        statTypeTabs: ['PASS YDS', 'TD', 'INT', 'RUSH YDS'],
        statsByTab: {
          L5: { 'PASS YDS': [{ date: '12/1', value: 320 }, { date: '11/24', value: 285 }], TD: [{ date: '12/1', value: 3 }, { date: '11/24', value: 2 }] },
        },
        line: 300,
        overPercent: 60,
        gameLog: [
          { player: 'Patrick Mahomes', result: 320, line: 300, odds: '1.9', hit: true },
          { player: 'Patrick Mahomes', result: 285, line: 300, odds: '1.9', hit: false },
        ],
        supportingStats: [
          { label: 'Completions', value: 28 },
          { label: 'Attempts', value: 40 },
        ],
      },
    ],
    MLB: [
      {
        name: 'Shohei Ohtani',
        team: 'Dodgers',
        position: 'DH',
        // MLB headshot
        photo: 'https://content.mlb.com/images/headshots/current/players/660271.jpg',
        statTabs: ['L5', 'L10', '2024'],
        statTypeTabs: ['HR', 'RBI', 'AVG', 'OPS'],
        statsByTab: {
          L5: { HR: [{ date: '5/1', value: 2 }, { date: '4/28', value: 1 }], RBI: [{ date: '5/1', value: 4 }, { date: '4/28', value: 2 }] },
        },
        line: 1.5,
        overPercent: 50,
        gameLog: [
          { player: 'Shohei Ohtani', result: 2, line: 1.5, odds: '2.1', hit: true },
          { player: 'Shohei Ohtani', result: 1, line: 1.5, odds: '2.1', hit: false },
        ],
        supportingStats: [
          { label: 'At Bats', value: 5 },
          { label: 'Hits', value: 3 },
        ],
      },
    ],
    Soccer: [
      {
        name: 'Erling Haaland',
        team: 'Man City',
        position: 'ST',
        // Soccer headshot
        photo: 'https://resources.premierleague.com/premierleague/photos/players/250x250/p223094.png',
        statTabs: ['L5', 'L10', '2024'],
        statTypeTabs: ['GOALS', 'ASSISTS', 'SHOTS'],
        statsByTab: {
          L5: { GOALS: [{ date: '5/1', value: 2 }, { date: '4/28', value: 1 }], ASSISTS: [{ date: '5/1', value: 1 }, { date: '4/28', value: 0 }] },
        },
        line: 1.5,
        overPercent: 70,
        gameLog: [
          { player: 'Erling Haaland', result: 2, line: 1.5, odds: '1.7', hit: true },
          { player: 'Erling Haaland', result: 1, line: 1.5, odds: '1.7', hit: false },
        ],
        supportingStats: [
          { label: 'Minutes', value: 90 },
          { label: 'Shots', value: 5 },
        ],
      },
    ],
    Tennis: [
      {
        name: 'Iga Swiatek',
        team: 'POL',
        position: 'WTA',
        // Tennis headshot
        photo: 'https://www.wtatennis.com/-/media/tennis/players/wta/2023/05/19/15/19/iga-swiatek-wta-headshot-2023-may.png',
        statTabs: ['L5', '2024'],
        statTypeTabs: ['ACES', 'DF', '1ST SERVE %'],
        statsByTab: {
          L5: { ACES: [{ date: '5/1', value: 7 }, { date: '4/28', value: 5 }], DF: [{ date: '5/1', value: 2 }, { date: '4/28', value: 1 }] },
        },
        line: 6.5,
        overPercent: 65,
        gameLog: [
          { player: 'Iga Swiatek', result: 7, line: 6.5, odds: '1.8', hit: true },
          { player: 'Iga Swiatek', result: 5, line: 6.5, odds: '1.8', hit: false },
        ],
        supportingStats: [
          { label: 'Double Faults', value: 2 },
          { label: 'Winners', value: 20 },
        ],
      },
    ],
    Esports: [
      {
        name: 's1mple',
        team: 'NAVI',
        position: 'AWPer',
        // Esports headshot
        photo: 'https://static.hltv.org/images/playerprofile/bodyshot/7998/300.jpeg',
        statTabs: ['L5', 'L10', '2024'],
        statTypeTabs: ['KILLS', 'DEATHS', 'ADR'],
        statsByTab: {
          L5: { KILLS: [{ date: '5/1', value: 28 }, { date: '4/28', value: 32 }], DEATHS: [{ date: '5/1', value: 12 }, { date: '4/28', value: 10 }] },
        },
        line: 25.5,
        overPercent: 75,
        gameLog: [
          { player: 's1mple', result: 28, line: 25.5, odds: '1.6', hit: true },
          { player: 's1mple', result: 32, line: 25.5, odds: '1.6', hit: true },
        ],
        supportingStats: [
          { label: 'ADR', value: 85 },
          { label: 'Headshots', value: 14 },
        ],
      },
    ],
    Hockey: [
      {
        name: 'Connor McDavid',
        team: 'Oilers',
        position: 'C',
        // Hockey headshot
        photo: 'https://cms.nhl.bamgrid.com/images/headshots/current/168x168/8478402.jpg',
        statTabs: ['L5', 'L10', '2024'],
        statTypeTabs: ['GOALS', 'ASSISTS', 'PTS', 'SOG'],
        statsByTab: {
          L5: { GOALS: [{ date: '5/1', value: 2 }, { date: '4/28', value: 1 }], ASSISTS: [{ date: '5/1', value: 3 }, { date: '4/28', value: 2 }] },
        },
        line: 1.5,
        overPercent: 68,
        gameLog: [
          { player: 'Connor McDavid', result: 2, line: 1.5, odds: '1.9', hit: true },
          { player: 'Connor McDavid', result: 1, line: 1.5, odds: '1.9', hit: false },
        ],
        supportingStats: [
          { label: 'Shots on Goal', value: 6 },
          { label: 'Time on Ice', value: 22 },
        ],
      },
    ],
  };
  return Object.values(players).flat();
}

// Helper to get team logo by sport and team name/abbr
function getTeamLogo(sport: string, team: string) {
  const logos: Record<string, Record<string, string>> = {
    NBA: {
      Lakers: 'https://cdn.nba.com/logos/nba/1610612747/primary/L/logo.svg',
      Nuggets: 'https://cdn.nba.com/logos/nba/1610612743/primary/L/logo.svg',
      // Add more NBA teams as needed
    },
    NFL: {
      Chiefs: 'https://static.www.nfl.com/t_q-best/league/api/clubs/logos/KC',
      Bills: 'https://static.www.nfl.com/t_q-best/league/api/clubs/logos/BUF',
      // Add more NFL teams as needed
    },
    MLB: {
      Dodgers: 'https://www.mlbstatic.com/team-logos/119.svg',
      Yankees: 'https://www.mlbstatic.com/team-logos/147.svg',
      // Add more MLB teams as needed
    },
    Soccer: {
      'Man City': 'https://resources.premierleague.com/premierleague/badges/t43.png',
      Arsenal: 'https://resources.premierleague.com/premierleague/badges/t3.png',
      // Add more soccer teams as needed
    },
    Tennis: {},
    Esports: {},
    Hockey: {
      Oilers: 'https://www-league.nhlstatic.com/images/logos/teams-current-primary-light/22.svg',
      Flames: 'https://www-league.nhlstatic.com/images/logos/teams-current-primary-light/20.svg',
      // Add more hockey teams as needed
    },
  };
  return logos[sport]?.[team] || '';
}

export default function PlayerProfilePage() {
  const params = useParams();
  const playerId = params?.playerId || "unknown";
  const allPlayers: Player[] = getAllPlayers();
  let player: Player | undefined = allPlayers.find((p: Player) => slugify(p.name) === playerId);
  if (!player) {
    player = allPlayers.find((p: Player) => slugify(p.name) === 'luka-doncic');
  }
  // Final fallback: hardcoded Luka Dončić if still undefined
  if (!player) {
    player = {
      name: 'Luka Dončić',
      team: 'Lakers',
      position: 'PG',
      photo: 'https://cdn.nba.com/headshots/nba/latest/1040x760/1629029.png',
      statTabs: ['H2H', 'L5', 'L10', 'L20', '2024', '2023'],
      statTypeTabs: ['PTS', 'AST', 'REB', '3PM', 'STL', 'BLK'],
      statsByTab: {},
      line: 28.5,
      overPercent: 80,
      gameLog: [],
      supportingStats: [],
    };
  }

  // Interactive state for tabs
  const [selectedTab, setSelectedTab] = useState(player.statTabs[0]);
  const [selectedStat, setSelectedStat] = useState(player.statTypeTabs[0]);
  const [showAltLines, setShowAltLines] = useState(false);
  const [imgSrc, setImgSrc] = useState(getSafeImage(player.photo));
  // Add custom line state
  const [customLine, setCustomLine] = useState<number>(player.line);

  // Dynamically get stats for the selected tab and stat type
  const stats: StatEntry[] = player.statsByTab?.[selectedTab]?.[selectedStat] || [];
  const avg = calculateAvg(stats);
  const median = calculateMedian(stats);
  const statValues = stats.map((s: StatEntry) => typeof s.value === 'number' ? s.value : 0);
  const maxValue = statValues.length > 0 ? Math.max(...statValues, 1) : 1;
  const safeMaxValue = isNaN(maxValue) || !isFinite(maxValue) || maxValue === 0 ? 1 : maxValue;

  // Filter game log for realism (show last 5 games for selected stat)
  // We'll use the stats array for the game log, since it's stat-specific
  const filteredGameLog = stats.map((s, i) => ({
    player: player.name,
    result: s.value,
    line: customLine,
    odds: '-',
    hit: s.value >= customLine,
    date: s.date,
  }));

  const router = useRouter();

  // Determine sport for the player
  let sport = 'NBA';
  if (player.team === 'Chiefs') sport = 'NFL';
  if (player.team === 'Dodgers') sport = 'MLB';
  if (player.team === 'Man City') sport = 'Soccer';
  if (player.team === 'POL') sport = 'Tennis';
  if (player.team === 'NAVI') sport = 'Esports';
  if (player.team === 'Oilers') sport = 'Hockey';

  // Set mock opponent and time for each sport
  let opponent = '';
  let matchupTime = '';
  if (sport === 'NFL') {
    opponent = 'Bills';
    matchupTime = 'Sun 3:25 PM';
  } else if (sport === 'NBA') {
    opponent = 'Nuggets';
    matchupTime = 'Sun 12:30 PM';
  } else if (sport === 'MLB') {
    opponent = 'Yankees';
    matchupTime = 'Sat 7:10 PM';
  } else if (sport === 'Soccer') {
    opponent = 'Arsenal';
    matchupTime = 'Sat 10:00 AM';
  } else if (sport === 'Hockey') {
    opponent = 'Flames';
    matchupTime = 'Fri 8:00 PM';
  } else {
    opponent = '';
    matchupTime = '';
  }

  return (
    <div className="min-h-screen w-full bg-gradient-to-br from-[#f8fafc] to-[#e0e7ef] text-gray-900 flex flex-col">
      {/* 2. Wide, horizontal header card at the top */}
      <div className="w-full flex flex-col md:flex-row items-center justify-between px-4 md:px-12 py-4 bg-white shadow-md rounded-b-3xl border-b border-gray-200" style={{ minHeight: 120 }}>
        {/* Back button */}
        <button
          className="absolute left-4 top-4 md:static md:mr-6 flex items-center gap-2 text-gray-500 hover:text-purple-700 text-sm font-semibold bg-gray-100 px-3 py-1 rounded-full shadow-sm border border-gray-200"
          onClick={() => router.back()}
        >
          Back
        </button>
        {/* Player photo and info */}
        <div className="flex items-center gap-4 flex-1 min-w-0">
          <img src={imgSrc} alt={player.name} onError={() => setImgSrc(getSafeImage(undefined))} className="w-16 h-16 md:w-20 md:h-20 object-cover rounded-full border-2 border-purple-400 shadow" />
          <div className="flex flex-col min-w-0">
            <div className="flex items-center gap-2 mb-1">
              {/* Team logos (mock, sport-aware) */}
              {sport !== 'Tennis' && sport !== 'Esports' && (
                <>
                  <img src={getTeamLogo(sport, player.team)} alt={player.team} className="w-8 h-8 rounded-full bg-white border border-gray-200" />
                  <span className="text-xs font-semibold text-gray-500">@</span>
                  <img src={getTeamLogo(sport, opponent)} alt={opponent} className="w-8 h-8 rounded-full bg-white border border-gray-200" />
                  <span className="ml-2 text-xs text-gray-400">{matchupTime}</span>
                </>
              )}
            </div>
            <div className="text-lg md:text-2xl font-bold truncate">{player.name}</div>
            <div className="text-xs md:text-base text-gray-500 truncate">{player.team} ({player.position})</div>
          </div>
        </div>
        {/* Stat line selector and stat type tabs */}
        <div className="flex flex-col md:items-end gap-2 mt-4 md:mt-0">
          <div className="flex gap-2 items-center">
            <label className="text-xs font-semibold text-gray-700">Stat:</label>
            <select value={selectedStat} onChange={e => setSelectedStat(e.target.value)} className="rounded px-2 py-1 text-xs bg-white border border-gray-300">
              {player.statTypeTabs.map(tab => (
                <option key={tab} value={tab}>{tab}</option>
              ))}
            </select>
            <label className="text-xs font-semibold text-gray-700 ml-2">Line:</label>
            <input type="number" value={customLine} onChange={e => setCustomLine(Number(e.target.value))} className="w-16 rounded px-2 py-1 text-xs bg-white border border-gray-300" />
            <button className="ml-2 px-3 py-1 rounded-full bg-purple-700 text-white text-xs font-bold shadow hover:bg-purple-800 transition">ALT LINES</button>
          </div>
          {/* Stat type tabs (horizontal, pill-shaped) */}
          <div className="flex gap-2 mt-2">
            {player.statTypeTabs.map(tab => (
              <button
                key={tab}
                className={`px-4 py-1 rounded-full text-sm font-semibold transition border-2 ${selectedStat === tab ? 'bg-purple-700 text-white border-purple-700 shadow scale-105 underline underline-offset-4' : 'bg-gray-100 text-gray-600 border-gray-200 hover:bg-purple-100 hover:text-purple-900'}`}
                onClick={() => setSelectedStat(tab)}
              >
                {tab}
              </button>
            ))}
          </div>
        </div>
      </div>
      {/* 3. Main content area: center and right columns */}
      <div className="flex flex-col lg:flex-row gap-8 w-full max-w-7xl mx-auto mt-8 px-2 md:px-8">
        {/* Center column: stats summary, chart, supporting stats, game log */}
        <div className="flex-1 flex flex-col gap-6">
          {/* Stats summary as colored pills above the chart */}
          <div className="flex flex-wrap gap-2 items-center mb-2">
            {player.statTabs.map((tab, idx) => (
              <button
                key={tab}
                className={`px-3 py-1 rounded-full text-xs font-bold border-2 ${selectedTab === tab ? 'bg-black text-white border-black shadow' : 'bg-gray-100 text-gray-600 border-gray-200 hover:bg-purple-100 hover:text-purple-900'} transition`}
                onClick={() => setSelectedTab(tab)}
              >
                {tab} <span className={`ml-1 font-semibold ${idx % 2 === 0 ? 'text-green-500' : 'text-red-400'}`}>{(20 + idx * 10)}%</span>
              </button>
            ))}
          </div>
          {/* Chart and stats in a large, white card */}
          <div className="bg-white rounded-2xl shadow-lg p-6 flex flex-col gap-4">
            <div className="flex justify-between items-center mb-2">
              <span className="font-bold text-green-600">{player.name} - {selectedStat}</span>
              <span className="text-xs">Avg <b>{avg}</b> | Median <b>{median}</b></span>
            </div>
            <div className="relative w-full bg-gradient-to-b from-purple-50 to-white rounded-lg p-2 flex items-end h-40 min-h-[140px] max-h-[200px] overflow-x-auto">
              {/* Horizontal line for the custom line value */}
              <div className="absolute left-0 right-0" style={{ top: `${160 - customLine * 120 / safeMaxValue}px`, height: 0 }}>
                <div className="border-t-2 border-dashed border-purple-400 w-full" style={{ position: 'relative', top: 0 }}></div>
                <span className="absolute right-0 -top-4 text-xs text-purple-500 font-bold">{customLine}</span>
              </div>
              {stats.length > 0 ? (
                stats.map((s: StatEntry, i: number) => (
                  <div key={i} className="flex flex-col items-center flex-1 mx-1 group">
                    <div className={`rounded-t-md w-full ${s.value >= customLine ? 'bg-green-500' : 'bg-red-400'} transition-all duration-200 group-hover:scale-110 shadow-md`} style={{ height: `${((typeof s.value === 'number' ? s.value : 0) / safeMaxValue) * 120}px`, minHeight: 10, maxHeight: 120 }} title={`Value: ${s.value}`}></div>
                    <span className="text-[14px] font-bold text-gray-700 mt-1">{s.value}</span>
                    <span className="text-[12px] text-gray-400">{s.date}</span>
                  </div>
                ))
              ) : (
                <span className="text-gray-400 text-xs w-full text-center">No stats available for this tab/type</span>
              )}
            </div>
          </div>
          {/* Supporting stats in a white card */}
          <div className="bg-white rounded-2xl shadow-lg p-4 flex flex-wrap gap-4 items-center justify-center">
            <div className="font-bold text-green-600 mb-2 w-full text-center">Supporting Stats</div>
            {player.supportingStats.map(stat => (
              <div key={stat.label} className="bg-gray-100 rounded px-3 py-1 text-xs text-gray-700 m-1">{stat.label}: <span className="font-bold text-gray-900">{stat.value}</span></div>
            ))}
          </div>
          {/* Game log in a white card */}
          <div className="bg-white rounded-2xl shadow-lg p-4">
            <div className="font-bold text-gray-900 mb-2">Game Log</div>
            <table className="w-full text-xs rounded-xl overflow-hidden">
              <thead>
                <tr className="text-purple-600">
                  <th className="p-2">Player</th>
                  <th className="p-2">Result</th>
                  <th className="p-2">Line</th>
                  <th className="p-2">Hit?</th>
                  <th className="p-2">Date</th>
                </tr>
              </thead>
              <tbody>
                {filteredGameLog.map((g, i) => (
                  <tr key={i} className="text-center">
                    <td className="p-2 text-blue-600 font-bold">{g.player}</td>
                    <td className="p-2">{g.result}</td>
                    <td className="p-2">{g.line}</td>
                    <td className="p-2">{g.hit ? <span className="text-green-600">✔</span> : <span className="text-red-500">✗</span>}</td>
                    <td className="p-2">{g.date}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
        {/* 4. Right panel: Player Trends, defense, team rankings */}
        <div className="w-full lg:w-1/3 flex flex-col gap-6">
          {/* Player Trends card (replaces Line movement) */}
          <div className="bg-white rounded-2xl shadow-lg p-4">
            <div className="font-bold text-sm text-gray-700 mb-2">Player Trends</div>
            <ul className="list-disc pl-5 text-xs text-gray-700 space-y-1">
              <li>Averaging 8.2 assists over last 5 games</li>
              <li>Hit over 2.5 3PM in 7 of last 10 games</li>
              <li>Scored 30+ points in 4 of last 6 games</li>
              <li>Recorded a double-double in 3 straight games</li>
            </ul>
          </div>
          {/* Matchup/defense/insights card with tabs */}
          <div className="bg-white rounded-2xl shadow-lg p-4">
            <div className="flex gap-2 mb-2">
              <button className="px-3 py-1 rounded-full text-xs font-bold bg-purple-100 text-purple-700 border border-purple-200">Matchup</button>
              <button className="px-3 py-1 rounded-full text-xs font-bold bg-gray-100 text-gray-500 border border-gray-200">Injuries</button>
              <button className="px-3 py-1 rounded-full text-xs font-bold bg-gray-100 text-gray-500 border border-gray-200">Insights</button>
            </div>
            <div className="font-bold text-sm text-gray-700 mb-2">Key OKC Assists defense</div>
            <div className="flex flex-col gap-1 text-xs">
              <div className="flex justify-between"><span>Assists</span><span className="font-bold">24.6</span></div>
              <div className="flex justify-between text-gray-400"><span>Rank</span><span>4</span></div>
            </div>
          </div>
          {/* Team rankings card */}
          <div className="bg-white rounded-2xl shadow-lg p-4">
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