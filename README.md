# openHackU2024_BACKEND

## 概要
[openHackU2024_front](https://github.com/kajiLabTeam/openHackU2024_front)からのリクエストを処理するAPIサーバー。  
POSTで送られてきた情報をデータベースへ登録し、ユーザー・グループ・曲データの管理を行う。

## 環境構築
### データベースの構築
MySQLのプロンプト上で"init.sql"を実行する。
<pre>
mysql> source ./db_init/init.sql;
</pre>
以下のデータベースとテーブルが自動で作成される。
<pre>
+---------------------+
| Tables_in_tomato_db |
+---------------------+
| group_tb            |
| user_tb             |
+---------------------+
</pre>
### pythonライブラリのインストール
<pre>
pip install Flask
pip install flask-cors
pip install mysql-connector-python
</pre>

## 実行方法
"main.py"を実行するとAPIサーバーが立ち上がる
<pre>
python3 main.py
</pre>

## 各プログラム
### main.py
#### Flaskを利用したAPIサーバー。  
- /api/account/align
    - アカウント連携ページ  
    Spotifyから取得した楽曲データ,表示名,UUIDを受け取り、データベースへ登録する。
- /api/room/access
    - グループへの参加確認・グループの作成  
    合言葉,表示名,UUIDを受け取り、一致する合言葉のグループに所属するユーザーを取得する。  
    もし、グループが存在しなかった場合、自動的にグループが作成される。
- /api/room/get
    - グループへの参加  
    合言葉,表示名,UUIDを受け取り、一致する合言葉のグループにユーザーを追加する。
- /api/account/align
    - グループデータの取得  
    合言葉,表示名,UUIDを受け取り、一致する合言葉のグループに所属するユーザー,楽曲データを取得する。
### /modules/database.py
#### "main.py"から呼び出されるデータベース操作用プログラム。  
- connect_database()  
データベースへ接続するための関数
- regist_data(spotify_data:list, display_name:str, user_id:str)  
データベースへ楽曲データ,表示名,UUIDを登録する。
- get_member(passphrase:str, display_name:str, user_id:str)  
データベースから合言葉のグループに所属するユーザーを取得する。  
もし、グループが存在しなかった場合、自動的にグループが作成される。
- join_group(passphrase:str, display_name:str, user_id:str)  
ユーザーのグループIDを合言葉のグループに変更する。
- get_group(passphrase:str)  
合言葉のグループに所属するユーザー,楽曲データを取得する。  
取得したユーザーごとの楽曲データを合計し、被っていた数を算出する。
- get_rawdata(table:str="user_tb", where:str="", sql:str="")  
データベースから生データを取得する。  
何も引数を渡さなかった場合、"user_tb"のデータを取得する。  
`table`に欲しいテーブルデータを指定することで、そのテーブルデータを取得することができる。  
`where`に`"name='hoge'"`のような条件を指定することもできる。  
`sql`に`"SELECT * FROM user_tb WHERE id=3"`のように直接SQLのクエリ文を指定することもできる。これを使用した場合、`sql`が最優先される。