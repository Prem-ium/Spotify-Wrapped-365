# Spotify Wrapped 365 
A python bot that utilizes the Spotipy Python library to retrieve a user's top tracks and artists. Then exports the information to Google Sheets AND automatically creates/updates top track playlists every (user specified) number of hours. 


# Installation
Clone the repository using git clone
```bash
  git clone https://github.com/Prem-ium/Spotify-Wrapped-365.git
  ```
Install dependencies using pip3
```bash
  cd Spotify-Wrapped365
  pip3 install -r requirements.txt
```

# Environmental Variables
These are the necessary enviormental variables for the Wrapped to function properly. They must be added.
- `CLIENT_ID`: [Found on Spotify Developer Dashboard](https://developer.spotify.com/dashboard/)
- `SECRET_CLIENT_ID`: [Found on Spotify Developer Dashboard](https://developer.spotify.com/dashboard/)
- `REDIRECT_URL`: The Redirect URL you added when creating the App on Spotify's Developer Dashboard
- `USERNAME`: Your Spotify account username [can be found in Spotify account settings.]([https://developer.spotify.com/dashboard/](https://www.spotify.com/us/account/overview/?utm_source=spotify&utm_medium=menu&utm_campaign=your_account))

Optional:
- `GSPREAD_KEYS`: Your Google Service Account JSON contents obtained via OAuth 2.0 Client ID in Credentials of Google Cloud API.
- `MINUTES`: How many minutes should the program wait until executing again? It is ideal to allow at least 6 hours (or 360 minutes).
- `APPRISE_ALERTS`:  Full list of services and their URLs available here: [found here on Apprise wiki](https://github.com/caronc/apprise/wiki).
# Configuration 

### Set First: Spotify Developer Account
Generate your Client ID and Client Secret by creating an app on the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/). Make sure to to include redirect urls (you can simpily put http://localhost if you aren't sure). 

### Next, Google Sheets/Drive API

Note: 
GSPREAD_KEYS in .env is now optional. If you have no interest in retrieving top artists, you can skip this section. Otherwise, follow the following tutorial to set up your GSPREAD_KEYS:
1. Sign into [Google Cloud Console](https://console.cloud.google.com/) & create your APP
2. Enable Google Sheets and Google Drive APIs
3. Head to API & Services -> Credentials ->  Create Credentials -> Service Account. Go through the prompts
4. Download JSON file upon completion of creating service account
5. Open Google Sheets and create a new file named 'Wrapped365'. Add tabs named 'short_term', 'medium_term', 'long_term', 'short_term Artists', 'medium_term Artists', and 'long_term Artists'
6. Share the Google Sheet Document with the email of your service account, make sure to give them editor permissions. The email can be found back on Google's Cloud Console Credentials or within the JSON file you downloaded. It would look something like: wrapped-test@wrapped-test943892.iam.gserviceaccount.com
