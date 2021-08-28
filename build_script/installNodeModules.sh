#!/bin/sh

cd /var/www/html/website2018/

cd frontend_react && yarn install --frozen-lockfile && cd ..

cd frontend_cms && yarn install --frozen-lockfile && cd ..