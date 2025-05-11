"use client";
import PlayerCard from '../../../components/PlayerCard';
import { fakePlayers } from '../../../data/fakePlayers';

export default function GolfDashboard() {
  const golfPlayers = fakePlayers.filter(p => p.sport === 'Golf');
  return (
    <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 p-8 min-h-screen bg-gray-950">
      {/* Live Tournaments */}
      <div className="lg:col-span-3 flex flex-col gap-6">
        <h2 className="text-2xl font-bold text-yellow-400 mb-2">Live Golf Tournaments</h2>
        <div className="bg-gray-900 rounded-2xl shadow-xl p-4 flex flex-col gap-4">
          <div className="text-white">No live golf tournaments right now. Check back later!</div>
        </div>
      </div>
      {/* Golf Tours/News */}
      <div className="lg:col-span-6 flex flex-col gap-6">
        <h2 className="text-2xl font-bold text-blue-400 mb-2">Golf Tours & News</h2>
        <div className="bg-gray-900 rounded-2xl shadow-xl p-4 flex flex-col gap-4">
          <div className="text-white">Golf news and tour standings coming soon!</div>
        </div>
      </div>
      {/* Top Golfers */}
      <div className="lg:col-span-3 flex flex-col gap-6">
        <h2 className="text-2xl font-bold text-purple-400 mb-2">Top Golfers</h2>
        <div className="flex flex-col gap-4">
          {golfPlayers.slice(0, 5).map(player => (
            <PlayerCard key={player.name} player={player} isFavorite={false} isWatchlisted={false} onFavorite={() => {}} onWatchlist={() => {}} />
          ))}
        </div>
      </div>
    </div>
  );
} 