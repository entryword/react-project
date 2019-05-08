### 專案架構
* (後端) website2018/pyladies
    * app/ : 主要開發目錄
        * api_1_0/ : v1.0 RESTful API
        * cms/ : cms 的 RESTful API
        * managers/ : 提供資料給 API 來達成各項功能
        * schemas/ : 定義 JSON schema 給 API 或 managers 使用
        * sqldb/ : 定義 DB 結構、提供 managers 操作 DB 後的資料
        * \__init__.py : 指定 server 要使用的 API 以及 error handler
        * constant.py : 共用常數
        * exceptions.py : error code 的定義檔
        * utils.py : 共用類別、函式
    * migrations/ : DB 結構更動記錄
    * tests/ : 所有 unit test files
    * config.py : 設定檔，含開發/測試/正式環境的設定
    * manage.py : 可透過此檔案來啟動 server、跑 unit test、更改 DB 結構等
    * requirements.txt : 所有用到的 python package

### 建立專案
```
git clone https://soniawaka@bitbucket.org/pyladies-tw/website2018.git
cd ./website2018
docker-compose build
docker-compose up -d
docker-compose exec app bash
python manage.py db upgrade
```

### 測試是否成功
1. localhost:5566 (能看到 phpMyAdmin 的畫面)
2. localhost:55688/v1.0/api/definitions (確認 flask 服務運作正常)
3. localhost:5555/v1.0/api/definitions (確認 nginx 服務運作正常)

### Local DB 操作
除了使用phpMyAdmin，也可使用MySQL Workbench或其他支援MariaDB的GUI。
設定連線方式如下：
![MySQL Workbench](/img/mysql_workbench.jpg)

### Docker 指令
```
# Build Docker images
docker-compose build
# 啟動 container
docker-compose up -d
# 查看目前啟動中的 container
docker ps
# 進入 app container
docker-compose exec app bash
# 關閉 container
docker-compose down
```

### DB Migration
```
# 進入 app container
docker-compose exec app bash
# 產生 migration file
python manage.py db migrate
# upgrade DB
python manage.py db upgrade
# downgrade DB
python manage.py db downgrade
```

### Pylint
```
docker-compose exec app bash
cd ..
pylint -rn --rcfile .pylintrc ./pyladies/
```

### Unit Test
```
docker-compose exec app bash
# 所有 Unit Test File
python manage.py test
# 指定 Unit Test File
pytest ./tests/{file}
```

### 參考文件
* [docker-readme.md](https://bitbucket.org/pyladies-tw/website2018/src/dev/docker-readme.md)
* [API 文件](https://docs.google.com/document/d/1qCN153gmU7bjnoKshdwh9ZsE11Cd4TX5Ob8e-p1z1Vw/edit)
* [籽籽的開發環境文章](https://medium.com/ichitsai/docker-note-pyladies-tw-%E5%AE%98%E6%96%B9%E7%B6%B2%E7%AB%99%E9%96%8B%E7%99%BC%E7%92%B0%E5%A2%83%E8%A3%BD%E4%BD%9C-%E9%96%8B%E7%99%BC%E7%AD%86%E8%A8%98-6cb795d35c8e?fbclid=IwAR1oQ7ccgiQtSivGrevEf6PpWao8FdM5Dh3kacdhuoK5kStazAad5O-we-0)
* [毛毛提供的官網組文件](https://www.facebook.com/groups/1910063375747037/files/)
