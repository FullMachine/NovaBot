'use client';

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

export default function Home() {
  return (
    <div className="flex min-h-screen bg-gray-950">
      <Sidebar />
      <main className="flex-1 p-8">
        <ThemeSwitcher />
        <QuickSearchBar />
        <TopFilterBar />
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {/* Player Card Example */}
          <Card className="bg-white text-black dark:bg-gray-900 dark:text-white p-6 flex flex-col items-center">
            <span className="text-5xl mb-2">🏀</span>
            <h2 className="text-lg font-bold mb-1 text-purple-700 dark:text-purple-400">NBA Player</h2>
            <p className="mb-2 text-base font-medium">Luka Dončić</p>
            <Button className="bg-purple-600 hover:bg-purple-700 w-full" onClick={() => window.alert('Stats for Luka Dončić coming soon!')}>View Stats</Button>
          </Card>
          <Card className="bg-white text-black dark:bg-gray-900 dark:text-white p-6 flex flex-col items-center">
            <span className="text-5xl mb-2">🏈</span>
            <h2 className="text-lg font-bold mb-1 text-purple-700 dark:text-purple-400">NFL Player</h2>
            <p className="mb-2 text-base font-medium">Patrick Mahomes</p>
            <Button className="bg-purple-600 hover:bg-purple-700 w-full" onClick={() => window.alert('Stats for Patrick Mahomes coming soon!')}>View Stats</Button>
          </Card>
          <Card className="bg-white text-black dark:bg-gray-900 dark:text-white p-6 flex flex-col items-center">
            <span className="text-5xl mb-2">⚾</span>
            <h2 className="text-lg font-bold mb-1 text-purple-700 dark:text-purple-400">MLB Player</h2>
            <p className="mb-2 text-base font-medium">Shohei Ohtani</p>
            <Button className="bg-purple-600 hover:bg-purple-700 w-full" onClick={() => window.alert('Stats for Shohei Ohtani coming soon!')}>View Stats</Button>
          </Card>
          <TrendsPanel />
          <StreaksPanel />
          <GameSimulationPanel />
          <SampleChartPanel />
          <WatchlistPanel />
          <ComparisonPanel />
          <AIPicksPanel />
          <AnimatedStatsPanel />
          <NewsFeedPanel />
          <Card className="bg-white text-black dark:bg-gray-900 dark:text-white p-6 flex flex-col items-center">
            <span className="text-5xl mb-2">⚽</span>
            <h2 className="text-lg font-bold mb-1 text-purple-700 dark:text-purple-400">Soccer Player</h2>
            <p className="mb-2 text-base font-medium">Erling Haaland</p>
            <Button className="bg-purple-600 hover:bg-purple-700 w-full" onClick={() => window.alert('Stats for Erling Haaland coming soon!')}>View Stats</Button>
          </Card>
          <Card className="bg-white text-black dark:bg-gray-900 dark:text-white p-6 flex flex-col items-center">
            <span className="text-5xl mb-2">🎾</span>
            <h2 className="text-lg font-bold mb-1 text-purple-700 dark:text-purple-400">Tennis Player</h2>
            <p className="mb-2 text-base font-medium">Iga Świątek</p>
            <Button className="bg-purple-600 hover:bg-purple-700 w-full" onClick={() => window.alert('Stats for Iga Świątek coming soon!')}>View Stats</Button>
          </Card>
          <Card className="bg-white text-black dark:bg-gray-900 dark:text-white p-6 flex flex-col items-center">
            <span className="text-5xl mb-2">🎮</span>
            <h2 className="text-lg font-bold mb-1 text-purple-700 dark:text-purple-400">Esports Player</h2>
            <p className="mb-2 text-base font-medium">Faker</p>
            <Button className="bg-purple-600 hover:bg-purple-700 w-full" onClick={() => window.alert('Stats for Faker coming soon!')}>View Stats</Button>
          </Card>
        </div>
      </main>
    </div>
  );
}
 