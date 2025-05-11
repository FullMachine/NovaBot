import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Autocomplete, TextField, CircularProgress, Box, Typography, Card } from '@mui/material';

const PlayersList = () => {
  const [players, setPlayers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [inputValue, setInputValue] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    const fetchPlayers = async () => {
      setLoading(true);
      setError(null);
      try {
        const response = await fetch('http://localhost:8000/api/v1/nba/players/search?limit=2000');
        if (!response.ok) throw new Error('Failed to fetch players');
        const data = await response.json();
        setPlayers(Array.isArray(data) ? data : []);
      } catch (err) {
        setError(err.message);
      }
      setLoading(false);
    };
    fetchPlayers();
  }, []);

  return (
    <Card sx={{ p: 3, mb: 3, bgcolor: 'background.paper', borderRadius: 3, boxShadow: 4 }}>
      <Typography variant="h5" sx={{ mb: 2, color: 'primary.main' }}>NBA Player Search</Typography>
      {error && <Box color="error.main">Error: {error}</Box>}
      <Autocomplete
        options={players}
        getOptionLabel={option => option.name || ''}
        loading={loading}
        onChange={(_, value) => value && navigate(`/player/${value.id}`)}
        inputValue={inputValue}
        onInputChange={(_, value) => setInputValue(value)}
        renderInput={params => (
          <TextField
            {...params}
            label="Search NBA Players"
            variant="outlined"
            InputProps={{
              ...params.InputProps,
              endAdornment: (
                <>
                  {loading ? <CircularProgress color="inherit" size={20} /> : null}
                  {params.InputProps.endAdornment}
                </>
              ),
            }}
          />
        )}
        sx={{ width: 350, bgcolor: 'background.default', borderRadius: 2 }}
      />
    </Card>
  );
};

export default PlayersList; 