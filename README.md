<p align="right"><a href="https://developer.spotify.com/dashboard"><img src="https://img.shields.io/badge/Spotify-1ED760?style=for-the-badge&logo=spotify&logoColor=white"/></a></p>
<h1 align="center"> 🎧 Spotify Wrapped 365 🎶 </h1>

<p align="center">Generate your Spotify <i>Top Tracks</i> in a Playlist, <i>Top Played Artists, & More</i>!</p>

![image](https://user-images.githubusercontent.com/80719066/202199720-a1203f3a-7d8b-441c-bc91-911490a073ab.png)

## Features
- Generate Top Tracks Playlist that auto-updates!
- Generate List of Top Played Artists
- Generate Reccomended Tracks Playlists (Optional)
- Optional Apprise Alerts/Notifications
- Docker Support
- Google Sheets Compatiable. 
- Keep_Alive Flask Server

### Issues
- GitHub Actions Support (Currently Not Working-> ISSUE: Spotipy Access token is able to be refreshed, but cannot be updated to GitHub Secrets for next run)

## Environment Variables
To run this project, you will need to add the following environment variables to your .env file (see .env.example for a reference):
##### Required .env:
| Environment Variable   | Description                                                                                                            | Default Value |
|------------------------|------------------------------------------------------------------------------------------------------------------------|---------------|
| `CLIENT_ID`            | Found on Spotify Developer Dashboard. [More Info](https://developer.spotify.com/dashboard/)                           | -             |
| `SECRET_CLIENT_ID`     | Found on Spotify Developer Dashboard. [More Info](https://developer.spotify.com/dashboard/)                           | -             |
| `REDIRECT_URL`         | The Redirect URL you added when creating the App on Spotify's Developer Dashboard. Check .env.example for reference. | -             |
| `USERNAME`             | Your Spotify account username (can be found in Spotify account settings.)                                             | -             |

##### Optional .env:
| Environment Variable   | Description                                                                                                            | Default Value                      |
|------------------------|------------------------------------------------------------------------------------------------------------------------|------------------------------------|
| `MINUTES`              | Number of minutes the program should wait before updating Top Tracks playlist.                                       | 360 minutes (or 6 hours)           |
| `PUBLIC_PLAYLIST`      | Boolean value indicating whether to create a public playlist.                                                         | True                               |
| `RECOMMENDATIONS`      | Boolean value indicating whether to generate recommendations (tracks playlist and artists recommendations).          | False                              |
| `KEEP_ALIVE`           | Whether to run the flask server or not to keep the program from sleeping on replit.                                  | False                              |
| `APPRISE_ALERTS`       | Full list of services and their URLs available here: [Apprise Wiki](https://github.com/caronc/apprise/wiki)          | -                                  |
| `TZ`                   | Your desired Time-Zone. Should be formatted from the IANA TZ Database.                                               | `America/New York`                 |
| `AUTH_CACHE`         | Cache JSON String retrieved from initial setup, for GitHub Actions.      | -                                  |
| `GSPREAD_KEYS`         | Your Google Service Account JSON contents obtained via OAuth 2.0 Client ID in Credentials of Google Cloud API.       | -                                  |


## Setup
#### Spotify Developer Credentials (Required)
1. Head over to [Spotify Developer's Dashboard](https://developer.spotify.com/dashboard/). Login or create an account using your Spotify. 
2. Create a new Application. Name it anything you want to, add any description, and agree to TOS.
3. Click on 'Edit Settings' and add redirect URL you've set in your .env file & save. Examples:
<img src="https://user-images.githubusercontent.com/80719066/202246758-b0472b8c-b03f-44fc-8e1a-c161c7746a93.png" style="width: 50%;"></img>
4. Click 'Show Client Secret'
5. Copy/paste Client ID into `CLIENT_ID` and Secret Client ID into `SECRET_CLIENT_ID` within your .env file.
<img src="https://user-images.githubusercontent.com/80719066/202246004-f7307806-69ec-4489-975b-beb71e6637b3.png" style="width: 50%;"></img>

### GitHub Actions
1. Fork the repository and start configuring your `.env` by navigating to your Forked Repository Settings: `Settings -> Security -> Secrets & Variables -> Actions -> New Repository Secret`.
3. Enable `GITHUB_ACTIONS` by assigning the value of `True` within your `.env`.
4. Run `main.py`, click the URL in the console, and approve the ticket for your account.
5. Copy the URL after approving permissions, paste it into the console, and hit enter.
6. Copy the cache JSON contents and assign it to the `AUTH_CACHE` variable within GitHub Secrets.
7. Adjust the cron job if necessary.

### Google Sheets/GSpread (Optional)
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
  cd Spotify-Wrapped-365
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

## License
This repository is using the [MIT](https://choosealicense.com/licenses/mit/) license.

## 🎧 What I've been listening to

[<img src="covers/short_term.jpg" style="width:30%;height:30%;">](https://open.spotify.com/playlist/41FgHkzQ2wf4v8MtoITL77?si=c4c016d8bdbf411a)   [<img src="covers/medium_term.jpg" style="width:30%;height:30%;">](https://open.spotify.com/playlist/657cuGMmf1CnJEeMhfwgnK?si=154abf33ddd64a20)  [<img src="covers/long_term.jpg" style="width:30%;height:30%;">](https://open.spotify.com/playlist/42TRuidms91LuMajAIu5xI?si=8a22e2ccb6b9445f)

## Donations
I've been working on this project for a few months now, and I'm really happy with how it's turned out. It's also been a helpful tool for users to earn some extra money with Bing Rewards. I'm currently working on adding new features to the script and working on other similar programs to generate passive income. I'm also working on making the script more user-friendly and accessible to a wider audience.
If you appreciate my work and would like to show your support, there are two convenient ways to make a donation:

1. **GitHub Sponsors**
   - [Donate via GitHub Sponsors](https://github.com/sponsors/Prem-ium)
   - This is the preferred donation method as you can place donations with no transaction fees & possibily receive perks for your donation.
   - [![GitHub Sponsor](https://img.shields.io/badge/sponsor-30363D?style=for-the-badge&logo=GitHub-Sponsors&logoColor=#EA4AAA)](https://github.com/sponsors/Prem-ium)

2. **Buy Me A Coffee**
   - [Donate via Buy Me A Coffee](https://www.buymeacoffee.com/prem.ium)
   - [![Buy Me A Coffee](https://img.shields.io/badge/Buy%20Me%20a%20Coffee-ffdd00?style=for-the-badge&logo=buy-me-a-coffee&logoColor=black)](https://www.buymeacoffee.com/prem.ium)

Your generous donations will go a long way in helping me cover the expenses associated with developing new features and promoting the project to a wider audience. I extend my heartfelt gratitude to all those who have already contributed. Thank you for your support!