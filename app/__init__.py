from flask import Flask, render_template, request, redirect, session, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash




db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.secret_key = "secret"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///pokemon_league.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = "dev-secret-key"

    db.init_app(app)
    Migrate(app, db)
    from app.models.user import User
    from app.models import user, team, pokemon
    
    @app.route("/")
    def index():
        if "username" in session:
            return redirect(url_for("dashboard"))
        return render_template("index.html")
    @app.route("/login", methods=["POST"])
    def login():
        username = request.form["username"]
        password = request.form["password"]
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            session["username"] = user.username
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
        session["username"] = new_user.username
        return redirect(url_for('dashboard'))
    @app.route("/dashboard")
    def dashboard():
        if "username" not in session:
            return redirect(url_for("index"))
        return render_template("dashboard.html", username=session["username"])
    @app.route("/logout")
    def logout():
        session.pop("username", None)
        return redirect(url_for("index"))
    return app