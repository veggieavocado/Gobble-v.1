#! /bin/bash

#### 샐러리 태스크 관리툴인 Flower 실행 ####

celery flower -A molecular --address=127.0.0.1 --port=5555
