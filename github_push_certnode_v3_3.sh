#!/bin/bash

REPO_DIR="certnode-v3.3-release"
REPO_NAME="certnode-v3.3-release"
GIT_URL="git@github.com:srbryant86/$REPO_NAME.git"

cd /mnt/data/$REPO_DIR

git init
git remote add origin $GIT_URL
git add .
git commit -m "Initial commit: CertNode v3.3 runtime capsule"
git branch -M main
git push -u origin main
