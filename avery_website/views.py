from flask import Blueprint, render_template

main = Blueprint('main', __name__)

@main.route('/')
def hello_world():
    return 'Hello, World!'
