from flask import Flask
from flask_socketio import SocketIO
import redis

app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('config.py')

socketio = SocketIO(app)

redis = redis.StrictRedis(host='localhost', port=6379, db=0)
