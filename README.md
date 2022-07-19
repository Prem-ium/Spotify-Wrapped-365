# Spotify Wrapped 365 

<p align="center"><img src="https://socialify.git.ci/sazncode/Spotify-Wrapped365/image?description=1&amp;descriptionEditable=Top%20Tracks%20%26%20Artists%20-%20Wrapped%20365%2FYear&amp;font=Inter&amp;language=1&amp;name=1&amp;owner=1&amp;pattern=Charlie%20Brown&amp;stargazers=1&amp;theme=Dark" alt="project-image"></p>
A python bot that utilizes the Spotipy Python library to retrieve a user's top tracks and artists. Then exports the information to Google Sheets AND automatically creates/updates top track playlists every (user specified) number of hours. 

## Installation

### Set First: Spotify Developer Account
Generate your Client ID and Client Secret by creating an app on the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/). Make sure to to include redirect urls (you can simpily put http://localhost if you aren't sure). 

### Next, Google Sheets/Drive API

Note: 
If your only interest is obtaining Top Tracks on your account, you may skip this step entirely and simpily comment out (using #) or deleting the gsheet lines of code.

1. Sign into [Google Cloud Console](https://console.cloud.google.com/) & create your APP
2. Enable Google Sheets and Google Drive APIs
3. Head to API & Services -> Credentials ->  Create Credentials -> Service Account. Go through the prompts
4. Download JSON file upon completion of creating service account
5. Open Google Sheets and create a new file named 'Wrapped365'. Add tabs named 'short_term', 'medium_term', 'long_term', 'short_term Artists', 'medium_term Artists', and 'long_term Artists'
6. Share the Google Sheet Document with the email of your service account, make sure to give them editor permissions. The email can be found back on Google's Cloud Console Credentials or within the JSON file you downloaded. It would look something like: wrapped-test@wrapped-test943892.iam.gserviceaccount.com

## DESCRIPTION FOR ENV VARIABLES
These are the necessary enviormental variables for the Wrapped to function properly. They must be added.
- CLIENT_ID: [Found on Spotify Developer Dashboard](https://developer.spotify.com/dashboard/)
- SECRET_CLIENT_ID: [Found on Spotify Developer Dashboard](https://developer.spotify.com/dashboard/)
- REDIRECT_URL: The Redirect URL you added when creating the App on Spotify's Developer Dashboard
- USERNAME: Your Spotify account username [can be found in Spotify account settings.]([https://developer.spotify.com/dashboard/](https://www.spotify.com/us/account/overview/?utm_source=spotify&utm_medium=menu&utm_campaign=your_account))
- MINUTES: How many minutes should the program wait until executing again? It is ideal to allow at least 6 hours (or 360 minutes).
- GSPREAD_KEYS: Your Google Service Account JSON contents obtained via OAuth 2.0 Client ID in Credentials of Google Cloud API,
- APPRISE_FOUND_ALERTS:  Full list of services and their URLs available here: [found here on Apprise wiki](https://github.com/caronc/apprise/wiki).
