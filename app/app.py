import flask
import sys
import os
import json
import webbrowser
import spotipy.util as util
import spotipy
from json.decoder import JSONDecoder

from flask import Flask, Response, request, render_template, redirect, url_for
# import flask_login



app = Flask(__name__)
# login_manager = flask_login.LoginManager()
# login_manager.init_app(app)

CLIENT_ID = '36feecb46ca04c2f987a737e6eab3477'
CLIENT_SECRET = '757ac79156a74c95a7f5a0af8142c77a'
redirect_uri = 'http://google.com'
scope = 'user-read-currently-playing'

username = "kamoltat"
#userId: https://open.spotify.com/user/kamoltat?si=zwwxCHVLSfKzCJIm8CXXtA

# user = spotifyObject.current_user()
# print(json.dumps(user,sort_keys=True,indent=4))
try:
    token = util.prompt_for_user_token(username, scope, CLIENT_ID, CLIENT_SECRET, redirect_uri)
except:
    print("except hits")
    # os.remove(f".cache-{username}")
    token = util.prompt_for_user_token(username)

sp = spotipy.Spotify(auth=token)
@app.route('/')
def home():
    return 'Hello World!'


@app.route('/drop_down')
def drop_down():
    return ''

    return render_template('top_users.html', message='TopUsers',topUsers = topUsers)

if __name__ == '__main__':

    app.run()


