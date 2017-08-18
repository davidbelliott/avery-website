from flask import Blueprint, render_template

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/gallery')
def gallery():
    return render_template('gallery.html')

@main.route('/calendar')
def calendar():
    return render_template('calendar.html')

@main.route('/government')
def government():
    return render_template('government.html')

@main.route('/tools')
def tools():
    return 'This is the tools page'
