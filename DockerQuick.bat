docker stop spotify-wrapped
docker rm spotify-wrapped
REM Replace the path below with the path to your youtube-analytics-bot folder
cd Desktop\Spotify-Wrapped-365
docker build -t spotify-wrapped .
docker run -itd --env-file ./.env --restart unless-stopped --name spotify-wrapped spotify-wrapped
REM WARNING: This will remove all dangling images. If you have other images that you want to keep, do not run this command. Otherwise, run this command to clean up your old docker images.
REM docker image prune -f --filter "dangling=true"
