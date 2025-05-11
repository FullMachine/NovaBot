import React, { useEffect, useState } from 'react';
import { Paper, Typography, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, CircularProgress, Box } from '@mui/material';
import axios from 'axios';

interface PlayerComparisonProps {
  player1: any;
  player2: any;
  season: string;
}

const PlayerComparison: React.FC<PlayerComparisonProps> = ({ player1, player2, season }) => {
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (player1 && player2 && season) {
      setLoading(true);
      setError(null);
      setData(null);
      axios.get(`/api/v1/nba/compare_players`, {
        params: {
          player1_id: player1.id,
          player2_id: player2.id,
          season: season.split('-')[0], // Use first year for API
        },
      })
        .then(res => {
          console.log('DEBUG: compare_players response', res.data);
          setData(res.data);
        })
        .catch(e => setError('Could not fetch comparison'))
        .finally(() => setLoading(false));
    }
  }, [player1, player2, season]);

  if (!player1 || !player2) return null;

  if (loading) return <Box display="flex" justifyContent="center"><CircularProgress /></Box>;
  if (error) return <Typography color="error">{error}</Typography>;
  if (!data) return null;

  // Flatten stats for display
  const stats1 = data.player1?.stats || {};
  const stats2 = data.player2?.stats || {};
  const allStatKeys = Array.from(new Set([...Object.keys(stats1), ...Object.keys(stats2)]));

  return (
    <Paper sx={{ p: 3 }}>
      <Typography variant="h5" align="center" gutterBottom>
        {data.player1?.name} vs. {data.player2?.name} ({season})
      </Typography>
      <TableContainer>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Stat</TableCell>
              <TableCell>{data.player1?.name}</TableCell>
              <TableCell>{data.player2?.name}</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {allStatKeys.map(key => (
              <TableRow key={key}>
                <TableCell>{key}</TableCell>
                <TableCell>{stats1[key] ?? '-'}</TableCell>
                <TableCell>{stats2[key] ?? '-'}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </Paper>
  );
};

export default PlayerComparison;
