"use client";
import React, { useState, useEffect, useRef } from "react";
import { Card } from "../../components/ui/card";
import { Button } from "../../components/ui/button";
import TrendsPanel from "../../components/TrendsPanel";
import StreaksPanel from "../../components/StreaksPanel";
import GameSimulationPanel from "../../components/GameSimulationPanel";
import SampleChartPanel from "../../components/SampleChartPanel";
import TopFilterBar from "../../components/TopFilterBar";
import WatchlistPanel from "../../components/WatchlistPanel";
import ComparisonPanel from "../../components/ComparisonPanel";
import AIPicksPanel from "../../components/AIPicksPanel";
import AnimatedStatsPanel from "../../components/AnimatedStatsPanel";
import NewsFeedPanel from "../../components/NewsFeedPanel";
import ThemeSwitcher from "../../components/ThemeSwitcher";
import QuickSearchBar from "../../components/QuickSearchBar";
import PlayerDetailModal from "../../components/PlayerDetailModal";
import PlayerCard from "../../components/PlayerCard";
import WatchLiveModal from "../../components/WatchLiveModal";
import MatchDetailsModal from "../../components/MatchDetailsModal";
import TopBar from "../../components/TopBar";

const players: { [key: string]: PlayerType[] } = {
  NBA: [
    {
      name: 'Luka Dončić',
      team: 'Lakers',
      position: 'PG',
      photo: 'https://cdn.nba.com/headshots/nba/latest/1040x760/1629029.png',
      statTabs: ['H2H', 'L5', 'L10', 'L20', '2024', '2023'],
      statTypeTabs: ['PTS', 'AST', 'REB', 'PTS+AST', '3PM'],
      selectedStat: 'PTS',
      stats: [
        { date: '4/4', opp: '@ GSW', value: 32 },
        { date: '4/6', opp: 'vs DEN', value: 28 },
        { date: '4/8', opp: 'vs PHX', value: 35 },
        { date: '4/11', opp: '@ NYK', value: 40 },
        { date: '4/20', opp: 'vs MIA', value: 29 },
        { date: '4/23', opp: 'vs MIA', value: 31 },
        { date: '4/26', opp: '@ MIA', value: 27 },
        { date: '4/28', opp: '@ MIA', value: 36 },
        { date: '5/4', opp: 'vs IND', value: 30 },
        { date: '5/6', opp: 'vs IND', value: 38 },
      ],
      line: 28.5,
      overPercent: 80,
      gameLog: [
        { player: 'Luka Dončić', result: 38, line: 28.5, odds: '20/21', hit: true },
        { player: 'Luka Dončić', result: 30, line: 28.5, odds: '21/20', hit: true },
        { player: 'Luka Dončić', result: 27, line: 28.5, odds: '19/20', hit: false },
      ],
    },
    {
      name: 'LeBron James',
      team: 'Lakers',
      position: 'SF',
      photo: 'https://cdn.nba.com/headshots/nba/latest/1040x760/2544.png',
      statTabs: ['H2H', 'L5', 'L10', '2024', '2023'],
      statTypeTabs: ['PTS', 'AST', 'REB'],
      selectedStat: 'PTS',
      stats: [
        { date: '4/4', opp: '@ GSW', value: 28 },
        { date: '4/6', opp: 'vs DEN', value: 25 },
        { date: '4/8', opp: 'vs PHX', value: 30 },
        { date: '4/11', opp: '@ NYK', value: 27 },
        { date: '4/20', opp: 'vs MIA', value: 32 },
      ],
      line: 26.5,
      overPercent: 75,
      gameLog: [
        { player: 'LeBron James', result: 32, line: 26.5, odds: '20/21', hit: true },
        { player: 'LeBron James', result: 25, line: 26.5, odds: '21/20', hit: false },
      ],
    },
  ],
  NFL: [
    {
      name: 'Patrick Mahomes',
      team: 'Chiefs',
      position: 'QB',
      photo: 'https://static.www.nfl.com/image/private/t_headshot_desktop/league/tx9z5gkqkqj7gkqj7gkq',
      statTabs: ['L5', 'L10', '2024', '2023'],
      statTypeTabs: ['PASS YDS', 'TD', 'INT'],
      selectedStat: 'PASS YDS',
      stats: [
        { date: '9/10', opp: 'vs DET', value: 305 },
        { date: '9/17', opp: '@ JAX', value: 285 },
        { date: '9/24', opp: 'vs CHI', value: 272 },
        { date: '10/1', opp: '@ NYJ', value: 249 },
        { date: '10/8', opp: '@ MIN', value: 281 },
      ],
      line: 275.5,
      overPercent: 60,
      gameLog: [
        { player: 'Patrick Mahomes', result: 305, line: 275.5, odds: '10/11', hit: true },
        { player: 'Patrick Mahomes', result: 249, line: 275.5, odds: '10/11', hit: false },
      ],
    },
  ],
  MLB: [
    {
      name: 'Shohei Ohtani',
      team: 'Dodgers',
      position: 'DH',
      photo: 'https://content.mlb.com/images/headshots/current/60x60/660271.png',
      statTabs: ['L5', 'L10', '2024', '2023'],
      statTypeTabs: ['HR', 'RBI', 'AVG'],
      selectedStat: 'HR',
      stats: [
        { date: '5/1', opp: '@ SD', value: 1 },
        { date: '5/2', opp: 'vs SF', value: 0 },
        { date: '5/3', opp: 'vs ARI', value: 2 },
        { date: '5/4', opp: 'vs ARI', value: 1 },
        { date: '5/5', opp: '@ SD', value: 0 },
      ],
      line: 1.5,
      overPercent: 50,
      gameLog: [
        { player: 'Shohei Ohtani', result: 2, line: 1.5, odds: '2/1', hit: true },
        { player: 'Shohei Ohtani', result: 0, line: 1.5, odds: '2/1', hit: false },
      ],
    },
  ],
  Soccer: [
    {
      name: 'Erling Haaland',
      team: 'Man City',
      position: 'ST',
      photo: 'https://resources.premierleague.com/premierleague/photos/players/250x250/p223094.png',
      statTabs: ['L5', 'L10', '2024', '2023'],
      statTypeTabs: ['GOALS', 'ASSISTS', 'MATCHES'],
      selectedStat: 'GOALS',
      stats: [
        { date: '4/1', opp: '@ ARS', value: 2 },
        { date: '4/8', opp: 'vs LIV', value: 1 },
        { date: '4/15', opp: 'vs CHE', value: 0 },
        { date: '4/22', opp: '@ TOT', value: 1 },
        { date: '4/29', opp: 'vs MUN', value: 2 },
      ],
      line: 1.5,
      overPercent: 70,
      gameLog: [
        { player: 'Erling Haaland', result: 2, line: 1.5, odds: '3/2', hit: true },
        { player: 'Erling Haaland', result: 0, line: 1.5, odds: '3/2', hit: false },
      ],
    },
  ],
  // ...add more sports and players as needed
};

interface PlayerType {
  name: string;
  team: string;
  position: string;
  photo: string;
  [key: string]: any;
}

type UserType = { name: string; favorites: PlayerType[]; watchlist: PlayerType[] };

function getUserFromStorage() {
  if (typeof window === 'undefined') return null;
  return JSON.parse(localStorage.getItem('user') || 'null');
}

function updateUser(user: UserType, update: Partial<UserType>): UserType {
  const newUser = { ...user, ...update };
  localStorage.setItem('user', JSON.stringify(newUser));
  return newUser;
}

const sportOptions = [
  { name: "NBA", icon: "🏀" },
  { name: "NFL", icon: "🏈" },
  { name: "MLB", icon: "⚾" },
  { name: "Soccer", icon: "⚽" },
  { name: "Tennis", icon: "🎾" },
  { name: "Esports", icon: "🎮" },
  { name: "Hockey", icon: "🏒" },
  { name: "Golf", icon: "⛳" },
];

// League options for each sport
const leagueOptions: { [key: string]: string[] } = {
  NBA: ["Western Conference", "Eastern Conference"],
  NFL: ["AFC", "NFC"],
  MLB: ["American League", "National League"],
  Soccer: ["Premier League", "La Liga", "Ligue 1", "Bundesliga", "UEFA Champions League", "UEFA Europe League"],
  Tennis: ["ATP", "WTA"],
  Esports: ["LCS", "LEC", "LCK", "LPL"],
  Hockey: ["NHL East", "NHL West"],
  Golf: ["PGA Tour", "European Tour"],
};

// Dynamic news and chart data by sport
const newsBySport: { [key: string]: { source: string; text: string }[] } = {
  NBA: [
    { source: '@wojespn', text: 'Breaking: Luka Dončić drops 40 in playoff win!' },
    { source: '@ESPNStatsInfo', text: 'LeBron James passes Kareem for all-time points.' },
  ],
  NFL: [
    { source: '@ESPNStatsInfo', text: 'Patrick Mahomes now leads the NFL in passing TDs for the 3rd straight year.' },
    { source: '@AdamSchefter', text: 'Chiefs clinch playoff spot with win over Bills.' },
  ],
  MLB: [
    { source: '@MLB', text: 'Shohei Ohtani hits 2 home runs in Dodgers win.' },
    { source: '@JeffPassan', text: 'Yankees sign top free agent pitcher.' },
  ],
  Soccer: [
    { source: '@OptaJoe', text: 'Erling Haaland has scored 10+ goals in 3 consecutive UCL campaigns.' },
    { source: '@FabrizioRomano', text: 'Transfer news: Mbappé to Real Madrid?' },
  ],
};

const chartDataBySport: { [key: string]: { name: string; value: number }[] } = {
  NBA: [
    { name: 'Game 1', value: 28 },
    { name: 'Game 2', value: 32 },
    { name: 'Game 3', value: 25 },
    { name: 'Game 4', value: 40 },
    { name: 'Game 5', value: 36 },
    { name: 'Game 6', value: 30 },
  ],
  NFL: [
    { name: 'Week 1', value: 305 },
    { name: 'Week 2', value: 285 },
    { name: 'Week 3', value: 272 },
    { name: 'Week 4', value: 249 },
    { name: 'Week 5', value: 281 },
  ],
  MLB: [
    { name: 'Game 1', value: 1 },
    { name: 'Game 2', value: 0 },
    { name: 'Game 3', value: 2 },
    { name: 'Game 4', value: 1 },
    { name: 'Game 5', value: 0 },
  ],
  Soccer: [
    { name: 'Match 1', value: 2 },
    { name: 'Match 2', value: 1 },
    { name: 'Match 3', value: 0 },
    { name: 'Match 4', value: 1 },
    { name: 'Match 5', value: 2 },
  ],
};

// Sample favorites/watchlist data
const sampleFavorites = [
  { name: 'Luka Dončić', team: 'Lakers', avatar: '/default-avatar.png', stat: 'PTS: 32.1' },
  { name: 'Shohei Ohtani', team: 'Dodgers', avatar: '/default-avatar.png', stat: 'HR: 44' },
  { name: 'Patrick Mahomes', team: 'Chiefs', avatar: '/default-avatar.png', stat: 'YDS: 4,800' },
];
// Sample live/upcoming matches
const sampleMatches = [
  { teams: 'Lakers vs Warriors', time: '7:30 PM', icon: '🏀' },
  { teams: 'Chiefs vs Eagles', time: '8:15 PM', icon: '🏈' },
  { teams: 'Dodgers vs Yankees', time: '9:00 PM', icon: '⚾' },
];
// Sample recent activity
const sampleActivity = [
  'Added LeBron James to Watchlist',
  'Viewed Lakers vs Celtics',
  'Checked stats for Shohei Ohtani',
  'Favorited Patrick Mahomes',
];
// Sample notifications
const sampleNotifications = [
  'NBA Finals start tomorrow!',
  'Your Watchlist player Luka Dončić scored 38 points!',
  'MLB All-Star Game voting is open.',
];

export default function SportsDashboard() {
  const [selectedSport, setSelectedSport] = useState<string | null>(null);
  const [selectedLeague, setSelectedLeague] = useState<string | null>(null);
  const [fade, setFade] = useState(false);
  const [modalOpen, setModalOpen] = useState(false);
  const [selectedPlayer, setSelectedPlayer] = useState<PlayerType | null>(null);
  const [user, setUser] = useState<UserType | null>(() => getUserFromStorage());
  const [openModal, setOpenModal] = useState<null | 'watch' | 'details'>(null);
  const [selectedMatch, setSelectedMatch] = useState<any>(null);

  const currentPlayers = players[selectedSport || 'NBA'];

  useEffect(() => {
    setFade(true);
    const timeout = setTimeout(() => setFade(false), 300);
    return () => clearTimeout(timeout);
  }, [selectedSport]);

  useEffect(() => {
    if (user) localStorage.setItem('user', JSON.stringify(user));
  }, [user]);

  useEffect(() => {
    const savedSport = typeof window !== 'undefined' ? localStorage.getItem('selectedSport') : null;
    if (savedSport) setSelectedSport(savedSport);
  }, []);

  useEffect(() => {
    if (selectedSport !== null && typeof window !== 'undefined') {
      localStorage.setItem('selectedSport', selectedSport);
    }
  }, [selectedSport]);

  function toggleFavorite(player: PlayerType) {
    if (!user) return;
    const isFav = user.favorites?.some((fav: PlayerType) => fav.name === player.name);
    const newFavs = isFav ? user.favorites.filter((fav: PlayerType) => fav.name !== player.name) : [...(user.favorites || []), player];
    setUser(updateUser(user, { favorites: newFavs }));
  }
  function toggleWatchlist(player: PlayerType) {
    if (!user) return;
    const isWatch = user.watchlist?.some((w: PlayerType) => w.name === player.name);
    const newWatch = isWatch ? user.watchlist.filter((w: PlayerType) => w.name !== player.name) : [...(user.watchlist || []), player];
    setUser(updateUser(user, { watchlist: newWatch }));
  }
  function isFavorite(player: PlayerType) {
    return user?.favorites?.some((fav: PlayerType) => fav.name === player.name);
  }
  function isWatchlisted(player: PlayerType) {
    return user?.watchlist?.some((w: PlayerType) => w.name === player.name);
  }

  // Sample match data for demo
  const nbaMatch = { homeTeam: 'Lakers', awayTeam: 'Warriors', homeLogo: players.NBA[0].photo, awayLogo: '', score: '102 - 98', time: 'Q3 05:12', teams: 'Lakers vs Warriors' };
  const nflMatch = { homeTeam: 'Chiefs', awayTeam: 'Eagles', homeLogo: players.NFL[0].photo, awayLogo: '', score: '21 - 17', time: 'Q2 12:45', teams: 'Chiefs vs Eagles' };
  const mlbMatch = { homeTeam: 'Dodgers', awayTeam: 'Yankees', homeLogo: players.MLB[0].photo, awayLogo: '', score: '5 - 3', time: 'Top 7th', teams: 'Dodgers vs Yankees' };
  const soccerMatch = { homeTeam: 'Man City', awayTeam: 'Real Madrid', homeLogo: players.Soccer[0].photo, awayLogo: '', score: '2 - 1', time: 'UCL - 2nd Half', teams: 'Man City vs Real Madrid' };

  // Use NBA as a default if selectedSport is null or undefined
  const safeSport = selectedSport || 'NBA';

  return (
    <div className="flex min-h-screen bg-gradient-to-br from-gray-950 to-gray-900">
      <main className="flex-1 flex flex-col px-4 md:px-10 lg:px-16 xl:px-24 py-4">
        <TopBar />
        <div className="mt-6 grid grid-cols-1 lg:grid-cols-12 gap-8 flex-1 items-stretch">
          {/* Column 1: Favorites/Watchlist, Sport/League Filter, Quick Stats */}
          <div className="lg:col-span-3 flex flex-col gap-6">
            <div className="bg-gray-900 rounded-2xl shadow-xl p-4">
              <div className="text-lg font-bold mb-2 text-blue-400">Favorites / Watchlist</div>
              <ul className="space-y-2">
                {sampleFavorites.map(fav => (
                  <li key={fav.name} className="flex items-center gap-3">
                    <img src={fav.avatar} alt={fav.name} className="w-8 h-8 rounded-full border-2 border-blue-400" />
                    <div>
                      <div className="font-semibold text-white">{fav.name}</div>
                      <div className="text-xs text-gray-400">{fav.team} • {fav.stat}</div>
                    </div>
                  </li>
                ))}
              </ul>
            </div>
            <div className="bg-gray-900 rounded-2xl shadow-xl p-4">
              <div className="text-lg font-bold mb-2 text-blue-400">Quick Stats</div>
              <ul className="text-gray-300 space-y-1">
                <li>Players Tracked: <b>1,234</b></li>
                <li>Leagues Covered: <b>9</b></li>
                <li>Games Today: <b>17</b></li>
                <li>Favorites: <b>3</b></li>
                <li>Watchlist: <b>4</b></li>
              </ul>
            </div>
          </div>
          {/* Column 2: Dynamic Chart, Live Matches, Top Players, News */}
          <div className="lg:col-span-6 flex flex-col gap-6">
            <div className="bg-gray-900 rounded-2xl shadow-xl p-4">
              <div className="text-lg font-bold mb-2 text-blue-400">Performance Chart</div>
              <SampleChartPanel data={chartDataBySport[safeSport] || []} />
            </div>
            <div className="bg-gray-900 rounded-2xl shadow-xl p-4">
              <div className="text-lg font-bold mb-2 text-blue-400">Live / Upcoming Matches</div>
              <ul className="space-y-2">
                {sampleMatches.map(match => (
                  <li key={match.teams} className="flex items-center gap-3">
                    <span className="text-2xl">{match.icon}</span>
                    <div className="flex-1">
                      <div className="font-semibold text-white">{match.teams}</div>
                      <div className="text-xs text-gray-400">{match.time}</div>
                    </div>
                  </li>
                ))}
              </ul>
            </div>
            <div className="bg-gray-900 rounded-2xl shadow-xl p-4">
              <div className="text-lg font-bold mb-2 text-blue-400">Top Players</div>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                {Array.isArray(currentPlayers) && currentPlayers.length > 0 ? currentPlayers.map(player => (
                  <div key={player.name} onClick={() => { setSelectedPlayer(player); setModalOpen(true); }} className="cursor-pointer">
                    <PlayerCard
                      player={player}
                      isFavorite={Boolean(isFavorite(player))}
                      isWatchlisted={Boolean(isWatchlisted(player))}
                      onFavorite={() => toggleFavorite(player)}
                      onWatchlist={() => toggleWatchlist(player)}
                    />
                  </div>
                )) : <div className="text-gray-400">No players available for this sport yet.</div>}
              </div>
            </div>
            <div className="bg-gray-900 rounded-2xl shadow-xl p-4">
              <div className="text-lg font-bold mb-2 text-blue-400">News & Social Feed</div>
              <NewsFeedPanel player={currentPlayers && currentPlayers[0] ? currentPlayers[0] : undefined} news={newsBySport[safeSport] || []} />
            </div>
          </div>
          {/* Column 3: User Profile, Recent Activity, Notifications */}
          <div className="lg:col-span-3 flex flex-col gap-6">
            <div className="bg-gray-900 rounded-2xl shadow-xl p-4 flex flex-col items-center">
              <img src="/default-avatar.png" alt="User Avatar" className="w-16 h-16 rounded-full border-2 border-blue-400 mb-2" />
              <div className="text-lg font-bold text-white">John Williams</div>
              <div className="text-xs text-gray-400 mb-2">Last activity: 6 Dec, 2025 at 12:43 pm</div>
              <div className="flex gap-4 mt-2">
                <div className="bg-green-900 text-green-300 rounded-xl px-3 py-1 text-xs font-bold">Active</div>
                <div className="bg-red-900 text-red-300 rounded-xl px-3 py-1 text-xs font-bold">Playing</div>
              </div>
              <div className="mt-4 text-center text-gray-300 text-sm">Level: <b>Pro</b> • Streak: <b>5 days</b></div>
            </div>
            <div className="bg-gray-900 rounded-2xl shadow-xl p-4">
              <div className="text-lg font-bold mb-2 text-blue-400">Recent Activity</div>
              <ul className="space-y-2">
                {sampleActivity.map((act, i) => (
                  <li key={i} className="text-gray-300 text-sm">{act}</li>
                ))}
              </ul>
            </div>
            <div className="bg-gray-900 rounded-2xl shadow-xl p-4">
              <div className="text-lg font-bold mb-2 text-blue-400">Notifications / Alerts</div>
              <ul className="space-y-2">
                {sampleNotifications.map((note, i) => (
                  <li key={i} className="text-gray-300 text-sm">{note}</li>
                ))}
              </ul>
            </div>
          </div>
        </div>
        {/* Footer */}
        <footer className="w-full mt-4 py-4 bg-gray-900 rounded-2xl shadow-inner text-center text-gray-500 text-xs opacity-80">
          © {new Date().getFullYear()} Nova Sports Dashboard. All rights reserved.
        </footer>
      </main>
      {/* Render modals */}
      <WatchLiveModal open={openModal === 'watch'} onClose={() => setOpenModal(null)} match={selectedMatch} />
      <MatchDetailsModal open={openModal === 'details'} onClose={() => setOpenModal(null)} match={selectedMatch} onViewPlayer={() => { setOpenModal(null); setSelectedPlayer(players[selectedSport || 'NBA'][0]); setModalOpen(true); }} />
      <PlayerDetailModal open={modalOpen} onClose={() => setModalOpen(false)} player={selectedPlayer} />
    </div>
  );
} 