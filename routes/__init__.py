from .events import register_event_routes
from .programs import register_programs_routes
from .games import register_games_routes
from .sounds import register_sound_routes
from .api import register_api_routes

def register_routes(app):
    register_event_routes(app)
    register_programs_routes(app)
    register_games_routes(app)
    register_api_routes(app)
    register_sound_routes(app)
