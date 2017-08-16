from flask import Blueprint, render_template

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/gallery')
def gallery():
    return 'This is the gallery'

@main.route('/calendar')
def calendar():
    return 'This is the calendar'

@main.route('/government')
def government():
    return 'This is the government page'

@main.route('/tools')
def tools():
    return 'This is the tools page'
