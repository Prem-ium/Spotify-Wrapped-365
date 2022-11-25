# Spotify Wrapped 365 🎶

Generate a playlist composed of your top played tracks on Spotify over the course of a month, 6 months, and the all-time Top Tracks of your account! 
![image](https://user-images.githubusercontent.com/80719066/202199720-a1203f3a-7d8b-441c-bc91-911490a073ab.png)

## Features

- Generate Top Played Tracks & Artists
- Automatically update any existing Top Tracks playlist
- Apprise Alerts/Notifications every update (Optional)
- Google Sheets Automation (Optional)
- [Replit](https://replit.com/) support (Running program online 24/7 for free!)

## Environment Variables
To run this project, you will need to add the following environment variables to your .env file (see .env.example for a reference):
##### Required .env:
`CLIENT_ID`: [Found on Spotify Developer Dashboard](https://developer.spotify.com/dashboard/)

`SECRET_CLIENT_ID`: [Found on Spotify Developer Dashboard](https://developer.spotify.com/dashboard/)

`REDIRECT_URL`: The Redirect URL you added when creating the App on Spotify's Developer Dashboard. Check .env.example for reference.

`USERNAME`: Your Spotify account username [can be found in Spotify account settings.](https://www.spotify.com/us/account/overview/?utm_source=spotify&utm_medium=menu&utm_campaign=your_account))

##### Optional .env:
`MINUTES`: Number of minutes the program should wait before updating Top Tracks playlist. Defaults to 360 minutes (or 6 hours).

`KEEP_ALIVE`: Whether to run the flask server or not to keep program from sleeping on replit. Defaults to False.

`APPRISE_ALERTS`:  Full list of services and their URLs available here: [found here on Apprise wiki](https://github.com/caronc/apprise/wiki).

`GSPREAD_KEYS`: Your Google Service Account JSON contents obtained via OAuth 2.0 Client ID in Credentials of Google Cloud API.


## Setup
#### Spotify Developer Credentials (Required)
1. Head over to [Spotify Developer's Dashboard](https://developer.spotify.com/dashboard/). Login or create an account using your Spotify. 
2. Create a new Application. Name it anything you want to, add any description, and agree to TOS.
3. Click on 'Edit Settings' and add redirect URL you've set in your .env file & save.
4. Click 'Show Client Secret'
5. Copy/paste Client ID into `CLIENT_ID` and Secret Client ID into `SECRET_CLIENT_ID` within your .env file.

#### Replit (Optional, Recommended)
1. Login/Create a [Replit](https://replit.com/) account and create a new Python repl.
2. Setup .env within Replit's Secret tab (set `KEEP_ALIVE` to True) & go through [Installation](#installation). Optionally, move all files out of folder for ease of navigation, replace empty/old main.py.
3. Run the program and copy URL in the Flask webview. It should be something similar to:
`https://{Name of Repl}.{Repl username}.repl.co/` 
4. Create an account on [Uptime Robot](https://uptimerobot.com/), Click 'Add New Monitor',HTTP monitor type, name the monitor anything you'd like, paste your copied link into URL, set interval to 5 minutes, timeout to 30 seconds, and create the monitor.
5. Rerun the repl program. The repl should stay on 24/7! Your playlist will continue to be updated at no computer resource cost to you!

#### Google Sheets/GSpread (Optional)
1. Sign into [Google Cloud Console](https://console.cloud.google.com/), create your APP,Enable Google Sheets and Google Drive APIs.
3. Head to API & Services -> Credentials ->  Create Credentials -> Service Account. Go through the prompts & download the JSON file afterwards.
5. Open Google Sheets and create a new file named 'Wrapped365'. Add tabs named 'short_term', 'medium_term', 'long_term', 'short_term Artists', 'medium_term Artists', and 'long_term Artists'
6. Share the Google Sheet Document with the email of your service account, give editor permissions. The email can be found back on Google's Cloud Console Credentials or within the JSON file you downloaded. It would look something like: wrapped-test@wrapped-test943892.iam.gserviceaccount.com

## Installation
This script can be used locally or using Docker.
### Python
Clone the repository & Install dependencies
```bash
  git clone https://github.com/Prem-ium/Spotify-Wrapped-365.git
  cd Spotify-Wrapped365
  pip install -r requirements.txt
```
Finally, you're ready to run the script!
```bash
  python main.py
```
### Docker
1. Run script locally with Python & generate cache file.
2. Download and install Docker on your system
3. Configure your `.env` file (See below and example for options)
4. 
   To build the image, cd into the repository and run:
   ```sh
   docker build -t spotify-wrapped .
   ```
   Then start the bot with:
   ```sh
   docker run -it --env-file ./.env --restart unless-stopped --name spotify-wrapped spotify-wrapped
   ```


5. Let the bot log in and begin working. DO NOT PRESS `CTRL-c`. This will kill the container and the bot. To exit the logs view, press `CTRL-p` then `CTRL-q`. This will exit the logs view but let the bot keep running.

