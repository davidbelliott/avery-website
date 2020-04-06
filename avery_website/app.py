from flask import Flask
import subprocess

app = Flask(__name__)
app.config.from_pyfile('config.py')
app.config.from_pyfile('instance/config.py', silent=True)

def constitution_hook():
    hook = app.config["CONSTITUTION_UPDATE_HOOK"]
    if hook:
        try:
            subprocess.Popen(hook)
        except FileNotFoundError:
            pass

