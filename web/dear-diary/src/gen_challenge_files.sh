#!/bin/bash

echo "Copying local Dockerfile and readme..."
mkdir deardiary
cp Dockerfile.local deardiary/Dockerfile
cp readme.local deardiary/README.md

echo "Copying backend..."
cp -r app deardiary
rm -rf deardiary/app/dist

echo "Copying frontend..."
cp -r frontend deardiary

echo "Building frontend..."
npm --prefix deardiary/frontend install
npm --prefix deardiary/frontend run build

echo "Adding frontend dist to app..."
mv deardiary/frontend/dist deardiary/app

echo "Removing frontend..."
rm -rf deardiary/frontend

echo "Redacting flag..."
sed -i "s/DDC{.*}/REDACTED/" deardiary/app/init_db.py

echo "Zipping deardiary/ as deardiary.zip"
zip -r deardiary deardiary
rm -rf deardiary