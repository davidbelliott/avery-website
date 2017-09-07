import facebook
import re
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools as tools
from oauth2client.file import Storage

import datetime
import udatetime

from flask import Blueprint, render_template, current_app

main = Blueprint('main', __name__)

def google_get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    credential_dir = 'instance/credentials'
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir, 'avery_website.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(current_app.config['GOOGLE_CLIENT_SECRET_FILE'], current_app.config['GOOGLE_SCOPES'])
        flow.user_agent = current_app.config['GOOGLE_APPLICATION_NAME']
        flow.params['access_type'] = 'offline'
        credentials = tools.run_flow(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/gallery')
def gallery():
    graph = facebook.GraphAPI(current_app.config['FACEBOOK_APP_ID'] + '|' + current_app.config['FACEBOOK_APP_SECRET'])
    albums = graph.get_object(id='averyglory/albums', fields='name,cover_photo{images}')
    for album in albums['data']:
        album['cover_photo']['medium_index'] = min(current_app.config['FACEBOOK_IMAGE_SIZE_INDEX'], len(album['cover_photo']['images']) - 1)
        album['name_stripped'] = re.sub("\[([^]]+)\]", "", album['name'])
    print(albums)
    return render_template('gallery.html', albums=[album for album in albums['data'] if album['name'] != 'Profile Pictures' and album['name'] != 'Cover Photos'])

@main.route('/gallery/album/<album_id>')
def gallery_album(album_id):
    graph = facebook.GraphAPI(current_app.config['FACEBOOK_APP_ID'] + '|' + current_app.config['FACEBOOK_APP_SECRET'])
    album = graph.get_object(id=album_id, fields='name, photos{images}')
    print(album)
    for photo in album['photos']['data']:
        photo['medium_index'] = min(current_app.config['FACEBOOK_IMAGE_SIZE_INDEX'], len(photo['images']) - 1)
    print(album)
    return render_template('album.html', album=album)

@main.route('/events')
def events():
    credentials = google_get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    print('Getting the upcoming 10 events')
    eventsResult = service.events().list(
        calendarId='primary', timeMin=now, maxResults=10, singleEvents=True,
        orderBy='startTime').execute()
    events = eventsResult.get('items', [])

    for event in events:
        all_day = bool(event['start'].get('date'))
        start = udatetime.from_string(event['start'].get('dateTime', event['start'].get('date')))
        end = udatetime.from_string(event['end'].get('dateTime', event['end'].get('date')))

        start_showdate = True
        start_showtime = not all_day
        end_showdate = end.year != start.year or end.month != start.month or end.day != start.day
        end_showtime = not all_day

        date_str = '%Y-%m-%d'
        time_str = '%-H:%M %p'
        sepr_str = ', '

        start_format = date_str + (sepr_str + time_str) if start_showtime else ''
        end_format = date_str if end_showdate else ''           \
            + sepr_str if end_showdate and end_showtime else '' \
            + time_str if end_showtime else ''

        timedate_str = start.strftime(start_format) + (' - ' if end_format else '') + end.strftime(end_format)

        event['timeDateStr'] = timedate_str
        print(start, event['summary'])

    return render_template('events.html', events=events)

@main.route('/government')
def government():
    return render_template('government.html')
