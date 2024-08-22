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
- Flaskを利用したAPIサーバー。  
- POSTで送られてきたデータをデータベースへ登録したり、楽曲のデータを収集・分析を行い、JSONデータにしてレスポンスを返す。
### database.py
- "main.py"から呼び出されるデータベース操作用プログラム。  
- MySQLデータベースへの接続を行い、実際にデータの入力、更新、取得などを行い"main.py"へデータを渡す。
