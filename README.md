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

* (前端) 
    * 所有外部讀取的程式碼放在 `website2018/frontend`，目前除下面兩點提到的頁面，都是直接做 html / js / css 開發，沒有 preprocessor。開發過程可以參考最下方參考資料的文章記錄。

    * 官網 活動列表 react app 在 `website2018/frontend_react`，建置好的 code 搬到 `website2018/frontend/eventlist`。詳情參考下面細節。
    
    * 官網 CMS 是 VueJS app 在 `website2018/frontend_cms`，建置好的 code 搬到 `website2018/frontend/cms`。詳情參考下面細節。


### 建置專案
* 下載程式碼
```
git clone https://github.com/PyLadiesTaiwan/website2018.git
```

* 建置docker image
```
cd ./website2018
docker-compose build
```
* 啟動container
```
docker-compose up -d
```
* upgrade schema
```
docker-compose exec app bash

# inside app container
python manage.py db upgrade
exit
```
* 塞假資料進database
```
docker-compose exec mariadb bash

# inside mariadb container
bash /sql_init/init.sh
exit
```
* 編譯前端頁面
```
# Install node modules (execute when yarn.lock is updated)
docker-compose exec -T node build_script/installNodeModules.sh

# build CMS (frontend_cms) 
docker-compose exec -T node build_script/cmsBuild.sh

# build APP (frontend_react)
docker-compose exec -T node build_script/frontendBuild.sh
```

### 測試是否成功
1. localhost:5566 (能看到 phpMyAdmin 的畫面，帳號: `root`，密碼: `12345678`)
2. localhost:55688/v1.0/api/definitions (確認 flask 服務運作正常)
3. localhost:5555/v1.0/api/definitions (確認 nginx 服務運作正常)

4. localhost:5555/ (前台畫面)
5. localhost:5555/cms (後台畫面，帳號: `pyladies`，密碼: `12345678`)


### 前端專案開發與建置

#### frontend_react - 開發時開啟此資料夾

    - 第一次進入
    ```
    npm i
    ```

    - 專案開發

    ```
    npm start
    ```

    瀏覽器開啟 http://localhost:3000

    - 專案建置

    ``` 
    npm run build
    ```

    - 建置搬遷程式碼：

        > 替換 /static 資料夾的資料 並重新命名。 index.html 已經固定，不需更動。

        - 移除 /frontend/eventlist/static/* 原本內容
        - 將 /frontend-react/build/static/* 搬到 /frontend/eventlist/static/*
        - 將 main.xxxxxxx.chunk.css 改成 main.css
        - 將 1.xxxxxxxx.chunk.js 改成 chunk.js
        - 將 main.xxxxxxx.chunk.js 改成 main.chunk.js

#### frontend_cms - 開發時開啟此資料夾   
 - 第一次進入
    ```
    npm i
    ```

 - 專案開發

    ```
    npm run dev
    ```

    瀏覽器開啟 http://localhost:8080

    目前 CMS 需要登入才能拉到 API 資料，先到 http://localhost:5555/cms/login.html 登入成功之後
    再回到 開發網址看到開發結果

- 專案建置

    ``` 
    npm run build
    ```
    - 遷移程式碼
    > 已經將 dev 和 prod 環境的不同處都以 Vue 設定 或 script 處個。
    
        - 將 website2018/frontend_cms/dist 下的 index.html 和 /static 資料夾內容 搬到 website2018/frontend/cms 下
        - login.html 是獨立頁面，如果沒有修改不需要動

#### 前端畫面

這裡所顯示的畫面是在 `website2018/frontend` 資料夾裡的 code 的結果，前端開發期間請用上述的開發 port。

1. http://localhost:5555 首頁
2. http://localhost:5555/eventlist/index.html 官網活動列表
3. http://localhost:5555/cms/ 後台 CMS
3. http://localhost:5555/cms/login.html 後台 CMS login 畫面

### Local DB 操作
除了使用phpMyAdmin，也可使用MySQL Workbench或其他支援MariaDB的GUI。
設定連線方式如下：
![](img/mysql_workbench.png)

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
* [籽籽的測試 model script](https://hackmd.io/tW3QdYK4TISrJUETLmJ-Hg)

前端開發紀錄文章

* [PyLadies Taiwan 官網的前端開發](https://medium.com/@peicheng_88746/pyladies-taiwan-%E5%AE%98%E7%B6%B2%E7%9A%84%E5%89%8D%E7%AB%AF%E9%96%8B%E7%99%BC-80cd9eb419d7)
* [PyLadies Taiwan 官網的前端開發 Part 2 - event list](https://medium.com/@peicheng_88746/pyladies-taiwan-%E5%AE%98%E7%B6%B2%E7%9A%84%E5%89%8D%E7%AB%AF%E9%96%8B%E7%99%BC-part-2-5fbf1b66ca73)
* 還在整理中的草稿 [PyLadies Taiwan 官網的前端開發 Part 3- 使用 Vue 建置內容管理系統 (CMS)](https://medium.com/@peicheng_88746/pyladies-taiwan-%E5%AE%98%E7%B6%B2%E7%9A%84%E5%89%8D%E7%AB%AF%E9%96%8B%E7%99%BC-part-3-%E4%BD%BF%E7%94%A8-vue-%E5%BB%BA%E7%BD%AE%E5%85%A7%E5%AE%B9%E7%AE%A1%E7%90%86%E7%B3%BB%E7%B5%B1-cms-acc383eb40d6)
