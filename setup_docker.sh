docker stop mafia
docker rm mafia
docker image rm mafia:latest
docker build . -t mafia
docker run -d --restart always --name mafia mafia
