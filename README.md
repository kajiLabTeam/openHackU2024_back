# openHackU2024_BACKEND

## 概要
まだかいてない

## 事前準備
### データベースの構築
MySQLのプロンプト上で"init_db.sql"を実行する。
<pre>
mysql> source ./db_init/init_db.sql;
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