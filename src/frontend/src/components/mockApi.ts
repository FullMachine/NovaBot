import axios from 'axios';

// Simple mock data for demo
const mockPlayers = [
  { name: 'LeBron James', id: '2544' },
  { name: 'Stephen Curry', id: '201939' },
  { name: 'Kevin Durant', id: '201142' },
  { name: 'Giannis Antetokounmpo', id: '203507' },
];

type PlayerStat = {
  name: string;
  stats: { [key: string]: number };
};

const mockStats: { [id: string]: PlayerStat } = {
  '2544': {
    name: 'LeBron James',
    stats: { PTS: 27.2, REB: 7.4, AST: 7.3, STL: 1.6, BLK: 0.8 },
  },
  '201939': {
    name: 'Stephen Curry',
    stats: { PTS: 24.8, REB: 4.6, AST: 6.5, STL: 1.7, BLK: 0.2 },
  },
  '201142': {
    name: 'Kevin Durant',
    stats: { PTS: 27.0, REB: 7.1, AST: 4.3, STL: 1.1, BLK: 1.1 },
  },
  '203507': {
    name: 'Giannis Antetokounmpo',
    stats: { PTS: 23.0, REB: 9.8, AST: 4.7, STL: 1.2, BLK: 1.3 },
  },
};

axios.interceptors.request.use((config) => {
  if (config.url?.startsWith('/api/v1/nba/players/search')) {
    console.log('Mock: /api/v1/nba/players/search', config.url);
    const url = new URL(config.url, window.location.origin);
    const query = url.searchParams.get('query')?.toLowerCase() || '';
    const results = mockPlayers.filter(p => p.name.toLowerCase().includes(query));
    config.adapter = async () => ({
      data: { results },
      status: 200,
      statusText: 'OK',
      headers: {},
      config,
    });
    return config;
  }
  if (config.url?.startsWith('/api/v1/nba/compare_players')) {
    const url = new URL(config.url, window.location.origin);
    const player1_id = url.searchParams.get('player1_id') || '';
    const player2_id = url.searchParams.get('player2_id') || '';
    console.log('Mock: /api/v1/nba/compare_players', { player1_id, player2_id });
    config.adapter = async () => ({
      data: {
        player1: mockStats[player1_id] || {},
        player2: mockStats[player2_id] || {},
      },
      status: 200,
      statusText: 'OK',
      headers: {},
      config,
    });
    return config;
  }
  return config;
});

// In your main.tsx, import './components/mockApi' to enable mocks during development. 