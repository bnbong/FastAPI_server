# FastAPI_server
deepened fast api practice for learning purpose

# TODO
 - 

# Docker setting
 > docker ps -a : check container, etc...
 > docker run --hostname=serverside-testing.bnbongcodeserver.tk -p 8000:8000 <image_name>: run at live server
 > docker container stop <container_name>
 > docker container restart <container_name>
 > dockr container rm <container_name>

# make docker image & push
 > docker stop <container>
 > docker build -t <tag> . / docker commit <container> <image_name>
 > docker push <remote_container>
 ex) docker build -t bnbong/fastapi_server:build_1.0
 ex) docker push bnbong/fastapi_server:build_1.0

# delete docker image
 > docker rmi <image_name>

# check container running log
 > docker logs <container_name>

# run docker-compose
 > docker-compose up -d 

# check docker volume files
 > docker volume ls

# alembic migration
 - make migration with no autogenerate
 > alembic revision -m "<migration_name>"

 - make migration automatically
 > alembic  revision  --autogenerate  -m  "autogenerate  first  migration"

 - upgrade db
 > alembic upgrade head

# 참고 웹페이지
 - routing, etc..
 > https://velog.io/@ddhyun93/FastAPI-SQL-%EC%97%B0%EA%B2%B0%EB%B6%80%ED%84%B0-Testing%EA%B9%8C%EC%A7%80