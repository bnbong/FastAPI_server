docker stop fastapi_server
docker rm fastapi_server
docker run --hostname="serverside-testing.bnbongcodeserver.tk" -d --name fastapi_server -p 8000:8000 bnbong/fastapi_server:myserverimage
docker ps -a