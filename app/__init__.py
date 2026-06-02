from flask import Flask

def create_app():
    app = Flask(__name__)
    @app.route('/')
    def index():
        return 'Test'
    @app.route('/hello')
    def hello():
        return 'Hello, World!'
    return app