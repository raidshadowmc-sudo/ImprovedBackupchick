from flask import jsonify, request
from app import app
from models import Player

@app.route('/api/leaderboard')
def api_leaderboard():
    """API endpoint for leaderboard data with fallback"""
    try:
        sort_by = request.args.get('sort', 'experience')
        limit = min(int(request.args.get('limit', 50)), 100)

        players = Player.get_leaderboard(sort_by=sort_by, limit=limit) or []

        # Convert players to dict format
        players_data = []
        for player in players:
            players_data.append({
                'id': player.id,
                'nickname': player.nickname,
                'level': player.level,
                'experience': player.experience,
                'kills': player.kills,
                'deaths': player.deaths,
                'wins': player.wins,
                'games_played': player.games_played,
                'kd_ratio': player.kd_ratio,
                'win_rate': player.win_rate
            })

        return jsonify({
            'success': True,
            'players': players_data,
            'total': len(players_data)
        })
    except Exception as e:
        app.logger.error(f"Error in API leaderboard: {e}")
        return jsonify({
            'success': False,
            'players': [],
            'total': 0,
            'error': 'Failed to load leaderboard data'
        }), 200  # Still return 200 with empty data

@app.route('/api/stats')
def api_stats():
    """API endpoint for statistics data"""
    try:
        stats = Player.get_statistics()
        # Convert Player objects to dictionaries
        serializable_stats = {}
        for key, value in stats.items():
            if hasattr(value, '__dict__'):  # If it's a model instance
                if hasattr(value, 'nickname'):  # Player object
                    serializable_stats[key] = {
                        'id': value.id,
                        'nickname': value.nickname,
                        'level': value.level,
                        'experience': value.experience,
                        'coins': getattr(value, 'coins', 0),
                        'reputation': getattr(value, 'reputation', 0)
                    }
                else:
                    serializable_stats[key] = str(value)
            else:
                serializable_stats[key] = value
        return jsonify(serializable_stats)
    except Exception as e:
        app.logger.error(f"Error in API stats: {e}")
        return jsonify({'error': 'Failed to load statistics'}), 500