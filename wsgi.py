#!/usr/bin/env python
from avery_website.main import app, socketio

if __name__ == "__main__":
	socketio.run(app)
