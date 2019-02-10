import flask
import sys
import os
import json
import webbrowser
import numpy
import spotipy
import spotipy.util as util
import indicoio
from googlesearch import search
from progress.bar import ShadyBar # Get rid of if need be
from json.decoder import JSONDecoder
from flask import Flask, Response, request, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
# import flask_login

indicoio.config.api_key = '60b7c73721680f219f9119ab83148b3a'

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

def songScore(sentiments, popularity, searchNum):
    #print(len(sentiments))

    score = (sum(sentiments)/searchNum)
    if popularity > 85:
        if score > 0.2:
            score -= 0.2
        else:
            score = 0
    if popularity < 20:
        if score < 0.75:
            score += 0.25
        else:
            score = 1
    return score

def songcatenate(songTuple):
    if len(" ".join([songTuple[0], songTuple[1], songTuple[2]])) > 70:
        if len(" ".join([songTuple[0], songTuple[1]])) > 50:
            return songTuple[0]
        return (" ".join([songTuple[0], songTuple[1]]))
    return (" ".join([songTuple[0], songTuple[1], songTuple[2]]))

def libraryScore(songList):
    """ """
    # This holds everything
    tempUrls = []

    # SEARCH_NUM changes to fit the number of songs inputted, to avoid overwhelming Indico
    SEARCH_NUM = 10
    if len(songList) > 100:
        SEARCH_NUM = 1
    elif len(songList) > 50:
        SEARCH_NUM = 2
    elif len(songList) > 30:
        SEARCH_NUM = 3
    elif len(songList) > 20:
        SEARCH_NUM = 5
    #TODO delete bar and bar references when adding to Flask, unless it just exists in console
    bar = ShadyBar("Google Searching...", max = len(songList), suffix = '%(percent).1f%% - %(eta)ds')

    # Google API can only search for URLS in increments of 10, so SEARCH_NUM limits the amount
    for i in range(len(songList)):
        n = 0
        #print(songcatenate(songList[i]))
        for url in search(songcatenate(songList[i]) + ' review', stop=SEARCH_NUM):
            n += 1
            if n <= SEARCH_NUM:
                tempUrls += [url]
        bar.next()
    bar.finish()

    #print(tempUrls)

    # exchange sentiment_hq with sentiment if calculation takes too long
    sentiment = indicoio.sentiment(tempUrls, url=True)

    #print(sentiment)

    scores = []
    # Extracts the proper range of sentiments from the crazy big list
    for i in range(len(songList)):
        i_range = sentiment[(i*SEARCH_NUM):(i*SEARCH_NUM)+(SEARCH_NUM)]
        scores += [(songList[i], songScore(i_range, songList[i][3], SEARCH_NUM))]
    # Return Structure: [(("<Song Name>", "<Artist Name>", "<Album Name>", <Popularity Score>), <Final Song Score>)]
    return scores

def get_spotify_token():
    token = util.prompt_for_user_token(username, scope, client_id, client_secret, redirect_uri)
    sp = spotipy.Spotify(auth=token)
    return sp

@app.route('/',methods=['POST', 'GET'])
def home():
    sp =get_spotify_token()
    user = sp.current_user()
    displayName = user['display_name']
    playlists = sp.user_playlists(username)
    list1 = []
    while playlists:
        for i, playlist in enumerate(playlists['items']):
            list1.append((playlist['uri'], playlist['name']))

        if playlists['next']:
            playlists = sp.next(playlists)
        else:
            playlists = None
    print(list1)
    return render_template('hello.html',title="Music Rating",items=list1,dis_name=displayName)


def generate_all_songs(tracks):
    results = []
    #sumpop = 0
    #count = 0
    for track in tracks["items"]:
        song_name = track['track']["name"] # get name of the song

        album_name = track['track']["album"]["name"] # get name of the album

        artist_name = track["track"]["artists"][0]["name"] # get name of the first artist on the track
        pop = track["track"]["popularity"]
        results += [(song_name, artist_name, album_name, pop)]
    #average_pop = sumpop // count

    return results


@app.route('/result',methods = ['POST', 'GET'])
def result():
    mylist = request.form.get('selectPlaylist')
    sp = get_spotify_token()
    playId=mylist.split(':')[-1].split("'")[0]
    tracks=sp.user_playlist_tracks(username,playlist_id=playId)
    search_and_popu = generate_all_songs(tracks)
    score_list = libraryScore(search_and_popu)
    mean_tot=numpy.mean([score_list[i][1] for i in range(len(score_list))])*100
    mean_pop = numpy.mean([score_list[i][0][3] for i in range(len(score_list))])
    # print(json.dumps(tracks, sort_keys=True,indent=4))

    return render_template('result.html',avg_tot=mean_tot,avg_pop=mean_pop)


@app.route('/drop_down',methods=['POST', 'GET'])
def drop_down():

    return render_template('drop_down.html')


if __name__ == '__main__':
    bootstrap = Bootstrap(app)
    app.run(debug=True)


