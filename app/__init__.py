from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///pokemon_league.db"
    app.config["SECRET_KEY"] = "dev-secret-key"

    db.init_app(app)
    Migrate(app, db)

    from app.models import user, team, pokemon

    @app.route("/")
    def index():
        return "Pokemon Draft League - Day 2 "

    return app