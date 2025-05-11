// Fake player data for demo/testing. Add more players as needed.
export const fakePlayers = [
  // NBA
  {
    name: 'Luka Dončić',
    team: 'Lakers',
    position: 'PG',
    photo: 'https://cdn.nba.com/headshots/nba/latest/1040x760/1629029.png',
    sport: 'NBA',
    statTabs: ['H2H', 'L5', 'L10', '2024', '2023'],
    statTypeTabs: ['PTS', 'AST', 'REB', '3PM', 'STL', 'BLK', 'TO'],
    statsByTab: {
      H2H: {
        PTS: [
          { date: '5/1', value: 32 },
          { date: '4/15', value: 28 },
          { date: '3/30', value: 35 },
          { date: '3/10', value: 40 },
          { date: '2/25', value: 29 },
        ],
        AST: [
          { date: '5/1', value: 10 },
          { date: '4/15', value: 12 },
          { date: '3/30', value: 8 },
          { date: '3/10', value: 14 },
          { date: '2/25', value: 11 },
        ],
        REB: [
          { date: '5/1', value: 7 },
          { date: '4/15', value: 9 },
          { date: '3/30', value: 8 },
          { date: '3/10', value: 10 },
          { date: '2/25', value: 6 },
        ],
        '3PM': [
          { date: '5/1', value: 4 },
          { date: '4/15', value: 3 },
          { date: '3/30', value: 5 },
          { date: '3/10', value: 6 },
          { date: '2/25', value: 2 },
        ],
        STL: [
          { date: '5/1', value: 2 },
          { date: '4/15', value: 1 },
          { date: '3/30', value: 3 },
          { date: '3/10', value: 2 },
          { date: '2/25', value: 2 },
        ],
        BLK: [
          { date: '5/1', value: 1 },
          { date: '4/15', value: 0 },
          { date: '3/30', value: 2 },
          { date: '3/10', value: 1 },
          { date: '2/25', value: 1 },
        ],
        TO: [
          { date: '5/1', value: 3 },
          { date: '4/15', value: 2 },
          { date: '3/30', value: 4 },
          { date: '3/10', value: 5 },
          { date: '2/25', value: 3 },
        ],
      },
      L5: {
        PTS: [
          { date: '5/6', value: 38 },
          { date: '5/4', value: 30 },
          { date: '4/28', value: 36 },
          { date: '4/26', value: 27 },
          { date: '4/23', value: 31 },
        ],
        AST: [
          { date: '5/6', value: 12 },
          { date: '5/4', value: 9 },
          { date: '4/28', value: 11 },
          { date: '4/26', value: 8 },
          { date: '4/23', value: 10 },
        ],
        REB: [
          { date: '5/6', value: 8 },
          { date: '5/4', value: 7 },
          { date: '4/28', value: 9 },
          { date: '4/26', value: 6 },
          { date: '4/23', value: 8 },
        ],
        '3PM': [
          { date: '5/6', value: 5 },
          { date: '5/4', value: 4 },
          { date: '4/28', value: 6 },
          { date: '4/26', value: 3 },
          { date: '4/23', value: 4 },
        ],
        STL: [
          { date: '5/6', value: 2 },
          { date: '5/4', value: 1 },
          { date: '4/28', value: 3 },
          { date: '4/26', value: 2 },
          { date: '4/23', value: 2 },
        ],
        BLK: [
          { date: '5/6', value: 1 },
          { date: '5/4', value: 0 },
          { date: '4/28', value: 2 },
          { date: '4/26', value: 1 },
          { date: '4/23', value: 1 },
        ],
        TO: [
          { date: '5/6', value: 4 },
          { date: '5/4', value: 3 },
          { date: '4/28', value: 2 },
          { date: '4/26', value: 5 },
          { date: '4/23', value: 3 },
        ],
      },
      // Add more tabs (L10, L20, 2024, 2023) with similar structure for realism
    },
    line: 28.5,
    overPercent: 80,
    gameLog: [
      { player: 'Luka Dončić', result: 38, line: 28.5, odds: '20/21', hit: true },
      { player: 'Luka Dončić', result: 30, line: 28.5, odds: '21/20', hit: true },
      { player: 'Luka Dončić', result: 27, line: 28.5, odds: '19/20', hit: false },
      { player: 'Luka Dončić', result: 35, line: 28.5, odds: '22/20', hit: true },
      { player: 'Luka Dončić', result: 25, line: 28.5, odds: '18/20', hit: false },
      { player: 'Luka Dončić', result: 40, line: 28.5, odds: '23/20', hit: true },
      { player: 'Luka Dončić', result: 29, line: 28.5, odds: '20/21', hit: true },
    ],
    supportingStats: [
      { label: 'Minutes', value: 36 },
      { label: 'Field Goals', value: 12 },
      { label: '3pts', value: 5 },
      { label: 'Fouls', value: 2 },
      { label: 'Turnovers', value: 3 },
      { label: 'Free Throws', value: 8 },
    ],
  },
  // NFL
  {
    name: 'Patrick Mahomes',
    team: 'Chiefs',
    position: 'QB',
    photo: 'https://static.www.nfl.com/image/private/t_headshot_desktop/league/tx9z5gkqkqj7gkqj7gkq',
    sport: 'NFL',
    statTabs: ['L5', 'L10', '2024', '2023'],
    statTypeTabs: ['PASS YDS', 'TD', 'INT', 'RUSH YDS', 'SACKS'],
    statsByTab: {
      L5: {
        'PASS YDS': [ { date: '9/10', value: 305 }, { date: '9/17', value: 285 }, { date: '9/24', value: 272 }, { date: '10/1', value: 249 }, { date: '10/8', value: 281 } ],
        TD: [ { date: '9/10', value: 3 }, { date: '9/17', value: 2 }, { date: '9/24', value: 4 }, { date: '10/1', value: 1 }, { date: '10/8', value: 2 } ],
        INT: [ { date: '9/10', value: 1 }, { date: '9/17', value: 0 }, { date: '9/24', value: 2 }, { date: '10/1', value: 1 }, { date: '10/8', value: 0 } ],
        'RUSH YDS': [ { date: '9/10', value: 25 }, { date: '9/17', value: 18 }, { date: '9/24', value: 30 }, { date: '10/1', value: 12 }, { date: '10/8', value: 20 } ],
        SACKS: [ { date: '9/10', value: 2 }, { date: '9/17', value: 1 }, { date: '9/24', value: 3 }, { date: '10/1', value: 0 }, { date: '10/8', value: 2 } ]
      },
      // ...other tabs
    },
    line: 275.5,
    overPercent: 60,
    gameLog: [ { player: 'Patrick Mahomes', result: 305, line: 275.5, odds: '10/11', hit: true }, { player: 'Patrick Mahomes', result: 249, line: 275.5, odds: '10/11', hit: false } ],
    supportingStats: [ { label: 'Completions', value: 28 }, { label: 'Attempts', value: 40 }, { label: 'Rushing Yards', value: 25 }, { label: 'Sacks', value: 2 } ],
  },
  // MLB
  {
    name: 'Shohei Ohtani',
    team: 'Dodgers',
    position: 'DH',
    photo: 'https://content.mlb.com/images/headshots/current/60x60/660271.png',
    sport: 'MLB',
    statTabs: ['L5', 'L10', '2024', '2023'],
    statTypeTabs: ['HR', 'RBI', 'AVG', 'SB', 'HBP'],
    statsByTab: {
      L5: {
        HR: [ { date: '5/1', value: 1 }, { date: '5/2', value: 0 }, { date: '5/3', value: 2 }, { date: '5/4', value: 1 }, { date: '5/5', value: 0 } ],
        RBI: [ { date: '5/1', value: 3 }, { date: '5/2', value: 1 }, { date: '5/3', value: 2 }, { date: '5/4', value: 0 }, { date: '5/5', value: 1 } ],
        AVG: [ { date: '5/1', value: 0.333 }, { date: '5/2', value: 0.250 }, { date: '5/3', value: 0.400 }, { date: '5/4', value: 0.200 }, { date: '5/5', value: 0.500 } ],
        SB: [ { date: '5/1', value: 1 }, { date: '5/2', value: 0 }, { date: '5/3', value: 1 }, { date: '5/4', value: 0 }, { date: '5/5', value: 2 } ],
        HBP: [ { date: '5/1', value: 0 }, { date: '5/2', value: 1 }, { date: '5/3', value: 0 }, { date: '5/4', value: 0 }, { date: '5/5', value: 1 } ]
      },
      // ...other tabs
    },
    line: 1.5,
    overPercent: 50,
    gameLog: [ { player: 'Shohei Ohtani', result: 2, line: 1.5, odds: '2/1', hit: true }, { player: 'Shohei Ohtani', result: 0, line: 1.5, odds: '2/1', hit: false } ],
    supportingStats: [ { label: 'At Bats', value: 5 }, { label: 'Hits', value: 2 }, { label: 'Walks', value: 1 }, { label: 'Stolen Bases', value: 1 } ],
  },
  // Soccer
  {
    name: 'Erling Haaland',
    team: 'Man City',
    position: 'ST',
    photo: 'https://resources.premierleague.com/premierleague/photos/players/250x250/p223094.png',
    sport: 'Soccer',
    statTabs: ['L5', 'L10', '2024', '2023'],
    statTypeTabs: ['GOALS', 'ASSISTS', 'SHOTS', 'PASSES', 'TACKLES'],
    statsByTab: {
      L5: {
        GOALS: [ { date: '4/1', value: 2 }, { date: '4/8', value: 1 }, { date: '4/15', value: 0 }, { date: '4/22', value: 1 }, { date: '4/29', value: 2 } ],
        ASSISTS: [ { date: '4/1', value: 1 }, { date: '4/8', value: 0 }, { date: '4/15', value: 2 }, { date: '4/22', value: 1 }, { date: '4/29', value: 1 } ],
        SHOTS: [ { date: '4/1', value: 5 }, { date: '4/8', value: 3 }, { date: '4/15', value: 4 }, { date: '4/22', value: 2 }, { date: '4/29', value: 6 } ],
        PASSES: [ { date: '4/1', value: 30 }, { date: '4/8', value: 28 }, { date: '4/15', value: 35 }, { date: '4/22', value: 32 }, { date: '4/29', value: 40 } ],
        TACKLES: [ { date: '4/1', value: 1 }, { date: '4/8', value: 2 }, { date: '4/15', value: 0 }, { date: '4/22', value: 1 }, { date: '4/29', value: 2 } ]
      },
      // ...other tabs
    },
    line: 1.5,
    overPercent: 70,
    gameLog: [ { player: 'Erling Haaland', result: 2, line: 1.5, odds: '3/2', hit: true }, { player: 'Erling Haaland', result: 0, line: 1.5, odds: '3/2', hit: false } ],
    supportingStats: [ { label: 'Minutes', value: 90 }, { label: 'Shots', value: 5 }, { label: 'Passes', value: 30 }, { label: 'Fouls', value: 1 } ],
  },
  // Tennis
  {
    name: 'Carlos Alcaraz',
    team: 'ESP',
    position: 'ATP',
    photo: 'https://www.atptour.com/-/media/images/players/head-shot/atp/a0c0/alcaraz-head-2022.png',
    sport: 'Tennis',
    statTabs: ['L5', 'L10', '2024', '2023'],
    statTypeTabs: ['ACES', 'DOUBLE FAULTS', 'WIN %', 'BREAKS', '1ST SERVE %'],
    statsByTab: {
      L5: {
        ACES: [ { date: '5/1', value: 12 }, { date: '4/28', value: 8 }, { date: '4/25', value: 15 }, { date: '4/20', value: 10 }, { date: '4/15', value: 9 } ],
        'DOUBLE FAULTS': [ { date: '5/1', value: 2 }, { date: '4/28', value: 1 }, { date: '4/25', value: 3 }, { date: '4/20', value: 2 }, { date: '4/15', value: 0 } ],
        'WIN %': [ { date: '5/1', value: 80 }, { date: '4/28', value: 75 }, { date: '4/25', value: 90 }, { date: '4/20', value: 85 }, { date: '4/15', value: 70 } ],
        BREAKS: [ { date: '5/1', value: 4 }, { date: '4/28', value: 3 }, { date: '4/25', value: 5 }, { date: '4/20', value: 2 }, { date: '4/15', value: 3 } ],
        '1ST SERVE %': [ { date: '5/1', value: 65 }, { date: '4/28', value: 70 }, { date: '4/25', value: 68 }, { date: '4/20', value: 72 }, { date: '4/15', value: 66 } ]
      },
      // ...other tabs
    },
    line: 10.5,
    overPercent: 65,
    gameLog: [ { player: 'Carlos Alcaraz', result: 12, line: 10.5, odds: '1.8', hit: true }, { player: 'Carlos Alcaraz', result: 8, line: 10.5, odds: '2.0', hit: false } ],
    supportingStats: [ { label: 'Aces', value: 12 }, { label: 'Double Faults', value: 2 }, { label: 'Break Points', value: 4 }, { label: 'Win %', value: 80 } ],
  },
  // Esports
  {
    name: 's1mple',
    team: 'NAVI',
    position: 'AWPer',
    photo: 'https://img-cdn.hltv.org/playerbodyshot/7998.png',
    sport: 'Esports',
    statTabs: ['L5', 'L10', '2024', '2023'],
    statTypeTabs: ['KILLS', 'DEATHS', 'ASSISTS', 'ADR', 'HS%'],
    statsByTab: {
      L5: {
        KILLS: [ { date: '5/1', value: 28 }, { date: '4/28', value: 32 }, { date: '4/25', value: 30 }, { date: '4/20', value: 27 }, { date: '4/15', value: 35 } ],
        DEATHS: [ { date: '5/1', value: 15 }, { date: '4/28', value: 12 }, { date: '4/25', value: 14 }, { date: '4/20', value: 16 }, { date: '4/15', value: 13 } ],
        ASSISTS: [ { date: '5/1', value: 7 }, { date: '4/28', value: 9 }, { date: '4/25', value: 8 }, { date: '4/20', value: 6 }, { date: '4/15', value: 10 } ],
        ADR: [ { date: '5/1', value: 85 }, { date: '4/28', value: 90 }, { date: '4/25', value: 88 }, { date: '4/20', value: 80 }, { date: '4/15', value: 95 } ],
        'HS%': [ { date: '5/1', value: 60 }, { date: '4/28', value: 62 }, { date: '4/25', value: 58 }, { date: '4/20', value: 65 }, { date: '4/15', value: 63 } ]
      },
      // ...other tabs
    },
    line: 25.5,
    overPercent: 75,
    gameLog: [ { player: 's1mple', result: 28, line: 25.5, odds: '1.7', hit: true }, { player: 's1mple', result: 32, line: 25.5, odds: '1.6', hit: true } ],
    supportingStats: [ { label: 'Kills', value: 28 }, { label: 'Deaths', value: 15 }, { label: 'Assists', value: 7 }, { label: 'ADR', value: 85 } ],
  },
  // Hockey
  {
    name: 'Connor McDavid',
    team: 'Oilers',
    position: 'C',
    photo: 'https://cms.nhl.bamgrid.com/images/headshots/current/168x168/8478402.jpg',
    sport: 'Hockey',
    statTabs: ['L5', 'L10', '2024', '2023'],
    statTypeTabs: ['GOALS', 'ASSISTS', 'POINTS', 'PIM'],
    statsByTab: {
      L5: {
        GOALS: [ { date: '4/1', value: 2 }, { date: '4/8', value: 1 }, { date: '4/15', value: 3 }, { date: '4/22', value: 2 }, { date: '4/29', value: 2 } ],
        ASSISTS: [ { date: '4/1', value: 3 }, { date: '4/8', value: 2 }, { date: '4/15', value: 4 }, { date: '4/22', value: 1 }, { date: '4/29', value: 5 } ],
        POINTS: [ { date: '4/1', value: 5 }, { date: '4/8', value: 3 }, { date: '4/15', value: 7 }, { date: '4/22', value: 3 }, { date: '4/29', value: 7 } ],
        PIM: [ { date: '4/1', value: 2 }, { date: '4/8', value: 0 }, { date: '4/15', value: 4 }, { date: '4/22', value: 2 }, { date: '4/29', value: 6 } ]
      },
      // ...other tabs
    },
    line: 1.5,
    overPercent: 85,
    gameLog: [ { player: 'Connor McDavid', result: 3, line: 1.5, odds: '2.2', hit: true }, { player: 'Connor McDavid', result: 1, line: 1.5, odds: '2.2', hit: false } ],
    supportingStats: [ { label: 'Goals', value: 2 }, { label: 'Assists', value: 3 }, { label: 'Points', value: 5 }, { label: 'Shots', value: 6 } ],
  },
  // Golf
  {
    name: 'Scottie Scheffler',
    team: 'USA',
    position: 'PGA',
    photo: 'https://www.pgatour.com/content/dam/pgatour/players/playerheadshots/46046.png',
    sport: 'Golf',
    statTabs: ['L5', 'L10', '2024', '2023'],
    statTypeTabs: ['WINS', 'TOP 10s', 'ROUNDS', 'EAGLES'],
    statsByTab: {
      L5: {
        WINS: [ { date: '4/1', value: 1 }, { date: '4/8', value: 0 }, { date: '4/15', value: 1 }, { date: '4/22', value: 0 }, { date: '4/29', value: 1 } ],
        'TOP 10s': [ { date: '4/1', value: 1 }, { date: '4/8', value: 1 }, { date: '4/15', value: 1 }, { date: '4/22', value: 1 }, { date: '4/29', value: 1 } ],
        ROUNDS: [ { date: '4/1', value: 4 }, { date: '4/8', value: 4 }, { date: '4/15', value: 4 }, { date: '4/22', value: 4 }, { date: '4/29', value: 4 } ],
        EAGLES: [ { date: '4/1', value: 0 }, { date: '4/8', value: 1 }, { date: '4/15', value: 0 }, { date: '4/22', value: 0 }, { date: '4/29', value: 1 } ]
      },
      // ...other tabs
    },
    line: 0.5,
    overPercent: 60,
    gameLog: [ { player: 'Scottie Scheffler', result: 1, line: 0.5, odds: '2.5', hit: true }, { player: 'Scottie Scheffler', result: 0, line: 0.5, odds: '2.5', hit: false } ],
    supportingStats: [ { label: 'Wins', value: 1 }, { label: 'Top 10s', value: 1 }, { label: 'Rounds', value: 4 }, { label: 'Birdies', value: 5 } ],
  },
]; 