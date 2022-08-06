docker stop fastapi-server-container
docker rm fastapi-server-container
docker build -t bnbong/fastapi_server:latest .
docker run --hostname="serverside-testing.bnbong.tk" -d --name fastapi-server-container -p 8000:8000 bnbong/fastapi_server:latest
docker ps -a