from flask import Flask, render_template, request, redirect, session, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash


db = SQLAlchemy()
csrf = CSRFProtect()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///pokemon_league.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = "dev-secret-key"

    csrf.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    Migrate(app, db)
    from app.models.team import Team
    from app.models.user import User
    from app.models import user, team, pokemon
    from app.models.pokemon import Pokemon
    login_manager.login_view = "index"

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    @app.route("/")
    def index():
        if current_user.is_authenticated:
            return redirect(url_for("dashboard"))
        return render_template("index.html")
    
    @app.route("/login", methods=["POST"])
    def login():
        username = request.form["username"]
        password = request.form["password"]
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('dashboard'))
        return redirect(url_for('index'))
    
    @app.route("/register", methods=["POST"])
    def register():
        username = request.form["username"]
        password = request.form["password"]
        user = User.query.filter_by(username=username).first()
        if user:
            return redirect(url_for('index'))
        new_user = User(username=username)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for('dashboard'))
    
    @app.route("/dashboard")
    @login_required
    def dashboard():
        if not current_user.is_authenticated:
            return redirect(url_for("index"))
        return render_template("dashboard.html", username=current_user.username)
    
    @app.route("/logout")
    @login_required
    def logout():
        logout_user()
        return redirect(url_for("index"))
    
    @app.route("/pokemon")
    @login_required
    def pokemon_list():
        all_pokemon = Pokemon.query.filter_by(drafted_by=None).all()
        return render_template("pokemon_list.html", pokemons=all_pokemon)
    
    @app.route("/teams", methods=["GET", "POST"])
    @login_required
    def teams():
        if request.method == "POST":
            team_name = request.form["team_name"]
            new_team = Team(name=team_name, owner_id=current_user.id)
            db.session.add(new_team)
            db.session.commit()
            return redirect(url_for("teams"))
        user_teams = Team.query.filter_by(owner_id=current_user.id).all()
        return render_template("teams.html", teams=user_teams)
    
    @app.route("/teams/<int:team_id>")
    @login_required
    def team_detail(team_id):
        team = Team.query.get_or_404(team_id)
        return render_template("team_detail.html", team=team)

    return app
# python run.py