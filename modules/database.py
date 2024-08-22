import mysql.connector, json

# MySQLServerに接続
def connect_database():
    conn = mysql.connector.connect(
        host="localhost",
        user="tomato",
        password="kaji2024",
        database="tomato_db"
    )
    # カーソルを取得
    cursor = conn.cursor()
    return conn, cursor

# データを登録
def regist_data(spotify_data, display_name, user_id):
    try:
        conn, cursor = connect_database()

        # SQL文
        sql = "INSERT INTO `user_tb` (`id`, `name`, `uuid`, `song`, `created_at`, `group_id`) VALUES (NULL, %s, %s, %s, NOW(), '0');"
        sql_data = (display_name, user_id, str(spotify_data))
        # SQL文を実行
        cursor.execute(sql, sql_data)
        conn.commit()

        # 接続を閉じる
        cursor.close()
        conn.close()

        return json.loads('{"status": "success"}')

    except Exception as e:
        return json.loads('{"status": "error", "error": "' + str(e) + '"}')

# グループに参加しているメンバーを取得
def get_member(passphrase, display_name, user_id):
    try:
        conn, cursor = connect_database()

        # SQL文 グループIDの取得
        sql = "SELECT id FROM `group_tb` WHERE `name`=%s;"
        sql_data = (passphrase, )
        # SQL文を実行
        cursor.execute(sql, sql_data)
        group_id = cursor.fetchall()

        # グループが存在しない場合
        if len(group_id) == 0:
            # SQL文 グループの作成
            sql = "INSERT INTO `group_tb` (`id`, `name`, `owner`, `created_at`) VALUES (NULL, %s, %s, NOW());"
            sql_data = (passphrase, user_id)
            # SQL文を実行
            cursor.execute(sql, sql_data)
            conn.commit()

            # SQL文 グループIDの取得
            sql = "SELECT id FROM `group_tb` WHERE `name`=%s;"
            sql_data = (passphrase, )
            # SQL文を実行
            cursor.execute(sql, sql_data)
            group_id = cursor.fetchall()[0][0]

            # SQL文 ユーザーのグループIDの更新
            sql = "UPDATE `user_tb` SET `group_id` = '%s' WHERE `user_tb`.`uuid` = %s;"
            sql_data = (group_id, user_id)
            # SQL文を実行
            cursor.execute(sql, sql_data)
            conn.commit()

            json_text = '{"status": "404", "display_names" : []}'
            return_message = json.loads(json_text)
        # グループが存在する場合
        else:
            group_id = group_id[0][0]

            # SQL文 グループに参加しているメンバーの取得
            sql = "SELECT * FROM `user_tb` WHERE `group_id`=%s;"
            sql_data = (group_id, )
            # SQL文を実行
            cursor.execute(sql, sql_data)
            joined_users = cursor.fetchall()
            # json形式に変換
            json_text = '{"status": "success", "display_names" : ['
            for joined_user in joined_users:
                json_text += '{"display_name" : "' + joined_user[1] + '", ' + '"user_id" : "' + joined_user[2] + '"},'
            json_text = json_text[:-1]
            json_text += ']}'

            return_message = json.loads(json_text)

        # 接続を閉じる
        cursor.close()
        conn.close()

        return return_message

    except Exception as e:
        return json.loads('{"status": "error", "error": "' + str(e) + '"}')

# グループへの参加
def join_group(passphrase, display_name, user_id):
    try:
        conn, cursor = connect_database()

        # SQL文 グループIDの取得
        sql = "SELECT id FROM `group_tb` WHERE `name`=%s;"
        sql_data = (passphrase, )
        # SQL文を実行
        cursor.execute(sql, sql_data)
        group_id = cursor.fetchall()

        # グループが存在しない場合エラーを返す
        if len(group_id) == 0: json.loads('{"status": "error", "error": "group not found"}')
        group_id = group_id[0][0]

        # SQL文 ユーザーのグループIDの更新
        sql = "UPDATE `user_tb` SET `group_id` = '%s' WHERE `user_tb`.`uuid` = %s;"
        sql_data = (group_id, user_id)
        # SQL文を実行
        cursor.execute(sql, sql_data)
        conn.commit()

        # 接続を閉じる
        cursor.close()
        conn.close()

        return json.loads('{"status": "success"}')

    except Exception as e:
        return json.loads('{"status": "error", "error": "' + str(e) + '"}')

# グループの情報を取得
def get_group(passphrase):
    try:
        conn, cursor = connect_database()

        # SQL文 グループIDの取得
        sql = "SELECT id FROM `group_tb` WHERE `name`=%s;"
        sql_data = (passphrase, )
        # SQL文を実行
        cursor.execute(sql, sql_data)
        group_id = cursor.fetchall()

        # グループが存在しない場合エラーを返す
        if len(group_id) == 0: return json.loads('{"status": "error", "error": "group not found"}')
        group_id = group_id[0][0]

        # SQL文 グループに参加しているメンバーの取得
        sql = "SELECT * FROM `user_tb` WHERE `group_id`=%s;"
        sql_data = (group_id, )
        # SQL文を実行
        cursor.execute(sql, sql_data)
        user_datas = cursor.fetchall()

        # 曲データの取得・合計
        song_datas = []
        song_overlaps = []
        for user_data in user_datas:
            for song_data in eval(user_data[3]):
                if song_data not in song_datas:
                    song_datas.append(song_data)
                    song_overlaps.append(1)
                else:
                    song_overlaps[song_datas.index(song_data)] += 1

        # 二つのリストの長さが同じでなかった場合エラーを返す
        if len(song_datas) != len(song_overlaps): return json.loads('{"status": "error", "error": "song data collect exception"}')

        # json形式に変換
        json_text = '{"status": "success", "display_names" : ['
        for joined_user in user_datas:
            json_text += '{"display_name" : "' + joined_user[1] + '", ' + '"user_id" : "' + joined_user[2] + '"},'
        json_text = json_text[:-1]
        json_text += '], "song_data" : ['
        for i in range(len(song_datas)):
            json_text += '{"song_title" : "' + song_datas[i][0] + '", "song_artist" : "' + song_datas[i][1] + '", "overlap" : "' + str(song_overlaps[i]) + '"},'
        json_text = json_text[:-1]
        json_text += ']}'

        # 接続を閉じる
        cursor.close()
        conn.close()

        return json.loads(json_text)

    except Exception as e:
        return json.loads('{"status": "error", "error": "' + str(e) + '"}')

#データベースから生データを取得
def get_rawdata(table="user_tb", where="", sql = ""):
    conn, cursor = connect_database()

    # SQL文
    if sql != "":
        pass
    elif where != "":
        sql = "SELECT * FROM `" + table + "` WHERE " + where + ";"
    else:
        sql = "SELECT * FROM `" + table + "`;"

    # SQL文を実行
    cursor.execute(sql)
    rawdata = cursor.fetchall()

    # 接続を閉じる
    cursor.close()
    conn.close()

    return rawdata

if __name__ == "__main__":
    pass
