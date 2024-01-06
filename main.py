# MIT License
# Copyright (c) 2023 Prem Patel
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# Prem-ium (Prem Patel)
# 🎵 Python script that generates Spotify playlist full of top played tracks & artists. 🎶
# Github Repository: https://github.com/Prem-ium/Spotify-Wrapped-365

import os, time, json, base64, traceback, datetime

import spotipy
import gspread
import apprise

import pandas                           as pd

from spotipy.oauth2                     import SpotifyOAuth
from oauth2client.service_account       import ServiceAccountCredentials
from pytz                               import timezone
from dotenv                             import load_dotenv

# Load ENV
load_dotenv()

# Spotify Credentials
if not os.environ["CLIENT_ID"] or not os.environ["SECRET_CLIENT_ID"] or not os.environ["REDIRECT_URL"] or not os.environ["USERNAME"]:
    raise Exception("Variables are missing within the .env file. Please ensure you have CLIENT_ID, SECRET_CLIENT_ID, REDIRECT_URL, and USERNAME set.")
else:
    # Update with your own Spotify Credentials (Client ID, Secret Client ID, redirect, and username)
    SPOTIPY_CLIENT = os.environ['CLIENT_ID']
    SPOTIPY_SECRET_CLIENT = os.environ['SECRET_CLIENT_ID']
    SPOTIPY_REDIRECT = os.environ['REDIRECT_URL']
    SCOPE = "user-top-read playlist-modify-private playlist-modify-public user-library-modify user-library-read playlist-read-private ugc-image-upload"
    USERNAME = os.environ['USERNAME']

    # Get Spotify OAuth token without user input
    sp_oauth = SpotifyOAuth(client_id=SPOTIPY_CLIENT, client_secret=SPOTIPY_SECRET_CLIENT,
                            redirect_uri=SPOTIPY_REDIRECT, scope=SCOPE, username=USERNAME, open_browser=False)
    if (os.environ.get("GITHUB_ACTIONS", "false").lower() == "true"):
        GITHUB_ACTIONS = True
        if os.environ.get('AUTH_CACHE', None) is not None:
            token_info = json.loads(os.environ['AUTH_CACHE'])
            SP = spotipy.Spotify(auth=token_info['access_token'])
        else:
            # Aware of the fact that this is not the best way to do this, but it works for now
            token_info = sp_oauth.get_access_token()
            print(f'Assign the following to the AUTH_CACHE secrets variable, within GitHub Actions Secrets page:\n{token_info}\n\n')
            SP = spotipy.Spotify(auth=token_info['access_token'])
    else:
        GITHUB_ACTIONS = False
        SP = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT, client_secret=SPOTIPY_SECRET_CLIENT,
                                                   redirect_uri=SPOTIPY_REDIRECT, scope=SCOPE, username=USERNAME, open_browser=False))
    USER_ID = SP.current_user()['id']
    
# Whether to use keep_alive.py
if (os.environ.get("KEEP_ALIVE", "false").lower() == "true"):
    from keep_alive                     import keep_alive
    keep_alive()

PLAYLIST_TYPE = True if os.environ.get(
    "PUBLIC_PLAYLIST", "true").lower() == "true" else False

# How many seconds should the program wait until executing again
WAIT = float(os.environ.get('MINUTES', 360)) * 60.0

RECCOMENDATIONS = True if os.environ.get("RECCOMENDATIONS", "False").lower() == "true" else False

# Set up Apprise, if enabled
APPRISE_ALERTS = os.environ.get("APPRISE_ALERTS")
if APPRISE_ALERTS:
    APPRISE_ALERTS = APPRISE_ALERTS.split(",")

TZ = timezone(os.environ.get("TZ", "America/New_York"))

# Initialize Google Sheets, if enabled
GOOGLE_SHEETS = os.environ.get("GSPREAD_KEYS", False)
if GOOGLE_SHEETS:
    # gspread / Google Sheets API
    GSscope = ["https://spreadsheets.google.com/feeds",
               "https://www.googleapis.com/auth/drive"]
    # Update with your own JSON Enviornment Variable
    my_secret = json.loads(os.environ['GSPREAD_KEYS'])
    creds = ServiceAccountCredentials.from_json_keyfile_dict(
        my_secret, GSscope)
    gc = gspread.authorize(creds)
    # Open exisiting Google Sheets document named Wrapped365
    sh = gc.open('Wrapped365')

def apprise_init():
    if APPRISE_ALERTS:
        alerts = apprise.Apprise()
        for service in APPRISE_ALERTS:
            alerts.add(service)
        return alerts

# Returns top artists within a time period
def get_top_artists(time_period):
    top_artists = SP.current_user_top_artists(limit=50, time_range=time_period)
    artist_info = []
    for artist in top_artists['items']:
        if GOOGLE_SHEETS:
            artist_info.append([artist['name'], artist['external_urls']
                            ['spotify'], artist['images'][0]['url']])
        else:
            artist_info.append([artist['name'], artist['external_urls']['spotify']])
    return artist_info

# Returns id of tracks
def get_track_ids(time_frame):
    track_ids = []
    for song in time_frame['items']:
        track_ids.append(song['id'])
    return track_ids

# Returns meta data of tracks
def get_track_features(id):
    meta = SP.track(id)
    name = meta['name']
    album = meta['album']['name']
    artist = meta['album']['artists'][0]['name']
    spotify_url = meta['external_urls']['spotify']
    album_cover = meta['album']['images'][0]['url']
    track_info = [name, album, artist, spotify_url, album_cover]
    return track_info

# insert tracks into google sheets
def insert_to_gsheet(track_ids, artist_info, time_period):
    # List of track IDs, get meta data of tracks, and insert into Google Sheets
    tracks = []
    for i in range(len(track_ids)):
        track = get_track_features(track_ids[i])
        tracks.append(track)
    df = pd.DataFrame(
        tracks, columns=['name', 'album', 'artist', 'spotify_url', 'album_cover'])
    worksheet = sh.worksheet(f'{time_period}')
    worksheet.update([df.columns.values.tolist()] + df.values.tolist())
    print(time_period + ' Tracks Done.')

    # Insert top artists into Google Sheets
    df = pd.DataFrame(artist_info, columns=[
                      'name', 'spotify_url', 'artist_cover'])
    worksheet = sh.worksheet(f'{time_period} Artists')
    worksheet.update([df.columns.values.tolist()] + df.values.tolist())
    print(time_period + ' Artist Done.')

    return tracks

def update_playlist(playlists, playlistTitle, playlistDescription, track_ids, time_period, imagePath = None):
    imagePath = f"covers/{imagePath}.jpg"

    for playlist in playlists['items']:
        if playlist['name'] == f'{playlistTitle}':
            playlist_id = playlist['id']
            # Update songs in existing playlist
            SP.user_playlist_replace_tracks(USER_ID, playlist_id, track_ids)
            SP.user_playlist_change_details(USER_ID, playlist_id, f'{playlistTitle}', description = playlistDescription)

            with open(imagePath, 'rb') as image:
                cover_encoded = base64.b64encode(image.read()).decode("utf-8")
            SP.playlist_upload_cover_image(playlist_id, cover_encoded)
            print(f'{playlistTitle} Playlist Updated.\nhttps://open.spotify.com/playlist/{playlist_id}\n\n')
            
            return playlist_id

    playlist_id = SP.user_playlist_create(USER_ID, f'{playlistTitle}', public=PLAYLIST_TYPE, collaborative=False,description=playlistDescription)['id']
    SP.user_playlist_add_tracks(USER_ID, playlist_id, track_ids)
    with open(imagePath, 'rb') as image:
        cover_encoded = base64.b64encode(image.read()).decode("utf-8")
    SP.playlist_upload_cover_image(playlist_id, cover_encoded)
    print(f'{playlistTitle} Playlist Created. \nhttps://open.spotify.com/playlist/{playlist_id}\n\n')
    return playlist_id

# Generates/Updates Recommended Playlist based on first 5 top tracks & artists
def generate_recommended(time_period, playlist_id, playlists):
    print('Generating Recommended Playlist (This may take a while)...')
    seed_tracks, seed_artists = [], []
    top_artists = SP.current_user_top_artists(limit=6, offset=0, time_range=time_period)
    seed_tracks = [track['track']['uri'] for track in SP.playlist_tracks(playlist_id, limit=5)['items']]
    seed_artists = [artist['uri'] for artist in top_artists['items'][:5]]

    recommendations = SP.recommendations(seed_tracks=seed_tracks, limit=25)
    recommended_track_uris = [track['uri'] for track in recommendations['tracks']]

    title = f'{time_period} Recommended: Wrapped 365'
    description = f'Recommended playlist curated based on my top tracks. Generated using Prem-ium\'s Wrapped365 Python Project. Updated every {WAIT/3600} hours. Last Updated {datetime.datetime.now(TZ).strftime("%I:%M%p %m/%d")} https://github.com/Prem-ium/Spotify-Wrapped-365'
    playlist_id = update_playlist(playlists, title, description, recommended_track_uris, time_period, imagePath = f'recommend_{time_period}')

   # Display Top 5 Recommended Artists based on Time Period
    artist_recommendations = SP.recommendations(seed_artists=seed_artists, limit=5)
    artist = f"Top Recommended Artists for {time_period}\n"
    print(artist)
    for i in range(0, 5):
        try:
            print(f"{i + 1}: {artist_recommendations['tracks'][i]['artists'][0]['name']}")
            artist += f"{i + 1}: {artist_recommendations['tracks'][i]['artists'][0]['name']}\n"
        except:
            pass
    
    if APPRISE_ALERTS:
        alerts.notify(title=f'Top Recommended Artists for {time_period}', body=artist)

def Wrapped():
    if APPRISE_ALERTS:
        alerts.notify(title=f'Spotify Wrapped 365 Starting!',body=f'{datetime.datetime.now(TZ).strftime("%I:%M%p %m/%d")}')

    time_ranges = ['short_term', 'medium_term', 'long_term']
    words = ["One Month", "Six Months", "Lifetime"]
    for i in range(0, 3):
        time_range = time_ranges[i]
        time_period = words[i]
        
       # print(
       #     f'\n------------------------------------------------------------------------------------' +
       #                                     f'\n\t\t\t\t\t\t\tStarting {time_range}'+
       #     f'\n------------------------------------------------------------------------------------\n')
        print(f'\n{"-"*88}\n{f"Starting {time_range}".upper().center(88)}\n{"-"*88}\n')

        # Get Top Tracks & Track IDs
        print(f'Getting {time_period} Top Tracks...')
        top_tracks = SP.current_user_top_tracks(limit=50, offset=0, time_range=time_range)
        track_ids = get_track_ids(top_tracks)
        print(f'{len(track_ids)} Top Tracks Found for {time_period}.\n\n')

        # Get Top Artists
        print(f'Getting {time_period} Top Artists...')
        top_artists = get_top_artists(time_range)
        print(f'{len(top_artists)} Top Artists Found for {time_period}.\n\n')
        

        # Get Playlists
        userPlaylists = SP.current_user_playlists()

        # Generate, Create, or Update Top Tracks Playlist
        print(f'Generating/Updating {time_period} Top Tracks Playlist...')
        title = f'{time_period} - Top Tracks Wrapped'
        description = f'My Top Played Tracks for {time_period}. Last Updated {datetime.datetime.now(TZ).strftime("%I:%M%p %m/%d")}. Updated every {WAIT/3600} hours. Generated using Prem-ium\'s GitHub: https://github.com/Prem-ium/Spotify-Wrapped-365'
        playlist_id = update_playlist(playlists = userPlaylists, playlistTitle=title, playlistDescription=description, track_ids=track_ids, time_period=time_range, imagePath = time_range)

        # Handle Google Sheets, if enabled
        if GOOGLE_SHEETS:
            print(f'Inserting {time_period} Top Tracks & Artists into Google Sheets...\n\n')
            # Insert Top Tracks & Artists into Google Sheets
            insert_to_gsheet(track_ids, top_artists, time_range)
        else:
            # Print Top Artists for Time Period
            most_played_artists = "\nTop Artists for {}:\n".format(time_period)
            most_played_artists += "\n".join("{}: {}".format(i+1, artist[0]) for i, artist in enumerate(top_artists))

            print(f'\n{most_played_artists}\n\n')

            # Send an alert to the user of data, if enabled
            if APPRISE_ALERTS:
                alerts.notify(title=f'Top Artists for {time_period}', body=most_played_artists)

        if RECCOMENDATIONS:
            try:    generate_recommended(time_range, playlist_id, playlists=userPlaylists)
            except: print(traceback.format_exc())
        print(f'\n{"-"*88}\n{f"Finished {time_range}".upper().center(88)}\n{"-"*88}\n\n')

    if APPRISE_ALERTS:
        alerts.notify(title=f'Wrapped365 Finished!',
                      body='Top Artists and Tracks Updated!')


def main():
    info = f'\nGenerated Spotify Wrapped 365 Playlists!\nThanks for using Prem-ium\'s Wrapped 365 project!\nPlease leave a star if you found this project cool!\nhttps://github.com/Prem-ium/Spotify-Wrapped-365\n\nSleeping for {WAIT / 3600} hours until updating your stats...\n'
    while True:
        try:
            Wrapped()
            print(f'\n{"-"*88}\n{f"{info}".center(88)}\n{"-"*88}\n')
            if not GITHUB_ACTIONS:   time.sleep(WAIT)
            else:                    break
        except Exception as e:
            print(f'\Exception:\n{e}\n\n{traceback.format_exc()}\n\n')
            if APPRISE_ALERTS:  alerts.notify(title=f'Wrapped365 Exception.', body=f'{e}\nAttempting to restart in 15 minutes...')
            time.sleep(900)
    
if __name__ == '__main__':
    if APPRISE_ALERTS:
        alerts = apprise_init()
    main()