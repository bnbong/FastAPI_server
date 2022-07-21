docker stop fastapi-server-container
docker rm fastapi-server-container
docker rmi fastapi-server-app
docker build -t fastapi-server-app .
docker run --hostname="0.0.0.0" -d --name fastapi-server-container -p 8000:8000 fastapi-server-app
docker ps -a