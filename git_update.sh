#!/bin/bash

echo "git 업데이트"

git add .
git commit -m "gunicorn과 nginx timeout 문제 해결하고 배포"
git push origin main
