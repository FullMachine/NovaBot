import React from 'react';

export default function WatchLiveModal({
  open,
  onClose,
  match,
}: {
  open: boolean;
  onClose: () => void;
  match: any;
}) {
  if (!open) return null;
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-60" onClick={onClose}>
      <div className="bg-white dark:bg-gray-900 rounded-2xl shadow-xl w-full max-w-md sm:max-w-lg mx-auto p-0 relative animate-fadeIn" style={{ minWidth: 320, maxWidth: 400, width: '90vw' }} onClick={e => e.stopPropagation()}>
        <button className="absolute top-4 right-4 text-2xl" onClick={onClose}>×</button>
        <div className="flex flex-col items-center p-8">
          <div className="text-xl font-bold mb-4 text-purple-700 dark:text-purple-300">Watch Live</div>
          {/* Sample video or coming soon */}
          <div className="w-full aspect-video bg-gray-200 dark:bg-gray-800 rounded-lg flex items-center justify-center mb-4">
            <span className="text-lg text-gray-500">Live stream coming soon!</span>
          </div>
          <div className="text-center text-gray-600 dark:text-gray-300 mb-2">{match?.teams || 'Match'} is not live yet. Check back soon!</div>
        </div>
      </div>
    </div>
  );
} 