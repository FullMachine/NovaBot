"""
API endpoints configuration for different sports data providers.
"""

# NBA API endpoints
NBA_API = {
    'base_url': 'https://api.basketball.api-sports.io',
    'endpoints': {
        'players': '/players',
        'teams': '/teams',
        'games': '/games',
        'statistics': '/statistics',
        'standings': '/standings'
    }
}

# NFL API endpoints
NFL_API = {
    'base_url': 'https://api.football.api-sports.io',
    'endpoints': {
        'players': '/players',
        'teams': '/teams',
        'games': '/games',
        'statistics': '/statistics',
        'standings': '/standings'
    }
}

# Soccer API endpoints
SOCCER_API = {
    'base_url': 'https://api.football.api-sports.io',
    'leagues': {
        'epl': 39,      # Premier League
        'laliga': 140,  # La Liga
        'bundesliga': 78,
        'seriea': 135,
        'ligue1': 61,
        'mls': 253,
        'ucl': 2        # Champions League
    },
    'endpoints': {
        'fixtures': '/fixtures',
        'standings': '/standings',
        'teams': '/teams',
        'players': '/players',
        'statistics': '/statistics'
    }
}

# Racing API endpoints
RACING_API = {
    'f1': {
        'base_url': 'https://api.formula1.com/v1',
        'endpoints': {
            'drivers': '/drivers',
            'races': '/races',
            'standings': '/standings',
            'results': '/results'
        }
    },
    'nascar': {
        'base_url': 'https://api.nascar.com/v1',
        'endpoints': {
            'drivers': '/drivers',
            'races': '/races',
            'standings': '/standings',
            'results': '/results'
        }
    }
}

# Baseball API endpoints
BASEBALL_API = {
    'kbo': {
        'base_url': 'https://api.kbo.com/v1',
        'endpoints': {
            'players': '/players',
            'teams': '/teams',
            'games': '/games',
            'standings': '/standings'
        }
    },
    'npb': {
        'base_url': 'https://api.npb.jp/v1',
        'endpoints': {
            'players': '/players',
            'teams': '/teams',
            'games': '/games',
            'standings': '/standings'
        }
    },
    'bbl': {
        'base_url': 'https://api.cricket.com.au/v1',
        'endpoints': {
            'players': '/players',
            'teams': '/teams',
            'matches': '/matches',
            'standings': '/standings'
        }
    }
}

# Esports API endpoints
ESPORTS_API = {
    'base_url': 'https://api.pandascore.co',
    'games': {
        'lol': '/lol',
        'dota2': '/dota2',
        'csgo': '/csgo',
        'valorant': '/valorant',
        'overwatch': '/ow'
    },
    'endpoints': {
        'matches': '/matches',
        'tournaments': '/tournaments',
        'teams': '/teams',
        'players': '/players'
    }
} 