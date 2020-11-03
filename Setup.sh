docker stop nofap
docker rm nofap
docker image rm nofap:latest
docker build .-t nofap
docker run -d --restart always --name nofap nofap