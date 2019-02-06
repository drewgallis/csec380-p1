#!/bin/bash
docker container rm -f nginx_web
docker build -t nginx_web ./nginx
docker run -d -p 81:80 -l traefik.weight=10 --name nginx_web nginx_web:latest
