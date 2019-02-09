import flask
import sys
import os
import json
import webbrowser
import spotipy
import spotipy.util as util
from json.decoder import JSONDecoder

from flask import Flask, Response, request, render_template, redirect, url_for
# import flask_login



app = Flask(__name__)
# login_manager = flask_login.LoginManager()
# login_manager.init_app(app)



redirect_uri = "https://google.com/"
scope = "user-library-read"
client_id="36feecb46ca04c2f987a737e6eab3477"
client_secret="757ac79156a74c95a7f5a0af8142c77a"
username = 'kamoltat'
# birdy_uri = 'spotify:artist:2WX2uTcsvV5OnS0inACecP'
#https://open.spotify.com/user/kamoltat?si=5Us0ZgjUSVGYBHCagQi7UA






token = util.prompt_for_user_token(username,scope,client_id,client_secret,redirect_uri)
sp = spotipy.Spotify(auth=token)
user = sp.current_user()

displayName = user['display_name']
followers = user['followers']['total']
playlists = sp.user_playlists(username)


list1 = []
while playlists:
    for i, playlist in enumerate(playlists['items']):
        list1.append((playlist['uri'],playlist['name']))
        print("%4d %s %s" % (i + 1 , playlist['uri'],  playlist['name']))
    if playlists['next']:
        playlists = sp.next(playlists)
    else:
        playlists = None


@app.route('/')
def home():
    return render_template('hello.html',title="Music Rating",items=list1)


@app.route('/drop_down')
def drop_down():

    return render_template('drop_down.html')

if __name__ == '__main__':

    app.run()


