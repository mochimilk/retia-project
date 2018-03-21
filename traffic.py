# -*- coding: utf-8 -*-

# ■道路交通情報 ---------------------------
# Version1.1 by ハルピー(@hamatetsu_train)
# Version2.0 by @mochimilk_
# 　JARTICサイトのフォーマットが変わったので1.1をベースに改造
# Version2.0 for Python by @mochimilk_
# 　Python用に書き換えた

# 　url_jar：jsonファイルのURL（http://www.jartic.or.jp/_json/M_xxxx_301.json）
# 　       xxxxはエリアごとに割り振られた数字
# 　        1001　北海道地方
# 　        1002　東北地方
# 　        1003　関東地方
# 　        1004　北陸地方
# 　        1005　中部地方
# 　        1006　近畿地方
# 　        1007　中国地方
# 　        1008　四国地方
# 　        1009　九州地方
# 　        1010　沖縄地方
# 
# 　highway：抽出したい路線名（配列）
# 　mode：0=通行止めだけツイート、1=規制があればツイート
# 　doro_joho：json形式からdict型となった生データ
# 　trafic_list：抽出した路線の規制情報のリスト。
# 　toot_text：トゥート内容。これを戻り値にする
# 　------
# 　分解した["item"]の中身
# 　doro_list： 各路線の詳細（リスト内のリスト）
# 　item_list[11]： 路線
# 　item_list[3]： 起点
# 　item_list[4]： 終点またはその付近
# 　item_list[2]： 上下
# 　item_list[5]： 原因
# 　item_list[6]： 規制内容

import json
import datetime
import re
import urllib.request


def get_trafic(code_text, mode=0):
    print('○　道路情報取得中 powerd by @mochimilk_')
    trafic_list = []
    toot_text = ''
    code_dict = {'北海道':'1001', 
                 '東北':'1002', 
                 '関東':'1003', 
                 '北陸':'1004', 
                 '中部':'1005', 
                 '近畿':'1006', 
                 '中国':'1007', 
                 '四国':'1008', 
                 '九州':'1009', 
                 '沖縄':'1010'} 

    if code_text not in code_dict.keys():
        return toot_text

    code = code_dict[code_text]
    url_jar = 'http://www.jartic.or.jp/_json/M_' + code + '_301.json?dummy=0'
    print('url:', url_jar)

    #jsonファイルの中身を取得
    f = urllib.request.urlopen(url_jar)
    doro_joho = json.loads(f.read().decode('utf-8'))

    #更新日時取得と形式変換
    update = re.search(r".+月.+日([0-9]+)時([0-9]+)分", doro_joho['updtime']);
    up_time = update.group(1) + '時' + update.group(2) + '分'
    print("更新時刻:", up_time, '/', code_text)

    #規制情報の取得
    for item_list in doro_joho['item']:
        item_list[6] = re.sub(r"第１走行規制|追越車線規制|登坂車線規制", "車線規制", item_list[6])

        if item_list[6] == '規制なし':
            print(item_list[11] + ':', item_list[6])

        elif mode == 0 and item_list[6] == '通行止': #mode=0：通行止めのみ
            if item_list[3] == '': #起点が空欄
                tx = '・' + item_list[4] + '(' + item_list[2] + ')で' + \
                                 item_list[5] + 'のため' + item_list[6]
                trafic_list.append(tx)
            else: #起点がある
                tx = '・' + item_list[3] + '→' + item_list[4] + \
                                 '(' + item_list[2] + ')で' + \
                                 item_list[5] + 'のため' + item_list[6]
                trafic_list.append(tx)

        elif mode == 1: #mode=1：規制があれば
            if item_list[3] == '': #起点が空欄
                tx = '・' + item_list[4] + '(' + item_list[2] + ')で' + \
                                 item_list[5] + 'のため' + item_list[6]
                trafic_list.append(tx)
            else: #起点がある
                tx = '・' + item_list[3] + '→' + item_list[4] + \
                                 '(' + item_list[2] + ')で' + \
                                 item_list[5] + 'のため' + item_list[6]
                trafic_list.append(tx)

    #print(trafic_list)

    if trafic_list: #規制があればトゥート内容を作る
        toot_header = '【交通情報：' + code_text + '地方' + '(' + up_time + ')】\n'
        toot_text = '\n'.join(trafic_list)
        toot_text = toot_header + toot_text
    #print(toot_text)
    return toot_text


#直接実行すると以下が実行される（モジュールとして読み込んだ場合は実行されない）
if __name__ == '__main__': 
    get_trafic('関東', 1)
    pass
