#!/bin/sh

cd /var/www/html/website2018/

## 1. build 
echo "[Pyladies] build cms..."
cd frontend_cms && yarn run build && cd ..

## 2. clean
echo "[Pyladies] clean..."
if [ -d ./frontend/cms ]
then
    rm -rf ./frontend/cms/*
else
    mkdir ./frontend/cms
fi

## 3. move
echo "[Pyladies] move..."
cp frontend_cms/dist/index.html frontend/cms
cp frontend_cms/login.html frontend/cms
cp -r frontend_cms/dist/static frontend/cms
