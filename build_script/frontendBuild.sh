#!/bin/sh

cd /var/www/html/website2018/

## 1. build 
echo "[Pyladies] build web..."
cd frontend_react && yarn run build && cd ..

## 2. clean
echo "[Pyladies] clean..."
if [ -d ./frontend/eventlist/static ]
then
    rm -rf ./frontend/eventlist/static/*
else
    mkdir ./frontend/eventlist/static
fi

## 3. move
echo "[Pyladies] move..."
mv ./frontend_react/build/static/* ./frontend/eventlist/static/
mv ./frontend/eventlist/static/css/main.*.chunk.css ./frontend/eventlist/static/css/main.css
mv ./frontend/eventlist/static/js/1.*.chunk.js ./frontend/eventlist/static/js/chunk.js
mv ./frontend/eventlist/static/js/main.*.chunk.js ./frontend/eventlist/static/js/main.chunk.js
