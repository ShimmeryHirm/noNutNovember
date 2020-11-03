docker stop signal-bot
docker rm signal-bot
docker image rm signal-bot:latest
docker build . -t signal-bot
docker run -d --restart always --name signal-bot signal-bo