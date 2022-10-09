#!/bin/bash

echo "git 업데이트"

git add .
git commit -m "동시접속에 문제가 있어서 gunicorn worker=12으로 변경"
git push origin main
