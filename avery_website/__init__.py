import os
from flask import Flask

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object('config')

    from .views import main as main
    app.register_blueprint(main)


    return app
