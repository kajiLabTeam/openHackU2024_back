from flask import Flask, request, render_template, jsonify
from flask_cors import CORS
import json
from modules import database

app = Flask(__name__)
CORS(app)
app.config["JSON_AS_ASCII"] = False

@app.route('/')
def index():
    return render_template("index.html")

#アカウント連携ページ
# 受け取ったjsonデータからプレイリストを取得
# データベース登録関数へデータを渡す
@app.route('/api/account/align', methods=['POST'])
def account_align():
    data = request.get_json()
    
    #playlist = data()"playlist1"
    playlist = data["spotify_data"]["playlist1"]
    # song = data["spotify_data"]["playlist1"]["song"]
    # artist = data["spotify_data"]["playlist1"]["artist"]
    # songArtist = [song,artist]



    spotify_data = [["夜に溺れる","YOASOBI"],["Click","ME:I"]]
    display_name = data.get("display_name")
    user_id = data.get("user_id")
    print(spotify_data,display_name,user_id)
    print("-----------------------------------------------------")
    print(playlist)

    return database.regist_data(spotify_data,display_name,user_id)

#合言葉を打ってグループを作成・参加確認
@app.route('/api/room/access', methods=['POST'])
def room_access():
    print("room_access")
    with open('./json/room_get.json','r', encoding="utf-8") as f:
        user_datas = json.load(f)
    data = request.get_json()

    passphrase=data.get("pass")
    display_name=data.get("display_name")
    user_id=data.get("user_id")

    print(passphrase,display_name,user_id)
    print("---------------------------------")
    return database.get_member(passphrase,display_name,user_id)

#グループへ参加
@app.route('/api/room/join', methods=['POST'])
def room_join():

    data = request.get_json()
    passphrase=data.get("pass")
    display_name=data.get("display_name")
    user_id=data.get("user_id")

    print(passphrase,display_name,user_id)

    return database.join_group(passphrase,display_name,user_id)

#共通していた楽曲の表示
@app.route('/api/room/get', methods=['POST'])
def room_get():
    data = json.loads(request.data.decode('utf-8'))["request"]#デコード
    passphrase=data["pass"]
    print(passphrase)
    return database.get_group(passphrase)

if __name__ == "__main__":
    # debugモードが不要の場合は、debug=Trueを消してください
    app.run(debug=True, port=8888, host='0.0.0.0')