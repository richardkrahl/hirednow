#!/bin/bash
# Push HiredNow to GitHub

cd ~/.openclaw/workspace/projects/job-hunter

echo "Initializing Git repo..."
git init

echo "Adding files..."
git add .

echo "Committing..."
git commit -m "Initial commit: HiredNow v1.0"

echo "Adding remote..."
git remote add origin https://github.com/richardkrahl/hirednow.git

echo "Pushing to GitHub..."
git branch -M main
git push -u origin main

echo "Done! Check: https://github.com/richardkrahl/hirednow"
