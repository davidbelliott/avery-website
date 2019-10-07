import re
import facebook
import os
import datetime
import udatetime
import json
import redis
import subprocess
from . import gcal

'''from apiclient import discovery
from oauth2client import client
from oauth2client import tools as tools
from oauth2client.file import Storage'''

from .app import app, strictredis
from .events import socketio
from .forms import MusicSubmitForm

from flask import render_template, redirect, url_for, request

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/gallery')
def gallery():
    graph = facebook.GraphAPI(access_token = app.config['FACEBOOK_PAGE_ACCESS_TOKEN'])
    albums = graph.get_object(id='averyglory/albums', fields='name,cover_photo{images}')
    for album in albums['data']:
        if 'cover_photo' in album:
            album['cover_photo']['medium_index'] = min(app.config['FACEBOOK_IMAGE_SIZE_INDEX'], len(album['cover_photo']['images']) - 1)
        album['name_stripped'] = re.sub("\[([^]]+)\]", "", album['name'])
    print(albums)
    return render_template('gallery.html', albums=[album for album in albums['data'] if album['name'] != 'Profile Pictures' and album['name'] != 'Cover Photos' and 'cover_photo' in album])

@app.route('/gallery/album/<album_id>')
def gallery_album(album_id):
    limit = 100
    graph = facebook.GraphAPI(access_token = app.config['FACEBOOK_PAGE_ACCESS_TOKEN'])
    album = graph.get_object(id=album_id, limit=limit, fields='name, photos{images}')
    album['name_stripped'] = re.sub("\[([^]]+)\]", "", album['name'])
    for photo in album['photos']['data']:
        photo['medium_index'] = min(app.config['FACEBOOK_IMAGE_SIZE_INDEX'], len(photo['images']) - 1)
    print("After: {}".format(album['photos']['paging']['cursors']['after']))
    return render_template('album.html', album=album)

@app.route('/events')
def events():
    events = gcal.get_events()

    for event in events:
        start_date = event['start'].get('date')
        end_date = event['end'].get('date')
        all_day = bool(start_date)
        if all_day:
            start = datetime.datetime.strptime(start_date, "%Y-%m-%d")
            end = datetime.datetime.strptime(end_date, "%Y-%m-%d")
        else:
            start = udatetime.from_string(event['start'].get('dateTime', event['start'].get('date')))
            end = udatetime.from_string(event['end'].get('dateTime', event['end'].get('date')))

        start_showdate = True
        start_showtime = not all_day
        end_showdate = end.year != start.year or end.month != start.month or end.day != start.day
        end_showtime = not all_day

        date_str = '%A %Y-%m-%d'
        time_str = '%-H:%M'
        sepr_str = ', '

        start_format = date_str + ((sepr_str + time_str) if start_showtime else '')
        end_format = date_str if end_showdate else ''           \
            + sepr_str if end_showdate and end_showtime else '' \
            + time_str if end_showtime else ''

        timedate_str = start.strftime(start_format) + (' - ' if end_format else '') + end.strftime(end_format)

        event['timeDateStr'] = timedate_str
        print(start, event['summary'])

    return render_template('events.html', events=events)

@app.route('/constitution')
def constitution():
    return render_template('constitution.html')

@app.route('/constitution/update', methods=["GET", "POST"])
def constitution_update():
    hook = app.config["CONSTITUTION_UPDATE_HOOK"]
    if hook:
        try:
            subprocess.Popen(hook)
        except FileNotFoundError:
            pass
    return redirect(url_for('constitution'))

@app.route('/music', methods=["GET", "POST"])
def music():
    form = MusicSubmitForm()
    online = False
    js = ''
    pos = 0
    try:
        if form.validate_on_submit():
            strictredis.rpush('tracks', form.url.data)
            print(strictredis.lrange('tracks', 0, -1))
            socketio.emit('new_tracks', [form.url.data])
            print('Sent new_tracks')
            return redirect(url_for('music'))
        raw = strictredis.get('playlist')
        if(raw):
            utf8 = raw.decode("utf-8")
            js = json.loads(utf8)
        else:
            js = []
        pos_raw = strictredis.get('pos')
        if(pos_raw):
            pos = pos_raw.decode("utf-8")
            print(pos)
        else:
            pos = "-1"
        online_raw = strictredis.get('music_server_online')
        online = not online_raw is None and bool(int(online_raw))
    except redis.exceptions.ConnectionError:
        online = False
    return render_template('music.html', form=form, online=online, playlist=js, pos=pos)
