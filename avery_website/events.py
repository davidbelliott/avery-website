from .app import socketio
from flask_socketio import emit

@socketio.on('connect')
def on_connect():
    print("Connected")

@socketio.on('disconnect')
def on_disconnect():
    print("Disconnected")

@socketio.on('aaa')
def on_aaa():
    emit('aaa_response')

@socketio.on('get_all_tracks')
def on_get_all_tracks():
    print("All tracks")
    emit('new_tracks', ['yt:https://www.youtube.com/watch?v=WYQ95pJFsiE', 'b', 'c'])
