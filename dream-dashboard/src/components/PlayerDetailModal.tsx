'use client';

import React, { useState, useMemo } from 'react';
import { Card } from './ui/card';
import { Button } from './ui/button';
import { defaultAvatar, getSafeImage } from '../lib/utils';

function calculateAvg(stats: any[]) {
  if (!stats || stats.length === 0) return 0;
  const sum = stats.reduce((a, b) => a + (b.value || b), 0);
  return (sum / stats.length).toFixed(1);
}
function calculateMedian(stats: any[]) {
  if (!stats || stats.length === 0) return 0;
  const values = stats.map(s => s.value !== undefined ? s.value : s).sort((a, b) => a - b);
  const mid = Math.floor(values.length / 2);
  return values.length % 2 !== 0 ? values[mid] : ((values[mid - 1] + values[mid]) / 2).toFixed(1);
}

export default function PlayerDetailModal({
  open,
  onClose,
  player,
}: {
  open: boolean;
  onClose: () => void;
  player: any;
}) {
  const [selectedTab, setSelectedTab] = useState(player?.statTabs?.[0] || 'L5');
  const [selectedStat, setSelectedStat] = useState(player?.statTypeTabs?.[0] || 'PTS');
  const [showAltLines, setShowAltLines] = useState(false);
  const [imgSrc, setImgSrc] = useState(getSafeImage(player?.photo));

  if (!open || !player) return null;

  // For demo: just use player.stats for all tabs (real app: filter by tab)
  const stats = player.stats || [];
  const avg = calculateAvg(stats);
  const median = calculateMedian(stats);
  const dates = stats.map((s: any) => s.date);

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-60" onClick={onClose}>
      <div className="bg-white dark:bg-gray-900 rounded-2xl shadow-xl w-full max-w-md sm:max-w-lg mx-auto p-0 relative animate-fadeIn" style={{ minWidth: 320, maxWidth: 400, width: '90vw' }} onClick={e => e.stopPropagation()}>
        {/* Sticky Top Bar */}
        <div className="sticky top-0 bg-gradient-to-br from-purple-100 to-white dark:from-gray-900 dark:to-gray-800 rounded-t-2xl px-4 pt-4 pb-2 flex flex-col items-center border-b border-purple-200 dark:border-purple-700">
          <button className="absolute top-4 left-4 text-2xl" onClick={onClose}>×</button>
          {/* Compare and Share buttons */}
          <div className="absolute top-4 right-4 flex gap-2">
            <button className="bg-gray-200 dark:bg-gray-700 rounded-full p-2 text-xs" title="Compare (coming soon)">🔀</button>
            <button className="bg-gray-200 dark:bg-gray-700 rounded-full p-2 text-xs" title="Share (coming soon)">🔗</button>
          </div>
          <img src={imgSrc} alt={player.name} onError={() => setImgSrc(getSafeImage(undefined))} className="w-20 h-20 object-cover rounded-full border-2 border-blue-400 mb-2" style={{ aspectRatio: '1/1', minWidth: 80, minHeight: 80, maxWidth: 80, maxHeight: 80 }} />
          <div className="text-xl font-bold text-gray-900 dark:text-white text-center w-full">{player.name}</div>
          <div className="text-sm text-gray-500 text-center w-full">{player.team} | {player.position} - {selectedStat}</div>
        </div>
        {/* Head-to-head stats row (above chart) */}
        <div className="flex justify-between items-center px-4 py-2 mb-1 bg-gray-50 dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-purple-700">
          {player.statTabs && player.statTabs.length > 0 ? (
            player.statTabs.map((tab: any, idx: number) => (
              <div key={tab} className="flex flex-col items-center mx-1">
                <span className={`text-xs font-bold ${selectedTab === tab ? 'text-black dark:text-white' : 'text-gray-500'}`}>{tab}</span>
                {/* Example: color-coded percentage, in real app use real data */}
                <span className={`text-xs font-semibold ${idx % 2 === 0 ? 'text-green-500' : 'text-red-400'}`}>{(20 + idx * 10)}%</span>
              </div>
            ))
          ) : (
            <span className="text-gray-400 text-xs">No stat tabs available</span>
          )}
        </div>
        {/* Stat Tabs */}
        <div className="flex gap-2 mb-2 px-4 overflow-x-auto">
          {player.statTabs && player.statTabs.length > 0 ? (
            player.statTabs.map((tab: any) => (
              <button
                key={tab}
                className={`px-3 py-1 rounded-full text-xs font-bold transition-all duration-150 ${selectedTab === tab ? 'bg-black text-white dark:bg-white dark:text-black shadow' : 'bg-gray-200 dark:bg-gray-800 text-gray-700 dark:text-gray-300'}`}
                onClick={() => setSelectedTab(tab)}
              >
                {tab}
              </button>
            ))
          ) : (
            <span className="text-gray-400 text-xs">No stat tabs available</span>
          )}
        </div>
        {/* Stat Type Tabs */}
        <div className="flex gap-2 mb-2 px-4 overflow-x-auto">
          {player.statTypeTabs && player.statTypeTabs.length > 0 ? (
            player.statTypeTabs.map((tab: any) => (
              <button
                key={tab}
                className={`px-2 py-1 rounded text-xs font-semibold transition-all duration-150 ${selectedStat === tab ? 'bg-purple-600 text-white shadow' : 'bg-gray-100 dark:bg-gray-800 text-gray-600 dark:text-gray-300'}`}
                onClick={() => setSelectedStat(tab)}
              >
                {tab}
              </button>
            ))
          ) : (
            <span className="text-gray-400 text-xs">No stat types available</span>
          )}
        </div>
        {/* Statistics Bar Chart */}
        <div className="mb-4 px-4">
          <div className="flex justify-between text-xs mb-1">
            <span className="font-bold text-green-600">Statistics</span>
            <span>Avg <b>{avg}</b> | Median <b>{median}</b></span>
          </div>
          <div className="relative overflow-x-auto w-full">
            {/* Horizontal line for the 'line' value */}
            <div className="absolute left-0 right-0" style={{ top: `${120 - player.line * 5}px`, height: 0 }}>
              <div className="border-t-2 border-dashed border-purple-400 w-full" style={{ position: 'relative', top: 0 }}></div>
              <span className="absolute right-0 -top-4 text-xs text-purple-500 font-bold">{player.line}</span>
            </div>
            <div className="flex items-end gap-2 h-32 min-w-[260px] max-w-full bg-gradient-to-b from-purple-50 to-white dark:from-gray-800 dark:to-gray-900 rounded-lg p-2" style={{ minWidth: Math.max(260, stats.length * 32) }}>
              {stats.map((s: any, i: number) => (
                <div key={i} className="flex flex-col items-center w-7">
                  <div className={`rounded-t-md w-full ${s.value >= player.line ? 'bg-green-400' : 'bg-red-300'} transition-all duration-200`} style={{ height: `${s.value * 5}px`, minHeight: 10, maxHeight: 120 }}></div>
                  <span className="text-[11px] font-bold text-gray-700 dark:text-gray-200">{s.value}</span>
                  <span className="text-[10px] text-gray-400">{s.date}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
        {/* Supporting Stats Pills */}
        <div className="mb-4 px-4">
          <div className="flex justify-between items-center mb-2">
            <span className="font-bold text-gray-700 dark:text-gray-200">Supporting Stats</span>
            <div className="flex gap-2">
              <button className={`px-2 py-1 rounded-full text-xs font-semibold ${true ? 'bg-black text-white dark:bg-white dark:text-black' : 'bg-gray-200 dark:bg-gray-800 text-gray-700 dark:text-gray-300'}`}>Average</button>
              <button className={`px-2 py-1 rounded-full text-xs font-semibold ${false ? 'bg-black text-white dark:bg-white dark:text-black' : 'bg-gray-200 dark:bg-gray-800 text-gray-700 dark:text-gray-300'}`}>Median</button>
            </div>
          </div>
          <div className="flex flex-wrap gap-2 mb-2">
            {player.supportingStats && player.supportingStats.length > 0 ? (
              player.supportingStats.map((stat: any, i: number) => (
                <span key={i} className="px-3 py-1 rounded-full bg-gray-100 dark:bg-gray-800 text-xs font-medium text-gray-700 dark:text-gray-200">{stat.label}: {stat.value}</span>
              ))
            ) : (
              <span className="text-gray-400 text-xs">No supporting stats available</span>
            )}
          </div>
          <Button className="w-full bg-black text-white dark:bg-purple-700 mt-1" onClick={() => setShowAltLines(true)}>ALT LINES</Button>
        </div>
        {/* ALT LINES Modal */}
        {showAltLines && (
          <div className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-60" onClick={() => setShowAltLines(false)}>
            <div className="bg-white dark:bg-gray-900 rounded-xl p-6 shadow-xl text-center" onClick={e => e.stopPropagation()}>
              <div className="text-lg font-bold mb-2">Alternate lines coming soon!</div>
              <Button className="mt-2 bg-purple-700 text-white" onClick={() => setShowAltLines(false)}>Close</Button>
            </div>
          </div>
        )}
        {/* Game Log Table */}
        <div className="mb-2 px-4">
          <div className="font-bold text-gray-700 dark:text-gray-200 mb-1">Game Log</div>
          <div className="overflow-x-auto">
            {player.gameLog && player.gameLog.length > 0 ? (
              <table className="w-full text-xs">
                <thead>
                  <tr className="bg-gray-100 dark:bg-gray-800">
                    <th className="p-1">Player</th>
                    <th className="p-1">Result</th>
                    <th className="p-1">Line</th>
                    <th className="p-1">Odds</th>
                    <th className="p-1">Hit?</th>
                  </tr>
                </thead>
                <tbody>
                  {player.gameLog.map((g: any, i: number) => (
                    <tr key={i} className="text-center">
                      <td className="p-1">{g.player}</td>
                      <td className="p-1">{g.result}</td>
                      <td className="p-1">O {g.line}</td>
                      <td className="p-1">{g.odds}</td>
                      <td className="p-1">{g.hit ? '✅' : '❌'}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            ) : (
              <span className="text-gray-400 text-xs">No game log data available</span>
            )}
          </div>
        </div>
      </div>
    </div>
  );
} 