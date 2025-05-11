import React from 'react';
import { getSafeImage } from '../lib/utils';

export default function MatchDetailsModal({
  open,
  onClose,
  match,
  onViewPlayer,
}: {
  open: boolean;
  onClose: () => void;
  match: any;
  onViewPlayer: (playerId: string) => void;
}) {
  if (!open) return null;
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-60" onClick={onClose}>
      <div className="bg-white dark:bg-gray-900 rounded-2xl shadow-xl w-full max-w-md sm:max-w-lg mx-auto p-0 relative animate-fadeIn" style={{ minWidth: 320, maxWidth: 400, width: '90vw' }} onClick={e => e.stopPropagation()}>
        <button className="absolute top-4 right-4 text-2xl" onClick={onClose}>×</button>
        <div className="flex flex-col items-center p-8">
          <div className="text-xl font-bold mb-4 text-blue-700 dark:text-blue-300">Match Details</div>
          <div className="flex items-center gap-4 mb-2">
            <img src={getSafeImage(match?.homeLogo)} alt={match?.homeTeam} className="w-10 h-10 rounded-full bg-gray-200" onError={e => { e.currentTarget.onerror = null; e.currentTarget.src = getSafeImage(undefined); }} />
            <span className="font-bold text-lg">{match?.homeTeam || 'Home'}</span>
            <span className="text-lg font-bold text-gray-400">-</span>
            <span className="font-bold text-lg">{match?.awayTeam || 'Away'}</span>
            <img src={getSafeImage(match?.awayLogo)} alt={match?.awayTeam} className="w-10 h-10 rounded-full bg-gray-200" onError={e => { e.currentTarget.onerror = null; e.currentTarget.src = getSafeImage(undefined); }} />
          </div>
          <div className="mb-2 text-gray-600 dark:text-gray-300">{match?.score || '0 - 0'} | {match?.time || 'Q1 00:00'}</div>
          <button className="bg-purple-600 hover:bg-purple-700 text-white font-bold py-2 px-4 rounded-lg mt-4" onClick={() => onViewPlayer('')}>View Player Profiles</button>
        </div>
      </div>
    </div>
  );
} 