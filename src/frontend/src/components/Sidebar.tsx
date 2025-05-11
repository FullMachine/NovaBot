import React from 'react';
import { Drawer, List, ListItem, ListItemIcon, ListItemText, Divider, Toolbar, Box, ListItemButton } from '@mui/material';
import HomeIcon from '@mui/icons-material/Home';
import SportsBasketballIcon from '@mui/icons-material/SportsBasketball';
import SportsFootballIcon from '@mui/icons-material/SportsFootball';
import SportsBaseballIcon from '@mui/icons-material/SportsBaseball';
import GroupIcon from '@mui/icons-material/Group';
import { Link, useLocation } from 'react-router-dom';

const drawerWidth = 220;

const Sidebar: React.FC<{ open: boolean; onClose: () => void; }> = ({ open, onClose }) => {
  const location = useLocation();
  return (
    <Drawer
      variant="permanent"
      sx={{
        width: drawerWidth,
        flexShrink: 0,
        [`& .MuiDrawer-paper`]: {
          width: drawerWidth,
          boxSizing: 'border-box',
          bgcolor: 'background.paper',
          color: 'text.primary',
          borderRight: 'none',
        },
        display: { xs: 'none', md: 'block' },
      }}
      open={open}
      onClose={onClose}
    >
      <Toolbar />
      <Box sx={{ overflow: 'auto', pt: 2 }}>
        <List>
          <ListItemButton component={Link} to="/" selected={location.pathname === '/'}>
            <ListItemIcon><HomeIcon color="primary" /></ListItemIcon>
            <ListItemText primary="Home" />
          </ListItemButton>
          <ListItemButton component={Link} to="/" selected={location.pathname.startsWith('/nba')}>
            <ListItemIcon><SportsBasketballIcon color="primary" /></ListItemIcon>
            <ListItemText primary="NBA" />
          </ListItemButton>
          <ListItemButton component={Link} to="/nfl" selected={location.pathname.startsWith('/nfl')}>
            <ListItemIcon><SportsFootballIcon color="primary" /></ListItemIcon>
            <ListItemText primary="NFL" />
          </ListItemButton>
          <ListItemButton component={Link} to="/mlb" selected={location.pathname.startsWith('/mlb')}>
            <ListItemIcon><SportsBaseballIcon color="primary" /></ListItemIcon>
            <ListItemText primary="MLB" />
          </ListItemButton>
        </List>
        <Divider sx={{ my: 2 }} />
        <List>
          <ListItem>
            <ListItemIcon><GroupIcon color="secondary" /></ListItemIcon>
            <ListItemText primary="Teams (Coming Soon)" />
          </ListItem>
        </List>
      </Box>
    </Drawer>
  );
};

export default Sidebar; 