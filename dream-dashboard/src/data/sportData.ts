// Centralized mock data for all sports dashboards

// --- Teams ---
const teamsData = {
  NBA: [
    { name: 'Los Angeles Lakers', abbr: 'LAL', logo: 'https://cdn.nba.com/logos/nba/1610612747/primary/L/logo.svg' },
    { name: 'Boston Celtics', abbr: 'BOS', logo: 'https://cdn.nba.com/logos/nba/1610612738/primary/L/logo.svg' },
    { name: 'Golden State Warriors', abbr: 'GSW', logo: 'https://cdn.nba.com/logos/nba/1610612744/primary/L/logo.svg' },
    { name: 'Miami Heat', abbr: 'MIA', logo: 'https://cdn.nba.com/logos/nba/1610612748/primary/L/logo.svg' },
    { name: 'Milwaukee Bucks', abbr: 'MIL', logo: 'https://cdn.nba.com/logos/nba/1610612749/primary/L/logo.svg' },
    { name: 'Dallas Mavericks', abbr: 'DAL', logo: 'https://cdn.nba.com/logos/nba/1610612742/primary/L/logo.svg' },
  ],
  NFL: [
    { name: 'Kansas City Chiefs', abbr: 'KC', logo: 'https://static.www.nfl.com/t_q-best/league/api/clubs/logos/KC' },
    { name: 'Buffalo Bills', abbr: 'BUF', logo: 'https://static.www.nfl.com/t_q-best/league/api/clubs/logos/BUF' },
    { name: 'San Francisco 49ers', abbr: 'SF', logo: 'https://static.www.nfl.com/t_q-best/league/api/clubs/logos/SF' },
    { name: 'Philadelphia Eagles', abbr: 'PHI', logo: 'https://static.www.nfl.com/t_q-best/league/api/clubs/logos/PHI' },
    { name: 'Dallas Cowboys', abbr: 'DAL', logo: 'https://static.www.nfl.com/t_q-best/league/api/clubs/logos/DAL' },
    { name: 'Baltimore Ravens', abbr: 'BAL', logo: 'https://static.www.nfl.com/t_q-best/league/api/clubs/logos/BAL' },
  ],
  MLB: [
    { name: 'Los Angeles Dodgers', abbr: 'LAD', logo: 'https://www.mlbstatic.com/team-logos/119.svg' },
    { name: 'New York Yankees', abbr: 'NYY', logo: 'https://www.mlbstatic.com/team-logos/147.svg' },
    { name: 'Houston Astros', abbr: 'HOU', logo: 'https://www.mlbstatic.com/team-logos/117.svg' },
    { name: 'Atlanta Braves', abbr: 'ATL', logo: 'https://www.mlbstatic.com/team-logos/144.svg' },
    { name: 'Chicago Cubs', abbr: 'CHC', logo: 'https://www.mlbstatic.com/team-logos/112.svg' },
    { name: 'Boston Red Sox', abbr: 'BOS', logo: 'https://www.mlbstatic.com/team-logos/111.svg' },
  ],
  Soccer: [
    { name: 'Manchester City', abbr: 'MCI', logo: 'https://resources.premierleague.com/premierleague/badges/t43.png' },
    { name: 'Arsenal', abbr: 'ARS', logo: 'https://resources.premierleague.com/premierleague/badges/t3.png' },
    { name: 'Liverpool', abbr: 'LIV', logo: 'https://resources.premierleague.com/premierleague/badges/t14.png' },
    { name: 'Chelsea', abbr: 'CHE', logo: 'https://resources.premierleague.com/premierleague/badges/t8.png' },
    { name: 'Tottenham', abbr: 'TOT', logo: 'https://resources.premierleague.com/premierleague/badges/t6.png' },
    { name: 'Newcastle', abbr: 'NEW', logo: 'https://resources.premierleague.com/premierleague/badges/t4.png' },
  ],
  Tennis: [],
  Esports: [],
  Hockey: [
    { name: 'Edmonton Oilers', abbr: 'EDM', logo: 'https://upload.wikimedia.org/wikipedia/en/4/4d/Edmonton_Oilers_logo.svg' },
    { name: 'Calgary Flames', abbr: 'CGY', logo: 'https://upload.wikimedia.org/wikipedia/en/6/60/Calgary_Flames_logo.svg' },
    { name: 'Toronto Maple Leafs', abbr: 'TOR', logo: 'https://upload.wikimedia.org/wikipedia/en/3/3a/Toronto_Maple_Leafs_logo.svg' },
    { name: 'Boston Bruins', abbr: 'BOS', logo: 'https://upload.wikimedia.org/wikipedia/commons/6/6d/Boston_Bruins.svg' },
    { name: 'New York Rangers', abbr: 'NYR', logo: 'https://upload.wikimedia.org/wikipedia/en/9/9f/New_York_Rangers.svg' },
    { name: 'Colorado Avalanche', abbr: 'COL', logo: 'https://upload.wikimedia.org/wikipedia/en/4/45/Colorado_Avalanche_logo.svg' },
  ],
};

// --- Standings ---
const standingsData = {
  NBA: {
    All: [
      { team: 'Boston Celtics', abbr: 'BOS', logo: 'https://cdn.nba.com/logos/nba/1610612738/primary/L/logo.svg', wins: 62, losses: 20, conf: 'East' },
      { team: 'Denver Nuggets', abbr: 'DEN', logo: 'https://cdn.nba.com/logos/nba/1610612743/primary/L/logo.svg', wins: 57, losses: 25, conf: 'West' },
      { team: 'Oklahoma City Thunder', abbr: 'OKC', logo: 'https://cdn.nba.com/logos/nba/1610612760/primary/L/logo.svg', wins: 56, losses: 26, conf: 'West' },
      { team: 'Milwaukee Bucks', abbr: 'MIL', logo: 'https://cdn.nba.com/logos/nba/1610612749/primary/L/logo.svg', wins: 54, losses: 28, conf: 'East' },
    ],
    East: [
      { team: 'Boston Celtics', abbr: 'BOS', logo: 'https://cdn.nba.com/logos/nba/1610612738/primary/L/logo.svg', wins: 62, losses: 20, conf: 'East' },
      { team: 'Milwaukee Bucks', abbr: 'MIL', logo: 'https://cdn.nba.com/logos/nba/1610612749/primary/L/logo.svg', wins: 54, losses: 28, conf: 'East' },
    ],
    West: [
      { team: 'Denver Nuggets', abbr: 'DEN', logo: 'https://cdn.nba.com/logos/nba/1610612743/primary/L/logo.svg', wins: 57, losses: 25, conf: 'West' },
      { team: 'Oklahoma City Thunder', abbr: 'OKC', logo: 'https://cdn.nba.com/logos/nba/1610612760/primary/L/logo.svg', wins: 56, losses: 26, conf: 'West' },
    ],
  },
  NFL: {
    All: [
      { team: 'Kansas City Chiefs', abbr: 'KC', logo: 'https://static.www.nfl.com/t_q-best/league/api/clubs/logos/KC', wins: 14, losses: 3, conf: 'AFC' },
      { team: 'Buffalo Bills', abbr: 'BUF', logo: 'https://static.www.nfl.com/t_q-best/league/api/clubs/logos/BUF', wins: 13, losses: 4, conf: 'AFC' },
      { team: 'San Francisco 49ers', abbr: 'SF', logo: 'https://static.www.nfl.com/t_q-best/league/api/clubs/logos/SF', wins: 13, losses: 4, conf: 'NFC' },
      { team: 'Philadelphia Eagles', abbr: 'PHI', logo: 'https://static.www.nfl.com/t_q-best/league/api/clubs/logos/PHI', wins: 12, losses: 5, conf: 'NFC' },
    ],
    AFC: [
      { team: 'Kansas City Chiefs', abbr: 'KC', logo: 'https://static.www.nfl.com/t_q-best/league/api/clubs/logos/KC', wins: 14, losses: 3, conf: 'AFC' },
      { team: 'Buffalo Bills', abbr: 'BUF', logo: 'https://static.www.nfl.com/t_q-best/league/api/clubs/logos/BUF', wins: 13, losses: 4, conf: 'AFC' },
    ],
    NFC: [
      { team: 'San Francisco 49ers', abbr: 'SF', logo: 'https://static.www.nfl.com/t_q-best/league/api/clubs/logos/SF', wins: 13, losses: 4, conf: 'NFC' },
      { team: 'Philadelphia Eagles', abbr: 'PHI', logo: 'https://static.www.nfl.com/t_q-best/league/api/clubs/logos/PHI', wins: 12, losses: 5, conf: 'NFC' },
    ],
  },
  MLB: {
    All: [
      { team: 'Los Angeles Dodgers', abbr: 'LAD', logo: 'https://www.mlbstatic.com/team-logos/119.svg', wins: 98, losses: 64, conf: 'NL' },
      { team: 'New York Yankees', abbr: 'NYY', logo: 'https://www.mlbstatic.com/team-logos/147.svg', wins: 92, losses: 70, conf: 'AL' },
      { team: 'Houston Astros', abbr: 'HOU', logo: 'https://www.mlbstatic.com/team-logos/117.svg', wins: 95, losses: 67, conf: 'AL' },
      { team: 'Atlanta Braves', abbr: 'ATL', logo: 'https://www.mlbstatic.com/team-logos/144.svg', wins: 101, losses: 61, conf: 'NL' },
    ],
    AL: [
      { team: 'New York Yankees', abbr: 'NYY', logo: 'https://www.mlbstatic.com/team-logos/147.svg', wins: 92, losses: 70, conf: 'AL' },
      { team: 'Houston Astros', abbr: 'HOU', logo: 'https://www.mlbstatic.com/team-logos/117.svg', wins: 95, losses: 67, conf: 'AL' },
    ],
    NL: [
      { team: 'Los Angeles Dodgers', abbr: 'LAD', logo: 'https://www.mlbstatic.com/team-logos/119.svg', wins: 98, losses: 64, conf: 'NL' },
      { team: 'Atlanta Braves', abbr: 'ATL', logo: 'https://www.mlbstatic.com/team-logos/144.svg', wins: 101, losses: 61, conf: 'NL' },
    ],
  },
  Soccer: {
    All: [
      { team: 'Manchester City', abbr: 'MCI', logo: 'https://resources.premierleague.com/premierleague/badges/t43.png', wins: 28, losses: 5, conf: 'EPL' },
      { team: 'Arsenal', abbr: 'ARS', logo: 'https://resources.premierleague.com/premierleague/badges/t3.png', wins: 26, losses: 7, conf: 'EPL' },
      { team: 'Liverpool', abbr: 'LIV', logo: 'https://resources.premierleague.com/premierleague/badges/t14.png', wins: 24, losses: 8, conf: 'EPL' },
      { team: 'Chelsea', abbr: 'CHE', logo: 'https://resources.premierleague.com/premierleague/badges/t8.png', wins: 20, losses: 12, conf: 'EPL' },
    ],
  },
  Tennis: {
    Rankings: [
      { team: 'Novak Djokovic', abbr: 'N.DJ', logo: 'https://www.atptour.com/-/media/images/players/head-shot/novak-djokovic.png', wins: 35, losses: 5, conf: 'SRB' },
      { team: 'Carlos Alcaraz', abbr: 'C.ALC', logo: 'https://www.atptour.com/-/media/images/players/head-shot/carlos-alcaraz.png', wins: 32, losses: 7, conf: 'ESP' },
      { team: 'Jannik Sinner', abbr: 'J.SIN', logo: 'https://www.atptour.com/-/media/images/players/head-shot/jannik-sinner.png', wins: 30, losses: 8, conf: 'ITA' },
      { team: 'Daniil Medvedev', abbr: 'D.MED', logo: 'https://www.atptour.com/-/media/images/players/head-shot/daniil-medvedev.png', wins: 28, losses: 10, conf: 'RUS' },
    ],
  },
  Esports: {
    Leaderboard: [
      { team: 'NAVI', abbr: 'NAVI', logo: 'https://img-cdn.hltv.org/teamlogo/2QZp8k5lYwQn6l0e6Q.png', wins: 18, losses: 4, conf: 'CS:GO' },
      { team: 'G2 Esports', abbr: 'G2', logo: 'https://img-cdn.hltv.org/teamlogo/HyD1b5bNwQn6l0e6Q.png', wins: 16, losses: 6, conf: 'CS:GO' },
      { team: 'T1', abbr: 'T1', logo: 'https://static.wikia.nocookie.net/lolesports_gamepedia_en/images/7/7a/T1logo_profile.png', wins: 15, losses: 7, conf: 'LoL' },
      { team: 'Fnatic', abbr: 'FNC', logo: 'https://static.wikia.nocookie.net/lolesports_gamepedia_en/images/7/7e/Fnaticlogo_profile.png', wins: 14, losses: 8, conf: 'LoL' },
    ],
  },
  Hockey: {
    All: [
      { team: 'Edmonton Oilers', abbr: 'EDM', logo: 'https://upload.wikimedia.org/wikipedia/en/4/4d/Edmonton_Oilers_logo.svg', wins: 50, losses: 23, conf: 'West' },
      { team: 'Calgary Flames', abbr: 'CGY', logo: 'https://upload.wikimedia.org/wikipedia/en/6/60/Calgary_Flames_logo.svg', wins: 45, losses: 28, conf: 'West' },
      { team: 'Toronto Maple Leafs', abbr: 'TOR', logo: 'https://upload.wikimedia.org/wikipedia/en/3/3a/Toronto_Maple_Leafs_logo.svg', wins: 48, losses: 25, conf: 'East' },
      { team: 'Boston Bruins', abbr: 'BOS', logo: 'https://upload.wikimedia.org/wikipedia/commons/6/6d/Boston_Bruins.svg', wins: 52, losses: 20, conf: 'East' },
    ],
    East: [
      { team: 'Toronto Maple Leafs', abbr: 'TOR', logo: 'https://upload.wikimedia.org/wikipedia/en/3/3a/Toronto_Maple_Leafs_logo.svg', wins: 48, losses: 25, conf: 'East' },
      { team: 'Boston Bruins', abbr: 'BOS', logo: 'https://upload.wikimedia.org/wikipedia/commons/6/6d/Boston_Bruins.svg', wins: 52, losses: 20, conf: 'East' },
    ],
    West: [
      { team: 'Edmonton Oilers', abbr: 'EDM', logo: 'https://upload.wikimedia.org/wikipedia/en/4/4d/Edmonton_Oilers_logo.svg', wins: 50, losses: 23, conf: 'West' },
      { team: 'Calgary Flames', abbr: 'CGY', logo: 'https://upload.wikimedia.org/wikipedia/en/6/60/Calgary_Flames_logo.svg', wins: 45, losses: 28, conf: 'West' },
    ],
  },
};

// --- Players ---
const playersData = {
  NBA: [
    { name: 'Luka Dončić', team: 'LAL', photo: 'https://cdn.nba.com/headshots/nba/latest/1040x760/1629029.png' },
    { name: 'Jayson Tatum', team: 'BOS', photo: 'https://cdn.nba.com/headshots/nba/latest/1040x760/1628369.png' },
    { name: 'Stephen Curry', team: 'GSW', photo: 'https://cdn.nba.com/headshots/nba/latest/1040x760/201939.png' },
    { name: 'Jimmy Butler', team: 'MIA', photo: 'https://cdn.nba.com/headshots/nba/latest/1040x760/202710.png' },
    { name: 'Giannis Antetokounmpo', team: 'MIL', photo: 'https://cdn.nba.com/headshots/nba/latest/1040x760/203507.png' },
  ],
  NFL: [
    { name: 'Patrick Mahomes', team: 'KC', photo: 'https://static.www.nfl.com/image/upload/t_player_profile_landscape_2x/f_auto/league/qrdbvu4iqy7wkqg8jq8d' },
    { name: 'Josh Allen', team: 'BUF', photo: 'https://static.www.nfl.com/image/upload/t_player_profile_landscape_2x/f_auto/league/ptxqjv7kqkqkqkqkqkqk' },
    { name: 'Christian McCaffrey', team: 'SF', photo: 'https://static.www.nfl.com/image/upload/t_player_profile_landscape_2x/f_auto/league/ptxqjv7kqkqkqkqkqkqk' },
    { name: 'Jalen Hurts', team: 'PHI', photo: 'https://static.www.nfl.com/image/upload/t_player_profile_landscape_2x/f_auto/league/ptxqjv7kqkqkqkqkqkqk' },
    { name: 'Dak Prescott', team: 'DAL', photo: 'https://static.www.nfl.com/image/upload/t_player_profile_landscape_2x/f_auto/league/ptxqjv7kqkqkqkqkqkqk' },
  ],
  MLB: [
    { name: 'Shohei Ohtani', team: 'LAD', photo: 'https://a.espncdn.com/i/headshots/mlb/players/full/40921.png' },
    { name: 'Aaron Judge', team: 'NYY', photo: 'https://a.espncdn.com/i/headshots/mlb/players/full/33192.png' },
    { name: 'Jose Altuve', team: 'HOU', photo: 'https://a.espncdn.com/i/headshots/mlb/players/full/31662.png' },
    { name: 'Ronald Acuña Jr.', team: 'ATL', photo: 'https://img.mlbstatic.com/mlb-photos/image/upload/v1/people/660670/headshot/67/current.jpg' },
    { name: 'Dansby Swanson', team: 'CHC', photo: 'https://img.mlbstatic.com/mlb-photos/image/upload/v1/people/663586/headshot/67/current.jpg' },
  ],
  Soccer: [
    { name: 'Erling Haaland', team: 'MCI', photo: 'https://resources.premierleague.com/premierleague/photos/players/250x250/p223094.png' },
    { name: 'Bukayo Saka', team: 'ARS', photo: 'https://resources.premierleague.com/premierleague/photos/players/250x250/p223340.png' },
    { name: 'Mohamed Salah', team: 'LIV', photo: 'https://resources.premierleague.com/premierleague/photos/players/250x250/p118748.png' },
    { name: 'Raheem Sterling', team: 'CHE', photo: 'https://resources.premierleague.com/premierleague/photos/players/250x250/p103955.png' },
    { name: 'Son Heung-min', team: 'TOT', photo: 'https://resources.premierleague.com/premierleague/photos/players/250x250/p85971.png' },
  ],
  Tennis: [],
  Esports: [],
  Hockey: [
    { name: 'Connor McDavid', team: 'EDM', photo: 'https://a.espncdn.com/i/headshots/nhl/players/full/3883573.png' },
    { name: 'Auston Matthews', team: 'TOR', photo: 'https://a.espncdn.com/i/headshots/nhl/players/full/4034418.png' },
    { name: 'David Pastrnak', team: 'BOS', photo: 'https://a.espncdn.com/i/headshots/nhl/players/full/3114710.png' },
    { name: 'Mika Zibanejad', team: 'NYR', photo: 'https://a.espncdn.com/i/headshots/nhl/players/full/2562587.png' },
    { name: 'Nathan MacKinnon', team: 'COL', photo: 'https://a.espncdn.com/i/headshots/nhl/players/full/3883572.png' },
  ],
};

// --- Exported functions ---
export function getSportTeams(sport: string) {
  return (teamsData as any)[sport] || [];
}
export function getSportStandings(sport: string) {
  return (standingsData as any)[sport] || { All: [] };
}
export function getSportPlayers(sport: string) {
  return (playersData as any)[sport] || [];
} 