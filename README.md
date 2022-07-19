# FastAPI_server
deepened fast api practice for learning purpose

# TODO
 - connection testing with PostgreSQL

# Docker setting
 > docker ps -a : check container, etc...
 > docker run --hostname=serverside-testing.bnbongcodeserver.tk -p 8000:8000 <image_name>: run at live server
 > docker container stop <container_name>
 > docker container restart <container_name>
 > dockr container rm <container_name>

# make docker image & push
 > docker stop <container>
 > docker commit <container> <image_name> / docker build -t <tag> .
 > docker push <remote_container>

# delete docker image
 > docker rmi <image_name>

# check container running log
 > docker logs <container_name>

# run docker-compose
 > docker-compose up -d 

# check docker volume files
 > docker volume ls