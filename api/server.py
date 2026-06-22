from flash import Flask
from server.routes import setup_routes

def create_server(ai, session):
    app = Flask(__name__)

    setup_routes(app, ai, session)
    return app