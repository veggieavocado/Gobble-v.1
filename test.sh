#! /bin/bash

#### 데이터 분석 엔진 Molecular 서버 도커로 pytest 실행 ####

docker rm -f $(docker ps -a -q)

docker-compose up -d --build

docker exec -it molecular-django pytest -v
