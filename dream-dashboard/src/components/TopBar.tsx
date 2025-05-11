import React, { useState } from 'react';
import { defaultAvatar, getSafeImage } from '../lib/utils';

const aiAvatars = [
  'https://cdn.jsdelivr.net/gh/edent/SuperTinyIcons/images/svg/robot.svg', // Reliable SVG robot icon
];
const aiNames = ['SportsAI'];

function getRandomAI() {
  return { avatar: aiAvatars[0], name: aiNames[0] };
}

export default function TopBar({ customAvatar }: { customAvatar?: any }) {
  const [aiUser] = useState(getRandomAI());
  const [search, setSearch] = useState('');
  const [avatarSrc, setAvatarSrc] = useState('https://images.unsplash.com/photo-1517649763962-0c623066013b?auto=format&fit=facearea&w=256&h=256&facepad=2&q=80');

  // Get current date/time for display
  const now = new Date();
  const dateString = now.toLocaleString('en-US', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric', hour: '2-digit', minute: '2-digit' });

  // Demo handlers
  function handleFilter() {
    window.alert('Filter feature coming soon! (Demo)');
  }
  function handleBell() {
    window.alert('No new notifications. (Demo)');
  }
  function handleSearch(e: React.FormEvent) {
    e.preventDefault();
    window.alert(`Searching for: ${search} (Demo)`);
  }

  return (
    <div className="flex items-center justify-between gap-6 mb-8 px-8 py-2 bg-gradient-to-br from-gray-900 via-gray-950 to-gray-900/95 rounded-2xl shadow-xl border-b-2 border-blue-900 sticky top-0 z-50 backdrop-blur-md">
      {/* Left: Filter + Search */}
      <div className="flex items-center gap-0">
        <button
          className="bg-[#23272f] text-blue-400 font-bold px-6 py-2 rounded-l-xl border-0 focus:ring-2 focus:ring-blue-400 hover:bg-blue-400 hover:text-white transition text-base flex items-center"
          onClick={handleFilter}
          style={{ borderTopRightRadius: 0, borderBottomRightRadius: 0 }}
        >
          Filter <span className="ml-2 text-lg">▼</span>
        </button>
        <form className="relative" onSubmit={handleSearch} autoComplete="off">
          <input
            className="bg-[#23272f] text-white px-6 py-2 rounded-r-xl border-0 focus:ring-2 focus:ring-blue-400 w-[340px] pr-10 transition-all shadow-inner placeholder-gray-400 text-base"
            type="text"
            placeholder="Search by events, teams, or leagues..."
            value={search}
            onChange={e => setSearch(e.target.value)}
            style={{ borderTopLeftRadius: 0, borderBottomLeftRadius: 0 }}
          />
          <button type="submit" className="absolute right-3 top-1/2 -translate-y-1/2 text-blue-300 text-xl hover:text-blue-400 focus:outline-none" tabIndex={-1} aria-label="Search">
            <span role="img" aria-label="search">🔍</span>
          </button>
        </form>
      </div>
      {/* Center: Date/time */}
      <div className="text-gray-200 font-medium text-base text-center flex-1 flex justify-center">
        {dateString}
      </div>
      {/* Right: SportsAI button + Bell */}
      <div className="flex items-center gap-3">
        <div className="flex items-center gap-2 px-4 py-1 rounded-full border-2 border-blue-400 bg-[#23272f] shadow text-blue-400 font-bold text-base transition-all duration-150 hover:bg-blue-400 hover:text-white" style={{ minWidth: 120 }}>
          <img src={avatarSrc} alt="AI User" className="w-7 h-7 rounded-full border-2 border-blue-400 bg-blue-300 object-cover" />
          <span className="ml-2">{aiUser.name}</span>
        </div>
        <button className="bg-transparent rounded-full p-0.5 text-blue-400 text-lg hover:bg-blue-400 hover:text-white transition shadow-none ml-2" style={{ minWidth: 24, minHeight: 24 }} onClick={handleBell} aria-label="Notifications">
          <span role="img" aria-label="bell">🔔</span>
        </button>
      </div>
    </div>
  );
} 