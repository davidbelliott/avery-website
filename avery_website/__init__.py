import os
from flask import Flask
from flask_assets import Environment, Bundle

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object('config')
    app.config.from_pyfile('config.py')

    assets = Environment(app)
    assets.append_path(os.path.join(os.path.dirname(__file__), 'assets', 'sass'))
    css = Bundle('all.sass',
            filters='sass',
            output='all.css')
    assets.register('css_all', css)

    from .views import main as main
    app.register_blueprint(main)

    from .extensions import login_manager

    return app
