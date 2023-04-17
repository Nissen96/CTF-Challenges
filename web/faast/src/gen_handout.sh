#!/bin/bash

echo "Copying files to new folder..."
mkdir faast
cp ../Dockerfile faast
cp readme.local faast/README.md
cp -r app faast
rm -rf faast/app/node_modules

echo "Updating local Dockerfile..."
sed -i "s/199ab15c-fe1a-4ef1-9529-522588e1e505/REDACTED-PATH/" faast/Dockerfile
sed -i "s/src\///" faast/Dockerfile

echo "Updating .env..."
echo "SERVER_SECRET=\"REDACTED\"" > faast/app/.env

echo "Adding fake flag..."
echo "DDC{REDACTED}" > faast/flag.txt

echo "Zipping faast/ as faast.zip..."
zip -r faast faast
rm -rf faast
