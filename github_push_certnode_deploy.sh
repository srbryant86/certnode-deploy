#!/bin/bash

REPO_DIR="certnode-deploy"
REPO_NAME="certnode-deploy"
GIT_URL="git@github.com:srbryant86/$REPO_NAME.git"

cd /mnt/data/$REPO_DIR

git init
git remote add origin $GIT_URL
git add .
git commit -m "Deploy CertNode v3.3 backend to certnode-deploy"
git branch -M main
git push -u origin main
