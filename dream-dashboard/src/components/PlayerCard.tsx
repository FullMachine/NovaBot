"use client";
import React, { useState } from 'react';
import Link from 'next/link';
import { Card } from './ui/card';
import { Button } from './ui/button';
import { defaultAvatar, getSafeImage } from '../lib/utils';

// Define Player type
interface Player {
  name: string;
  team: string;
  position: string;
  photo: string;
}

interface PlayerCardProps {
  player: Player;
  isFavorite: boolean;
  isWatchlisted: boolean;
  onFavorite: () => void;
  onWatchlist: () => void;
}

function slugify(name: string) {
  return name.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/(^-|-$)/g, '');
}

export default function PlayerCard({ player, isFavorite, isWatchlisted, onFavorite, onWatchlist }: PlayerCardProps) {
  const [imgSrc, setImgSrc] = useState(getSafeImage(player.photo));
  const playerId = slugify(player.name);

  return (
    <Card className="bg-gray-900 border border-blue-900 text-white p-6 flex flex-col justify-between items-stretch rounded-2xl shadow-xl transition-all min-w-[260px] max-w-[340px] w-full mx-auto pb-8 h-full">
      <img
        src={imgSrc}
        alt={player.name}
        onError={() => setImgSrc(getSafeImage(undefined))}
        className="w-20 h-20 object-cover rounded-full border-2 border-blue-400 mb-2 shadow mx-auto"
        style={{ aspectRatio: '1/1', minWidth: 80, minHeight: 80, maxWidth: 80, maxHeight: 80 }}
      />
      <div className="flex flex-col items-center gap-2 w-full">
        {/* Standardized: Team (big), Position (smaller), Name (bold) */}
        <h2 className="text-2xl font-bold text-blue-400 text-center leading-tight">{player.team}</h2>
        <span className="text-lg font-medium text-gray-300 text-center">{player.position}</span>
        <p className="text-xl font-semibold text-center text-white leading-tight">{player.name}</p>
      </div>
      {/* Divider above button group, inside the card */}
      <div className="w-full border-t border-blue-900 my-4"></div>
      {/* Button group: always inside the card, stacked vertically, full width */}
      <div className="flex flex-col gap-2 mt-4 w-full">
        <Button className={`w-full py-2 text-center text-base ${isFavorite ? 'bg-blue-400 text-white' : 'bg-gray-800 text-gray-300 border border-blue-400'} rounded-lg font-bold transition hover:bg-blue-500 hover:text-white`} onClick={e => { e.preventDefault(); onFavorite(); }}>{isFavorite ? '★' : '☆'} Favorite</Button>
        <Button className={`w-full py-2 text-center text-base ${isWatchlisted ? 'bg-blue-600 text-white' : 'bg-gray-800 text-gray-300 border border-blue-400'} rounded-lg font-bold transition hover:bg-blue-700 hover:text-white`} onClick={e => { e.preventDefault(); onWatchlist(); }}>{isWatchlisted ? '✓' : '+'} Watchlist</Button>
        <Link href={`/sports/players/${playerId}`} className="w-full">
          <Button className="w-full py-2 text-center text-base bg-blue-600 hover:bg-blue-700 rounded-lg font-bold">View Stats</Button>
        </Link>
      </div>
    </Card>
  );
} 