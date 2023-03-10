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

import os, time, json, base64, traceback

import spotipy
import gspread
import apprise

import pandas                           as pd

from spotipy.oauth2                     import SpotifyOAuth
from oauth2client.service_account       import ServiceAccountCredentials
from dotenv                             import load_dotenv

# Load ENV
load_dotenv()

# Spotify Credentials
if not os.environ["CLIENT_ID"] or not os.environ["SECRET_CLIENT_ID"] or not os.environ["REDIRECT_URL"] or not os.environ["USERNAME"]:
    raise Exception(
        "Variables are missing within the .env file. Please ensure you have CLIENT_ID, SECRET_CLIENT_ID, REDIRECT_URL, and USERNAME set.")
else:
    # Update with your own Spotify Credentials (Client ID, Secret Client ID, redirect, and username)
    SPOTIPY_CLIENT = os.environ['CLIENT_ID']
    SPOTIPY_SECRET_CLIENT = os.environ['SECRET_CLIENT_ID']
    SPOTIPY_REDIRECT = os.environ['REDIRECT_URL']
    SCOPE = "user-top-read playlist-modify-private playlist-modify-public user-library-modify user-library-read playlist-read-private ugc-image-upload"
    USERNAME = os.environ['USERNAME']

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

# Whether to use keep_alive.py
if (os.environ.get("KEEP_ALIVE", "false").lower() == "true"):
    from keep_alive import keep_alive
    keep_alive()

PLAYLIST_TYPE = True if os.environ.get(
    "PUBLIC_PLAYLIST", "true").lower() == "true" else False

# How many seconds should the program wait until executing again
WAIT = float(os.environ.get('MINUTES', 360)) * 60.0

RECCOMENDATIONS = True if os.environ.get(
    "RECCOMENDATIONS", "False").lower() == "true" else False

# Set up Apprise, if enabled
APPRISE_ALERTS = os.environ.get("APPRISE_ALERTS")
if APPRISE_ALERTS:
    APPRISE_ALERTS = APPRISE_ALERTS.split(",")

def apprise_init():
    if APPRISE_ALERTS:
        alerts = apprise.Apprise()
        # Add all services from .env
        for service in APPRISE_ALERTS:
            alerts.add(service)
        return alerts

# Returns top artists within a time period
def get_top_artists(time_period):
    top_artists = sp.current_user_top_artists(limit=50, time_range=time_period)
    artist_info = []
    for artist in top_artists['items']:
        if GOOGLE_SHEETS:
            artist_info.append([artist['name'], artist['external_urls']
                            ['spotify'], artist['images'][0]['url']])
        else:
            artist_info.append([artist['name'], artist['external_urls']
                            ['spotify']])
    return artist_info

# Returns id of tracks
def get_track_ids(time_frame):
    track_ids = []
    for song in time_frame['items']:
        track_ids.append(song['id'])
    return track_ids

# Returns meta data of tracks
def get_track_features(id):
    meta = sp.track(id)
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

# Generates/Updates Recommended Playlist based on first 5 top tracks & artists
def generate_recommended(time_period, playlist_id, playlists):
    seed_tracks, seed_artists = [], []
    user_id = sp.current_user()['id']
    top_artists = sp.current_user_top_artists(
        limit=6, offset=0, time_range=time_period)
    for i in range(0, 5):
        seed_tracks.append(sp.playlist_tracks(playlist_id)['items'][i]['track']['uri'])
        try:    seed_artists.append(top_artists['items'][i]['uri'])
        except IndexError: pass

    recommendations = sp.recommendations(seed_tracks=seed_tracks, limit=25)
    recommended_track_uris = [track['uri'] for track in recommendations['tracks']]

    playlistExists = False
    for playlist in playlists['items']:
        if playlist['name'] == f'Recommended: Wrapped 365':
            playlist_id = playlist['id']
            if time_period == 'short_term':
                sp.user_playlist_replace_tracks(
                    user_id, playlist_id, recommended_track_uris)
            else:
                sp.user_playlist_add_tracks(user_id, playlist_id, recommended_track_uris)
            sp.user_playlist_change_details(
                user_id, playlist_id, description=f'Recommended playlist curated based on my top tracks. Generated using Prem-ium\'s Wrapped365 Python Project. Updated every {WAIT/3600} hours. https://github.com/Prem-ium/Spotify-Wrapped-365')
            with open(f"covers/rec.jpg", 'rb') as image:
                cover_encoded = base64.b64encode(image.read()).decode("utf-8")
                sp.playlist_upload_cover_image(playlist_id, cover_encoded)
            playlistExists = True
            break

    # Create playlist
    if not playlistExists:
        playlist_id = sp.user_playlist_create(user_id, f'Recommended: Wrapped 365', public=PLAYLIST_TYPE, collaborative=False,
                                              description=f'Recommended playlist curated based on my top tracks. Generated using Prem-ium\'s Wrapped365 Python Project. Updated every {WAIT/3600} hours. https://github.com/Prem-ium/Spotify-Wrapped-365')['id']
        sp.user_playlist_add_tracks(
            user_id, playlist_id, recommended_track_uris)
        with open(f"covers/rec.jpg", 'rb') as image:
            cover_encoded = base64.b64encode(image.read()).decode("utf-8")
            sp.playlist_upload_cover_image(playlist_id, cover_encoded)

    # Display Top 5 Recommended Artists based on Time Period
    artist_recommendations = sp.recommendations(seed_artists=seed_artists, limit=5)
    artist = f"Top 5 Recommended Artists for {time_period}\n"

    for i in range(0, 5):
        artist += f"{i + 1}: {artist_recommendations['tracks'][i]['artists']['name']}\n"

    try:    print(f'Recommended Playlist Created/Updated!\n{artist}')
    except: pass

    if APPRISE_ALERTS:
        alerts.notify(
            title=f'Top 5 Recommended Artists for {time_period}', body=artist)

    return


def Wrapped():
    print('\n------------------------------------------------------------------------------------------------------------------------------------------\n')
    if APPRISE_ALERTS:
        alerts.notify(title=f'Wrapped365 Starting...',
                      body='Top Artists and Tracks starting to update...')

    time_ranges = ['short_term', 'medium_term', 'long_term']
    for time_period in time_ranges:
        print(
            f'\n------------------------------------------Starting {time_period}------------------------------------------\n')

        # Reset PlayList Exist variable
        playlistExists = False

        # Get Top Tracks
        top_tracks = sp.current_user_top_tracks(
            limit=50, offset=0, time_range=time_period)
        track_ids = get_track_ids(top_tracks)

        # Get Top Artists
        top_artists = get_top_artists(time_period)
        period = time_period.replace("_", " ")

        if GOOGLE_SHEETS:
            # Insert Top Tracks & Artists into Google Sheets
            insert_to_gsheet(track_ids, top_artists, time_period)
        else:
            most_played_artists = f"------\nTop Artists for {period}:\n"
            # Loop through top artists while having an index
            for i, artist in enumerate(top_artists):
                most_played_artists += f"{i + 1}: {artist[0]}\n"
            most_played_artists += f"\n\n------"
            print(most_played_artists)
            if APPRISE_ALERTS:
                alerts.notify(
                    title=f'Top Artists for {period}', body=most_played_artists)

        # get list of user's playlists & iterate over it to prevent duplication
        playlists = sp.current_user_playlists()

        for playlist in playlists['items']:
            if playlist['name'] == f'{period} - Top Tracks Wrapped':
                playlist_id = playlist['id']
                # Update songs in existing playlist
                sp.user_playlist_replace_tracks(
                    USERNAME, playlist_id, track_ids)
                sp.user_playlist_change_details(
                    USERNAME, playlist_id, description=f'My Top Played Tracks for {period}. Generated using Prem-ium\'s Wrapped365 Python Project. Updated every {WAIT/3600} hours. https://github.com/Prem-ium/Spotify-Wrapped-365')
                playlistExists = True
                print(f'\n{period} Top Tracks playlist updated.\n\n')
                break

        # Create playlist
        if not playlistExists:
            playlist_id = sp.user_playlist_create(USERNAME, f'{period} - Top Tracks Wrapped', public=PLAYLIST_TYPE, collaborative=False,
                                                  description=f'My Top Played Tracks for {period}. Generated using Prem-ium\'s Wrapped365 Python Project. Updated every {WAIT/3600} hours. https://github.com/Prem-ium/Spotify-Wrapped-365')['id']
            sp.user_playlist_add_tracks(USERNAME, playlist_id, track_ids)
            with open(f"covers/{time_period}.jpg", 'rb') as image:
                cover_encoded = base64.b64encode(image.read()).decode("utf-8")
            sp.playlist_upload_cover_image(playlist_id, cover_encoded)
            print(f'\n{period} Top Tracks playlist created.\n\n')

        if RECCOMENDATIONS:
            generate_recommended(time_period, playlist_id,
                                 playlists=sp.current_user_playlists())

        print(f'------------------------------------------------------------------------------------------------------------------------------------------\n')

    if APPRISE_ALERTS:
        alerts.notify(title=f'Wrapped365 Finished!',
                      body='Top Artists and Tracks Updated!')


def main():
    while True:
        try:
            Wrapped()
            print(
                f'\nAll done!\nThanks for using Prem-ium\'s Wrapped 365 project, please share it with your friends!\nSleeping for {WAIT / 3600} hours until updating your stats...\n')
            time.sleep(WAIT)
            
        except Exception as e:
            print(f'\Exception:\n{e}\n\n{traceback.format_exc()}\n\n')
            if APPRISE_ALERTS:
                alerts.notify(title=f'Wrapped365 Exception.',
                              body=f'{e}\nAttempting to restart in 15 minutes...')
            time.sleep(900)
            continue


if __name__ == '__main__':
    if APPRISE_ALERTS:
        alerts = apprise_init()

    # Initialize Spotify
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT, client_secret=SPOTIPY_SECRET_CLIENT,
                                                   redirect_uri=SPOTIPY_REDIRECT, scope=SCOPE, username=USERNAME, open_browser=False))
    
    main()
