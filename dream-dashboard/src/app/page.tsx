'use client';
import React, { useState, useEffect, useRef } from "react";
import Sidebar from "../components/Sidebar";
import { Card } from "../components/ui/card";
import { Button } from "../components/ui/button";
import TrendsPanel from "../components/TrendsPanel";
import StreaksPanel from "../components/StreaksPanel";
import GameSimulationPanel from "../components/GameSimulationPanel";
import SampleChartPanel from "../components/SampleChartPanel";
import TopFilterBar from "../components/TopFilterBar";
import WatchlistPanel from "../components/WatchlistPanel";
import ComparisonPanel from "../components/ComparisonPanel";
import AIPicksPanel from "../components/AIPicksPanel";
import AnimatedStatsPanel from "../components/AnimatedStatsPanel";
import NewsFeedPanel from "../components/NewsFeedPanel";
import ThemeSwitcher from "../components/ThemeSwitcher";
import QuickSearchBar from "../components/QuickSearchBar";
import PlayerDetailModal from "../components/PlayerDetailModal";
import PlayerCard from "../components/PlayerCard";
import Link from "next/link";
import { fakePlayers } from "../data/fakePlayers";
import { slugify } from "../lib/utils";

const players = {
  NBA: {
    name: 'Luka Dončić',
    team: 'Mavericks',
    position: 'PG',
    photo: 'https://cdn.nba.com/headshots/nba/latest/1040x760/1629029.png',
    statTabs: ['H2H', 'L5', 'L10', 'L20', '2024', '2023'],
    statTypeTabs: ['PTS', 'AST', 'REB', 'PTS+AST', '3PM'],
    selectedStat: 'PTS',
    stats: [
      { date: '4/4', opp: '@ SAS', value: 32 },
      { date: '4/6', opp: 'vs SAC', value: 28 },
      { date: '4/8', opp: 'vs CHI', value: 35 },
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
  NFL: {
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
  MLB: {
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
  Soccer: {
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
  Tennis: {
    name: 'Iga Świątek',
    team: 'Poland',
    position: 'WTA',
    photo: 'https://www.wtatennis.com/-/media/tennis/players/wta/2023/05/19/14/19/iga-swiatek-2023-madrid.jpg',
    statTabs: ['L5', 'L10', '2024', '2023'],
    statTypeTabs: ['WINS', 'LOSSES', 'TITLES'],
    selectedStat: 'WINS',
    stats: [
      { date: '5/1', opp: 'vs SAB', value: 2 },
      { date: '5/3', opp: 'vs RYB', value: 2 },
      { date: '5/5', opp: 'vs JAB', value: 1 },
      { date: '5/7', opp: 'vs KRE', value: 2 },
      { date: '5/9', opp: 'vs GRA', value: 2 },
    ],
    line: 1.5,
    overPercent: 90,
    gameLog: [
      { player: 'Iga Świątek', result: 2, line: 1.5, odds: '1/2', hit: true },
      { player: 'Iga Świątek', result: 1, line: 1.5, odds: '1/2', hit: false },
    ],
  },
  Esports: {
    name: 'Faker',
    team: 'T1',
    position: 'MID',
    photo: 'https://static.wikia.nocookie.net/lolesports_gamepedia_en/images/7/7e/T1_Faker_2023_Split_2.png',
    statTabs: ['L5', 'L10', '2024', '2023'],
    statTypeTabs: ['KDA', 'WINS', 'MATCHES'],
    selectedStat: 'KDA',
    stats: [
      { date: '4/1', opp: 'vs GEN', value: 5.2 },
      { date: '4/8', opp: 'vs DK', value: 4.8 },
      { date: '4/15', opp: 'vs HLE', value: 3.9 },
      { date: '4/22', opp: 'vs KT', value: 6.1 },
      { date: '4/29', opp: 'vs DRX', value: 4.5 },
    ],
    line: 4.5,
    overPercent: 75,
    gameLog: [
      { player: 'Faker', result: 6.1, line: 4.5, odds: '1.8', hit: true },
      { player: 'Faker', result: 3.9, line: 4.5, odds: '1.8', hit: false },
    ],
  },
  Hockey: {
    name: 'Connor McDavid',
    team: 'Oilers',
    position: 'C',
    photo: 'https://cms.nhl.bamgrid.com/images/headshots/current/168x168/8478402.jpg',
    statTabs: ['L5', 'L10', '2024', '2023'],
    statTypeTabs: ['GOALS', 'ASSISTS', 'POINTS'],
    selectedStat: 'POINTS',
    stats: [
      { date: '4/1', opp: '@ CGY', value: 2 },
      { date: '4/8', opp: 'vs VAN', value: 1 },
      { date: '4/15', opp: 'vs WPG', value: 3 },
      { date: '4/22', opp: '@ SEA', value: 2 },
      { date: '4/29', opp: 'vs LAK', value: 2 },
    ],
    line: 1.5,
    overPercent: 85,
    gameLog: [
      { player: 'Connor McDavid', result: 3, line: 1.5, odds: '2.2', hit: true },
      { player: 'Connor McDavid', result: 1, line: 1.5, odds: '2.2', hit: false },
    ],
  },
  Golf: {
    name: 'Scottie Scheffler',
    team: 'USA',
    position: 'PGA',
    photo: 'https://www.pgatour.com/content/dam/pgatour/players/playerheadshots/46046.png',
    statTabs: ['L5', 'L10', '2024', '2023'],
    statTypeTabs: ['WINS', 'TOP 10s', 'ROUNDS'],
    selectedStat: 'WINS',
    stats: [
      { date: '4/1', opp: 'Masters', value: 1 },
      { date: '4/8', opp: 'RBC', value: 0 },
      { date: '4/15', opp: 'Zurich', value: 1 },
      { date: '4/22', opp: 'Wells Fargo', value: 0 },
      { date: '4/29', opp: 'PGA', value: 1 },
    ],
    line: 0.5,
    overPercent: 60,
    gameLog: [
      { player: 'Scottie Scheffler', result: 1, line: 0.5, odds: '2.5', hit: true },
      { player: 'Scottie Scheffler', result: 0, line: 0.5, odds: '2.5', hit: false },
    ],
  },
};

type PlayerType = typeof players.NBA;
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

function createUser(name: string): UserType {
  // If no user exists in localStorage, this is the owner
  const isFirstUser = !localStorage.getItem('user');
  const newUser = { name, isOwner: isFirstUser, favorites: [], watchlist: [] };
  localStorage.setItem('user', JSON.stringify(newUser));
  return newUser;
}

// Sample top games and news data
const topGames = [
  { sport: 'NBA', teams: 'Lakers vs Celtics', time: '7:00 PM ET', status: 'Live', id: 1 },
  { sport: 'NFL', teams: 'Chiefs vs Bills', time: '8:30 PM ET', status: 'Upcoming', id: 2 },
  { sport: 'Soccer', teams: 'Man City vs Real Madrid', time: '2:00 PM ET', status: 'Final', id: 3 },
];
const newsFeed = [
  { headline: 'Luka Dončić drops 38 in win over Pacers', sport: 'NBA', id: 1 },
  { headline: 'Patrick Mahomes throws 4 TDs in comeback', sport: 'NFL', id: 2 },
  { headline: 'Shohei Ohtani hits 2 HRs, Dodgers win', sport: 'MLB', id: 3 },
];

export default function Home() {
  const [selectedSport, setSelectedSport] = useState<string | null>(null);
  // Fade-in animation state
  const [fade, setFade] = useState(false);
  const [modalOpen, setModalOpen] = useState(false);
  const [selectedPlayer, setSelectedPlayer] = useState<PlayerType | null>(null);
  const [user, setUser] = useState<UserType | null>(() => getUserFromStorage());
  const [showLogin, setShowLogin] = useState(false);
  const loginInputRef = useRef<HTMLInputElement>(null);
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

  // Helper functions for favorites/watchlist
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

  return (
    <div className="flex flex-col min-h-screen bg-gray-950 items-center justify-start w-full">
      <Card className="max-w-lg w-full flex flex-col items-center gap-6 p-10 mt-8 mb-8">
        <h1 className="text-3xl font-bold mb-2">Welcome{user ? `, ${user.name}` : ''}!</h1>
        {user ? (
          <>
            <div className="w-full">
              <div className="font-semibold mb-1">Favorites:</div>
              <ul className="list-disc list-inside ml-2 mb-2">
                {user.favorites && user.favorites.length > 0 ? user.favorites.map((fav: PlayerType) => (
                  <li key={fav.name}>★ {fav.name}</li>
                )) : <li className="text-gray-400">None</li>}
              </ul>
              <div className="font-semibold mb-1">Watchlist:</div>
              <ul className="list-disc list-inside ml-2">
                {user.watchlist && user.watchlist.length > 0 ? user.watchlist.map((w: PlayerType) => (
                  <li key={w.name}>👁️ {w.name}</li>
                )) : <li className="text-gray-400">None</li>}
              </ul>
            </div>
            <Link href="/sports">
              <Button className="bg-yellow-400 text-black text-lg px-8 py-3 rounded-xl font-bold mt-4 hover:bg-yellow-300 transition">Go to Sports Dashboard</Button>
            </Link>
          </>
        ) : (
          <Button className="bg-purple-700 text-white px-4 py-2 rounded-full" onClick={() => setShowLogin(true)}>Login / Signup</Button>
        )}
      </Card>
      {/* Trending Players Section */}
      <div className="w-full max-w-5xl mx-auto grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-10">
        <div className="col-span-1 bg-gray-900 rounded-2xl shadow-xl p-6">
          <h2 className="text-xl font-bold text-purple-400 mb-4">Trending Players</h2>
          <div className="flex flex-col gap-3">
            {fakePlayers.slice(0, 5).map((player, i: number) => (
              <Link key={player.name} href={`/sports/players/${slugify(player.name)}`} className="flex items-center gap-3 hover:bg-gray-800 rounded-lg p-2 transition">
                <img src={player.photo} alt={player.name} className="w-10 h-10 rounded-full object-cover border border-purple-300" onError={e => { e.currentTarget.onerror = null; e.currentTarget.src = '/default-avatar.png'; }} />
                <div>
                  <div className="font-bold text-white">{player.name}</div>
                  <div className="text-xs text-gray-400">{player.team} • {player.sport}</div>
                </div>
              </Link>
            ))}
          </div>
        </div>
        {/* Top Games Section */}
        <div className="col-span-1 bg-gray-900 rounded-2xl shadow-xl p-6">
          <h2 className="text-xl font-bold text-blue-400 mb-4">Top Games</h2>
          <div className="flex flex-col gap-3">
            {topGames.map((game: any, i: number) => (
              <div key={game.id} className="flex items-center gap-3">
                <span className="text-lg">{game.sport === 'NBA' ? '🏀' : game.sport === 'NFL' ? '🏈' : game.sport === 'Soccer' ? '⚽' : '🎮'}</span>
                <div className="flex-1">
                  <div className="font-bold text-white">{game.teams}</div>
                  <div className="text-xs text-gray-400">{game.time} • {game.status}</div>
                </div>
                <span className={`text-xs font-bold ${game.status === 'Live' ? 'text-green-400' : game.status === 'Upcoming' ? 'text-yellow-400' : 'text-gray-400'}`}>{game.status}</span>
              </div>
            ))}
          </div>
        </div>
        {/* News Feed Section */}
        <div className="col-span-1 bg-gray-900 rounded-2xl shadow-xl p-6">
          <h2 className="text-xl font-bold text-pink-400 mb-4">Latest News</h2>
          <div className="flex flex-col gap-3">
            {newsFeed.map((news: any, i: number) => (
              <div key={news.id} className="flex items-center gap-3">
                <span className="text-lg">📰</span>
                <div>
                  <div className="font-bold text-white">{news.headline}</div>
                  <div className="text-xs text-gray-400">{news.sport}</div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
      {/* Login Modal (UI only) */}
      {showLogin && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-60">
          <div className="bg-white dark:bg-gray-900 rounded-2xl shadow-xl w-full max-w-xs mx-auto p-6 relative animate-fadeIn flex flex-col items-center">
            <button className="absolute top-2 right-4 text-2xl" onClick={() => setShowLogin(false)}>×</button>
            <h2 className="text-lg font-bold mb-4 text-purple-700 dark:text-purple-300">Login / Signup</h2>
            <input ref={loginInputRef} className="w-full mb-3 px-3 py-2 rounded border border-purple-300 dark:bg-gray-800 dark:text-white" placeholder="Enter your name" />
            <Button className="w-full bg-purple-700 text-white" onClick={() => {
              const name = loginInputRef.current?.value;
              if (name) { setUser(createUser(name)); setShowLogin(false); }
            }}>Continue</Button>
          </div>
        </div>
      )}
    </div>
  );
}
