import React, { useState } from 'react';
import { Autocomplete, TextField, CircularProgress } from '@mui/material';
import axios from 'axios';

interface PlayerSearchProps {
  label: string;
  onPlayerSelect: (player: any) => void;
  selectedPlayer: any;
}

const PlayerSearch: React.FC<PlayerSearchProps> = ({ label, onPlayerSelect, selectedPlayer }) => {
  const [inputValue, setInputValue] = useState('');
  const [options, setOptions] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);

  const handleInputChange = async (_: any, value: string) => {
    setInputValue(value);
    if (value.length < 2) {
      setOptions([]);
      return;
    }
    setLoading(true);
    try {
      const res = await axios.get(`/api/v1/nba/players/search?query=${encodeURIComponent(value)}`);
      setOptions(res.data.results || []);
    } catch (e) {
      setOptions([]);
    }
    setLoading(false);
  };

  return (
    <Autocomplete
      value={selectedPlayer}
      onChange={(_, newValue) => onPlayerSelect(newValue)}
      inputValue={inputValue}
      onInputChange={handleInputChange}
      options={options}
      getOptionLabel={option => option.name || ''}
      isOptionEqualToValue={(option, value) => option.id === value.id}
      loading={loading}
      renderInput={params => (
        <TextField {...params} label={label} variant="outlined" InputProps={{
          ...params.InputProps,
          endAdornment: (
            <>
              {loading ? <CircularProgress color="inherit" size={20} /> : null}
              {params.InputProps.endAdornment}
            </>
          ),
        }} />
      )}
    />
  );
};

export default PlayerSearch;
