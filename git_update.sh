#!/bin/bash

echo "git 업데이트"

git add .
git commit -m "ARM 서버로 변경, gunicorn worker=6으로, 방화벽 설정 변경"
git push origin main
