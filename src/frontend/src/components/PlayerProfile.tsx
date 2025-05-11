import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { Box, Card, CardContent, Typography, Avatar, Tabs, Tab, Select, MenuItem, Grid, CircularProgress, AppBar, Toolbar, IconButton, Tooltip, Button, Fade, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, Autocomplete, TextField } from '@mui/material';
import { LineChart, Line, XAxis, YAxis, Tooltip as ReTooltip, ResponsiveContainer, Radar, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis } from 'recharts';
import CompareArrowsIcon from '@mui/icons-material/CompareArrows';
import SportsBasketballIcon from '@mui/icons-material/SportsBasketball';
import PlayerComparison from './PlayerComparison';

interface Player {
  id: string;
  name: string;
  position: string;
  height: string;
  weight: string;
  birth_date: string;
  college?: string;
  team?: string;
  photoUrl?: string;
  bio?: string;
  funFact?: string;
  career_stats?: any;
  season_stats?: any[];
}

const seasons = ["2023-24", "2022-23", "2021-22", "2020-21"];

const PlayerProfile: React.FC = () => {
  const { id } = useParams();
  const [player, setPlayer] = useState<Player | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [season, setSeason] = useState(seasons[0]);
  const [tab, setTab] = useState(0);
  const [allPlayers, setAllPlayers] = useState<Player[]>([]);
  const [comparePlayer, setComparePlayer] = useState<Player | null>(null);
  const [compareLoading, setCompareLoading] = useState(false);

  useEffect(() => {
    if (!id) return;
    setLoading(true);
    setError(null);
    fetch(`/api/v1/nba/players/${id}/stats?season=${season}`)
      .then(res => {
        if (!res.ok) throw new Error('Failed to fetch player profile');
        return res.json();
      })
      .then(data => {
        setPlayer(data);
        setLoading(false);
      })
      .catch(err => {
        setError(err.message);
        setLoading(false);
      });
  }, [id, season]);

  useEffect(() => {
    // Fetch all players for comparison dropdown
    fetch('/api/v1/nba/players/search')
      .then(res => res.json())
      .then(data => setAllPlayers(Array.isArray(data) ? data : []));
  }, []);

  // Fetch compare player data
  useEffect(() => {
    if (!comparePlayer || !comparePlayer.id) return;
    setCompareLoading(true);
    fetch(`/api/v1/nba/players/${comparePlayer.id}/stats?season=${season}`)
      .then(res => res.json())
      .then(data => setComparePlayer(data))
      .finally(() => setCompareLoading(false));
  }, [comparePlayer?.id, season]);

  if (loading) return <Box display="flex" justifyContent="center" alignItems="center" minHeight="60vh"><CircularProgress /></Box>;
  if (error) return <Box color="error.main">Error: {error}</Box>;
  if (!player) return <Box>No player data found.</Box>;
  if (player.name === 'No data available') return <Box color="warning.main">No stats available for this player.</Box>;

  // Example chart data (replace with real stats if available)
  const performanceData = [
    { game: '1', points: 22 },
    { game: '2', points: 28 },
    { game: '3', points: 19 },
    { game: '4', points: 31 },
    { game: '5', points: 25 },
  ];
  const radarData = [
    { stat: 'Scoring', value: 90 },
    { stat: 'Defense', value: 70 },
    { stat: 'Passing', value: 80 },
    { stat: 'Rebounding', value: 75 },
    { stat: 'Athleticism', value: 85 },
  ];

  // Helper: get initials for avatar
  const getInitials = (name: string) => name.split(' ').map(n => n[0]).join('').toUpperCase();

  // Helper: render stats table
  const renderStatsTable = () => {
    if (!player.season_stats || !Array.isArray(player.season_stats) || player.season_stats.length === 0) {
      return <Typography>No stats available for this season.</Typography>;
    }
    const statsSet = player.season_stats[0];
    if (!statsSet.headers || !statsSet.rowSet) return <Typography>No stats available.</Typography>;
    return (
      <TableContainer component={Paper} sx={{ borderRadius: 2, boxShadow: 2, mb: 2 }}>
        <Table size="small">
          <TableHead>
            <TableRow>
              {statsSet.headers.map((header: string) => (
                <TableCell key={header} sx={{ fontWeight: 700 }}>{header}</TableCell>
              ))}
            </TableRow>
          </TableHead>
          <TableBody>
            {statsSet.rowSet.map((row: any[], idx: number) => (
              <TableRow key={idx} hover>
                {row.map((cell, i) => (
                  <TableCell key={i}>{cell}</TableCell>
                ))}
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    );
  };

  return (
    <Box sx={{ bgcolor: 'background.default', color: 'text.primary', minHeight: '100vh', p: { xs: 1, md: 3 } }}>
      <AppBar position="static" color="primary" sx={{ borderRadius: 2, mb: 3 }}>
        <Toolbar>
          <SportsBasketballIcon sx={{ mr: 2 }} />
          <Typography variant="h6" sx={{ flexGrow: 1 }}>NBA Player Profile</Typography>
          <Tooltip title="Compare Players">
            <IconButton color="inherit" onClick={() => setShowComparison(!showComparison)}>
              <CompareArrowsIcon />
            </IconButton>
          </Tooltip>
        </Toolbar>
      </AppBar>
      <Grid container spacing={3}>
        <Grid item xs={12} md={4}>
          <Fade in timeout={800}>
            <Card sx={{ bgcolor: 'background.paper', borderRadius: 3, boxShadow: 4, p: 2, transition: 'box-shadow 0.3s', '&:hover': { boxShadow: 8 } }}>
              <Box display="flex" flexDirection="column" alignItems="center" gap={2}>
                <Avatar src={player.photoUrl} sx={{ width: 120, height: 120, mb: 1, boxShadow: 2, fontSize: 40 }}>
                  {!player.photoUrl && getInitials(player.name)}
                </Avatar>
                <Typography variant="h5" fontWeight={700}>{player.name}</Typography>
                <Typography variant="subtitle1" color="text.secondary">{player.team} | {player.position}</Typography>
                <Typography variant="body2">Height: {player.height} | Weight: {player.weight}</Typography>
                <Typography variant="body2">Born: {player.birth_date}</Typography>
                {player.college && <Typography variant="body2">College: {player.college}</Typography>}
                {player.funFact && <Typography variant="body2" color="secondary">Fun Fact: {player.funFact}</Typography>}
                <Select value={season} onChange={e => setSeason(e.target.value as string)} sx={{ mt: 2, bgcolor: 'background.default', color: 'text.primary', borderRadius: 2 }}>
                  {seasons.map(s => <MenuItem key={s} value={s}>{s}</MenuItem>)}
                </Select>
              </Box>
            </Card>
          </Fade>
        </Grid>
        <Grid item xs={12} md={8}>
          <Fade in timeout={800}>
            <Card sx={{ bgcolor: 'background.paper', borderRadius: 3, boxShadow: 4, transition: 'box-shadow 0.3s', '&:hover': { boxShadow: 8 } }}>
              <Tabs value={tab} onChange={(_, v) => setTab(v)} textColor="primary" indicatorColor="primary" sx={{ borderBottom: 1, borderColor: 'divider' }}>
                <Tab label="Stats" />
                <Tab label="Performance" />
                <Tab label="Bio" />
                <Tab label="Comparison" />
              </Tabs>
              <CardContent>
                {tab === 0 && (
                  <Box>
                    <Typography variant="h6" sx={{ mb: 2 }}>Season Stats</Typography>
                    {renderStatsTable()}
                  </Box>
                )}
                {tab === 1 && (
                  <Box>
                    <Typography variant="h6" sx={{ mb: 2 }}>Performance Trend</Typography>
                    <ResponsiveContainer width="100%" height={300}>
                      <LineChart data={performanceData}>
                        <XAxis dataKey="game" />
                        <YAxis />
                        <ReTooltip />
                        <Line type="monotone" dataKey="points" stroke="#1976d2" strokeWidth={3} />
                      </LineChart>
                    </ResponsiveContainer>
                    <Typography variant="h6" sx={{ mt: 4, mb: 2 }}>Skill Breakdown</Typography>
                    <ResponsiveContainer width="100%" height={250}>
                      <RadarChart cx="50%" cy="50%" outerRadius="80%" data={radarData}>
                        <PolarGrid />
                        <PolarAngleAxis dataKey="stat" />
                        <PolarRadiusAxis angle={30} domain={[0, 100]} />
                        <Radar name="Skill" dataKey="value" stroke="#1976d2" fill="#1976d2" fillOpacity={0.6} />
                      </RadarChart>
                    </ResponsiveContainer>
                  </Box>
                )}
                {tab === 2 && (
                  <Box>
                    <Typography variant="h6" sx={{ mb: 2 }}>Bio</Typography>
                    <Typography variant="body1">{player.bio || 'No bio available.'}</Typography>
                    {player.funFact && <Typography variant="body2" color="secondary" sx={{ mt: 2 }}>Fun Fact: {player.funFact}</Typography>}
                  </Box>
                )}
                {tab === 3 && (
                  <Box>
                    <Box sx={{ mb: 2 }}>
                      <Autocomplete
                        options={allPlayers.filter(p => p.id !== player.id)}
                        getOptionLabel={option => option.name || ''}
                        value={comparePlayer}
                        onChange={(_, value) => setComparePlayer(value)}
                        renderInput={params => <TextField {...params} label="Compare with..." variant="outlined" />}
                        sx={{ width: 300, mb: 2 }}
                      />
                    </Box>
                    {comparePlayer && !compareLoading && (
                      <PlayerComparison player1={player} player2={comparePlayer} season={season} />
                    )}
                    {compareLoading && <CircularProgress />}
                    {!comparePlayer && <Typography variant="body2" color="text.secondary">Select another player to compare.</Typography>}
                  </Box>
                )}
              </CardContent>
            </Card>
          </Fade>
        </Grid>
      </Grid>
    </Box>
  );
};

export default PlayerProfile; 