import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";

const PlayerProfile = () => {
  const { id } = useParams();
  const [player, setPlayer] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!id) return;
    setLoading(true);
    setError(null);
    fetch(`http://localhost:8000/api/v1/nba/players/${id}`)
      .then((res) => {
        if (!res.ok) throw new Error("Failed to fetch player profile");
        return res.json();
      })
      .then((data) => {
        setPlayer(data);
        setLoading(false);
      })
      .catch((err) => {
        setError(err.message);
        setLoading(false);
      });
  }, [id]);

  if (loading) return <div>Loading player profile...</div>;
  if (error) return <div style={{ color: 'red' }}>Error: {error}</div>;
  if (!player) return <div>No player data found.</div>;
  if (player.name === 'No data available') return <div style={{ color: 'orange' }}>No stats available for this player.</div>;

  return (
    <div style={{ margin: 32, background: '#fff', borderRadius: 8, padding: 24, boxShadow: '0 2px 16px rgba(0,0,0,0.08)' }}>
      <h2 style={{ color: '#1976d2' }}>{player.name || player.player_name}</h2>
      <div><strong>Player ID:</strong> {player.id || player.player_id}</div>
      <div><strong>Position:</strong> {player.position || '-'}</div>
      <div><strong>Height:</strong> {player.height || '-'}</div>
      <div><strong>Weight:</strong> {player.weight || '-'}</div>
      <div><strong>Birth Date:</strong> {player.birth_date || '-'}</div>
      <pre style={{ background: '#f6fafd', padding: 12, borderRadius: 6, marginTop: 16, fontSize: 13 }}>{JSON.stringify(player, null, 2)}</pre>
    </div>
  );
};

export default PlayerProfile; 