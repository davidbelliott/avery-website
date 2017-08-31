import facebook
from flask import Blueprint, render_template

FACEBOOK_APP_ID = '261003164413097'
FACEBOOK_APP_SECRET = '31c63be403ce8ac70e6d1441ebe84b85'
IMAGE_SIZE_INDEX = 2

graph = facebook.GraphAPI(FACEBOOK_APP_ID + '|' + FACEBOOK_APP_SECRET)

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/gallery')
def gallery():
    albums = graph.get_object(id='averyglory/albums', fields='name,cover_photo{images}')
    for album in albums['data']:
        album['cover_photo']['medium_index'] = min(IMAGE_SIZE_INDEX, len(album['cover_photo']['images']) - 1)
    print(albums)
    return render_template('gallery.html', albums=[album for album in albums['data'] if album['name'] != 'Profile Pictures' and album['name'] != 'Cover Photos'])

@main.route('/gallery/album/<album_id>')
def album(album_id):
    return 'Album ' + album_id

@main.route('/calendar')
def calendar():
    return render_template('calendar.html')

@main.route('/government')
def government():
    return render_template('government.html')

@main.route('/tools')
def tools():
    return 'This is the tools page'
