#! /bin/bash

#### 데이터 분석 엔진 Molecular 서버 자동 배포 스크립트 ####

# install Docker on server
sudo apt-get update
sudo apt-get install docker.io
sudo curl -L https://github.com/docker/compose/releases/download/1.21.2/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

sudo ufw app list
sudo ufw allow OpenSSH
sudo ufw allow 3000
echo -e "y" | sudo ufw enable

### docker-compose 실행: 장고 + Nginx + Redis 실행 ###
docker-compose up -d --build
