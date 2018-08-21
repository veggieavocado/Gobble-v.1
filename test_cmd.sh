#! /bin/bash

### Travis CI에서 사용할 용도 ###

docker exec -it molecular-django python -m pytest -n 3 --cov-config .coveragerc --cov=. -v
