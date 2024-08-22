from flask import Flask, request, render_template, jsonify
from flask_cors import CORS
from modules import database
import json

app = Flask(__name__)
CORS(app)
app.config["JSON_AS_ASCII"] = False

#アカウント連携ページ
# 受け取ったjsonデータからプレイリストを取得
# データベース登録関数へデータを渡す
@app.route('/api/account/align', methods=['POST'])
def account_align():
    data = request.get_json()
    # キーを取得
    keys = data["spotify_data"].keys()
    playlist_count = len(data["spotify_data"])

    songAndArtist=[]

    for i in keys:
        playlists = data["spotify_data"][i]
        for playlist in playlists:
            song=playlist["song"]
            artist=playlist["artist"]

            songAndArtist.append([song,artist])

    spotify_data = songAndArtist
    display_name = data.get("display_name")
    user_id = data.get("user_id")

    print(songAndArtist)
    print(spotify_data,display_name,user_id)
    return database.regist_data(spotify_data,display_name,user_id)

#合言葉を打ってグループを作成・参加確認
@app.route('/api/room/access', methods=['POST'])
def room_access():
    data = request.get_json()
    passphrase=data.get("pass")
    display_name=data.get("display_name")
    user_id=data.get("user_id")

    print(passphrase,display_name,user_id)
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
    data = request.get_json()
    passphrase=data.get("pass")

    print(passphrase)
    return database.get_group(passphrase)

if __name__ == "__main__":
    # debugモードが不要の場合は、debug=Trueを消してください
    app.run(debug=True, port=8888, host='0.0.0.0')