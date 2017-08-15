from flask import Flask

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object('config')
    app.config.from_pyfile('config.py')

    from .views import main as main_bp
    app.register_blueprint(main_bp)

    return app
