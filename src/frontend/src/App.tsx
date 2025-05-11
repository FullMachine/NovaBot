import React, { useContext, useState } from 'react';
import { Routes, Route, Link } from 'react-router-dom';
import PlayersList from './components/PlayersList';
import NBAPlayersCollectedList from './components/NBAPlayersCollectedList';
import PlayerProfile from './components/PlayerProfile';
import { AppBar, Toolbar, Typography, Box, Container, Button, IconButton, useTheme, useMediaQuery } from '@mui/material';
import SportsBasketballIcon from '@mui/icons-material/SportsBasketball';
import SportsFootballIcon from '@mui/icons-material/SportsFootball';
import SportsBaseballIcon from '@mui/icons-material/SportsBaseball';
import MenuIcon from '@mui/icons-material/Menu';
import Brightness4Icon from '@mui/icons-material/Brightness4';
import Brightness7Icon from '@mui/icons-material/Brightness7';
import { ColorModeContext } from './theme';
import Sidebar from './components/Sidebar';

// Placeholder components for NFL and MLB
const NFLPage = () => <div><h2 style={{color:'#8e24aa'}}>NFL Section (Coming Soon)</h2><p>Player stats, teams, and analytics for NFL will appear here.</p></div>;
const MLBPage = () => <div><h2 style={{color:'#8e24aa'}}>MLB Section (Coming Soon)</h2><p>Player stats, teams, and analytics for MLB will appear here.</p></div>;

const drawerWidth = 220;

function App() {
  const theme = useTheme();
  const colorMode = useContext(ColorModeContext);
  const [drawerOpen, setDrawerOpen] = useState(false);
  const isDesktop = useMediaQuery(theme.breakpoints.up('md'));

  return (
    <Box sx={{ bgcolor: 'background.default', minHeight: '100vh', display: 'flex' }}>
      {/* Sidebar for desktop */}
      {isDesktop && <Sidebar open={true} onClose={() => {}} />}
      {/* Sidebar for mobile */}
      {!isDesktop && <Sidebar open={drawerOpen} onClose={() => setDrawerOpen(false)} />}
      <Box sx={{ flexGrow: 1, ml: { md: `${drawerWidth}px` } }}>
        <AppBar position="static" color="primary" sx={{ borderRadius: 2, mb: 3 }}>
          <Toolbar>
            {!isDesktop && (
              <IconButton edge="start" color="inherit" aria-label="menu" sx={{ mr: 2 }} onClick={() => setDrawerOpen(true)}>
                <MenuIcon />
              </IconButton>
            )}
            <SportsBasketballIcon sx={{ mr: 2 }} />
            <Typography variant="h5" sx={{ flexGrow: 1, fontWeight: 700 }}>
              Nova Sports Analytics
            </Typography>
            <IconButton sx={{ ml: 1 }} onClick={colorMode.toggleColorMode} color="inherit">
              {theme.palette.mode === 'dark' ? <Brightness7Icon /> : <Brightness4Icon />}
            </IconButton>
          </Toolbar>
        </AppBar>
        <Container maxWidth="lg">
          <Routes>
            <Route path="/" element={
              <div>
                <PlayersList />
                <NBAPlayersCollectedList />
              </div>
            } />
            <Route path="/nfl" element={<NFLPage />} />
            <Route path="/mlb" element={<MLBPage />} />
            <Route path="/player/:id" element={<PlayerProfile />} />
          </Routes>
        </Container>
        {/* Footer */}
        <Box sx={{ textAlign: 'center', py: 3, color: 'text.secondary', fontSize: 14 }}>
          © {new Date().getFullYear()} Nova Sports Analytics. All rights reserved.
        </Box>
      </Box>
    </Box>
  );
}

export default App;
