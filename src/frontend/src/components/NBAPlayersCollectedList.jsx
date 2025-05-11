import React, { useEffect, useState } from "react";

const modalStyle = {
  position: 'fixed', top: 0, left: 0, width: '100vw', height: '100vh', background: 'rgba(0,0,0,0.4)', display: 'flex', alignItems: 'center', justifyContent: 'center', zIndex: 1000
};
const modalContentStyle = {
  background: '#fff', borderRadius: 8, padding: 24, minWidth: 320, maxWidth: 600, boxShadow: '0 2px 16px rgba(0,0,0,0.2)'
};
const closeBtnStyle = {
  position: 'absolute', top: 16, right: 24, fontSize: 24, cursor: 'pointer', color: '#1976d2', background: 'none', border: 'none'
};

const PAGE_SIZE = 20;
const ANALYTICS_OPTIONS = [
  { label: 'Games Played', value: 'games_played' },
  { label: 'Points', value: 'points' },
  { label: 'Assists', value: 'assists' },
  { label: 'Rebounds', value: 'rebounds' },
];

const NBAPlayersCollectedList = () => {
  const [players, setPlayers] = useState([]);
  const [filteredPlayers, setFilteredPlayers] = useState([]);
  const [search, setSearch] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [modalPlayer, setModalPlayer] = useState(null);
  const [page, setPage] = useState(1);
  const [analyticsStat, setAnalyticsStat] = useState('games_played');

  // Fetch players from backend
  useEffect(() => {
    setLoading(true);
    setError(null);
    // If search is empty, fetch all players; otherwise, search
    const url = search
      ? `http://localhost:8000/api/v1/nba/players/search?name=${encodeURIComponent(search)}`
      : `http://localhost:8000/api/v1/nba/players/search`;
    fetch(url)
      .then((res) => {
        if (!res.ok) throw new Error("Failed to fetch players");
        return res.json();
      })
      .then((data) => {
        setPlayers(Array.isArray(data) ? data : []);
        setLoading(false);
        setPage(1); // reset page on new data
      })
      .catch((err) => {
        setError(err.message);
        setLoading(false);
      });
  }, [search]);

  useEffect(() => {
    setFilteredPlayers(players);
    setPage(1); // reset page on new data
  }, [players]);

  // Pagination logic
  const totalPages = Math.ceil(filteredPlayers.length / PAGE_SIZE);
  const paginatedPlayers = filteredPlayers.slice((page - 1) * PAGE_SIZE, page * PAGE_SIZE);

  // Analytics bar chart logic
  const topPlayers = [...filteredPlayers]
    .sort((a, b) => (b[analyticsStat] || 0) - (a[analyticsStat] || 0))
    .slice(0, 10);
  const maxStat = Math.max(...topPlayers.map((p) => p[analyticsStat] || 0), 1);

  return (
    <div style={{ marginTop: 32, fontFamily: 'system-ui, sans-serif', background: '#f9f9fb', borderRadius: 8, padding: 24 }}>
      <h2 style={{ color: '#1976d2' }}>All Collected NBA Players</h2>
      <div style={{ marginBottom: 16, display: 'flex', alignItems: 'center', gap: 16 }}>
        <input
          type="text"
          placeholder="Search by name..."
          value={search}
          onChange={e => setSearch(e.target.value)}
          style={{ padding: 6, borderRadius: 4, border: '1px solid #ccc', minWidth: 180 }}
        />
      </div>
      {loading && <div>Loading collected NBA players...</div>}
      {error && <div style={{ color: 'red' }}>Error: {error}</div>}
      {!loading && !error && (
        <>
          <table style={{ width: '100%', marginBottom: 12, background: '#fff', borderRadius: 8, boxShadow: '0 1px 4px rgba(0,0,0,0.04)' }}>
            <thead style={{ background: '#e3eafc' }}>
              <tr>
                <th style={{ padding: 8 }}>Name</th>
                <th style={{ padding: 8 }}>Player ID</th>
                <th style={{ padding: 8 }}>Team</th>
                <th style={{ padding: 8 }}>Games Played</th>
              </tr>
            </thead>
            <tbody>
              {paginatedPlayers.map((p) => (
                <tr key={p.id} style={{ cursor: 'pointer', background: '#f6fafd' }} onClick={() => setModalPlayer(p)}>
                  <td style={{ padding: 8 }}>{p.name}</td>
                  <td style={{ padding: 8 }}>{p.id}</td>
                  <td style={{ padding: 8 }}>{p.team || '-'}</td>
                  <td style={{ padding: 8 }}>{p.games_played || '-'}</td>
                </tr>
              ))}
            </tbody>
          </table>
          {/* Pagination controls */}
          <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', gap: 16, marginBottom: 24 }}>
            <button onClick={() => setPage(p => Math.max(1, p - 1))} disabled={page === 1} style={{ padding: '6px 12px', borderRadius: 4, border: '1px solid #1976d2', background: page === 1 ? '#eee' : '#1976d2', color: page === 1 ? '#888' : '#fff', cursor: page === 1 ? 'not-allowed' : 'pointer' }}>Previous</button>
            <span>Page {page} of {totalPages}</span>
            <button onClick={() => setPage(p => Math.min(totalPages, p + 1))} disabled={page === totalPages} style={{ padding: '6px 12px', borderRadius: 4, border: '1px solid #1976d2', background: page === totalPages ? '#eee' : '#1976d2', color: page === totalPages ? '#888' : '#fff', cursor: page === totalPages ? 'not-allowed' : 'pointer' }}>Next</button>
          </div>
          {/* Analytics selector */}
          <div style={{ marginBottom: 8, display: 'flex', alignItems: 'center', gap: 12 }}>
            <label htmlFor="analytics-stat">Bar Chart Stat:</label>
            <select id="analytics-stat" value={analyticsStat} onChange={e => setAnalyticsStat(e.target.value)}>
              {ANALYTICS_OPTIONS.map(opt => (
                <option key={opt.value} value={opt.value}>{opt.label}</option>
              ))}
            </select>
          </div>
          <h3 style={{ color: '#1976d2' }}>Top 10 Players by {ANALYTICS_OPTIONS.find(opt => opt.value === analyticsStat)?.label}</h3>
          <div style={{ display: 'flex', alignItems: 'flex-end', height: 180, gap: 8, marginBottom: 32 }}>
            {topPlayers.map((p) => (
              <div key={p.id} style={{ textAlign: 'center', width: 40 }}>
                <div style={{ background: '#1976d2', height: `${(p[analyticsStat] || 0) / maxStat * 150}px`, width: '100%', borderRadius: 4, marginBottom: 4 }}></div>
                <div style={{ fontSize: 12 }}>{p.name?.split(' ')[1] || p.name}</div>
                <div style={{ fontSize: 10 }}>{p[analyticsStat] || 0}</div>
              </div>
            ))}
          </div>
        </>
      )}
      {modalPlayer && (
        <div style={modalStyle} onClick={() => setModalPlayer(null)}>
          <div style={{ ...modalContentStyle, position: 'relative' }} onClick={e => e.stopPropagation()}>
            <button style={closeBtnStyle} onClick={() => setModalPlayer(null)}>&times;</button>
            <h2 style={{ color: '#1976d2' }}>{modalPlayer.name}</h2>
            <div><strong>Player ID:</strong> {modalPlayer.id}</div>
            <div><strong>Team:</strong> {modalPlayer.team || '-'}</div>
            <div><strong>Games Played:</strong> {modalPlayer.games_played || '-'}</div>
            {/* Add more details here as needed */}
            <pre style={{ background: '#f6fafd', padding: 12, borderRadius: 6, marginTop: 16, fontSize: 13 }}>{JSON.stringify(modalPlayer, null, 2)}</pre>
            <button style={{ marginTop: 16, color: '#fff', background: '#1976d2', border: 'none', borderRadius: 4, padding: '8px 16px', cursor: 'pointer' }} onClick={() => window.location.href = `/player/${modalPlayer.id}`}>View Full Profile</button>
          </div>
        </div>
      )}
    </div>
  );
};

export default NBAPlayersCollectedList; 