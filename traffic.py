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
# 　mode：0=通行止めだけトゥー、1=規制があればトゥー、2=通行止と「規制中」があればトゥー
# 　doro_joho：json形式からdict型となった生データ
# 　traffic_list：抽出した路線の規制情報のリスト。
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


def get_traffic(code_text, mode=0):
    print('○　道路情報取得中 powerd by @mochimilk_')
    traffic_list = []
    toot_header = ''
    toot_text = ''
    kisei = ''
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
        #toot_text = '★'
        #return toot_text
        return toot_header, toot_text

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
        #    print(item_list[11] + ':', item_list[6])
            pass

        #mode=0：通行止のみ
        elif mode == 0 and item_list[6] == '通行止': 
            if item_list[3] == '': #起点が空欄
                tx = item_list[11]  + '：' + item_list[4] + '(' + item_list[2] + ')で' + \
                                 item_list[5] + 'のため' + item_list[6]
                traffic_list.append(tx)
            else: #起点がある
                tx = item_list[11] + '：' + item_list[3] + '→' + item_list[4] + \
                                 '(' + item_list[2] + ')で' + \
                                 item_list[5] + 'のため' + item_list[6]
                traffic_list.append(tx)


        #mode=1：全種類の規制がある場合
        elif mode == 1: 
            if item_list[3] == '': #起点が空欄
                tx = item_list[11] + '：' + item_list[4] + '(' + item_list[2] + ')で' + \
                                 item_list[5] + 'のため' + item_list[6]
                traffic_list.append(tx)
            else: #起点がある
                tx = item_list[11] + '：' + item_list[3] + '→' + item_list[4] + \
                                 '(' + item_list[2] + ')で' + \
                                 item_list[5] + 'のため' + item_list[6]
                traffic_list.append(tx)

        #mode=2：通行止と「規制中」のみ
        elif mode == 2 and (item_list[6] == '通行止' or item_list[6] == '規制中'): 
            if item_list[3] == '': #起点が空欄
                tx = item_list[11] + '：' + item_list[4] + '(' + item_list[2] + ')で' + \
                                 item_list[5] + 'のため' + item_list[6]
                traffic_list.append(tx)
            else: #起点がある
                tx = item_list[11] + '：' + item_list[3] + '→' + item_list[4] + \
                                 '(' + item_list[2] + ')で' + \
                                 item_list[5] + 'のため' + item_list[6]
                traffic_list.append(tx)

    #print(traffic_list)
    #toot_header = '【交通情報：' + code_text + '地方' + '(' + up_time + ')】\n★'
    toot_header = '【交通情報：' + code_text + '地方' + '(' + up_time + ')】\n'

    if mode == 0:
        kisei = '通行止'
    elif mode == 1:
        kisei = '規制'
    elif mode == 2:
        kisei = '通行止と「規制中」'

    if traffic_list: #規制があればトゥート内容を作る
        toot_text = '\n'.join(traffic_list)
        #print(toot_text)
    else:
        toot_text = '現在、' + kisei + 'はありません☆'

    #toot_text = toot_header + toot_text

    #return toot_text
    return toot_header, toot_text


#直接実行すると以下が実行される（モジュールとして読み込んだ場合は実行されない）
if __name__ == '__main__': 
    print(
        get_traffic('北海道', 2), '\n',
        get_traffic('東北', 2), '\n',
        get_traffic('関東', 2), '\n',
        get_traffic('中部', 2), '\n',
        get_traffic('北陸', 2), '\n',
        get_traffic('近畿', 2), '\n',
        get_traffic('中国', 2), '\n',
        get_traffic('四国', 2), '\n',
        get_traffic('九州', 2), '\n',
        get_traffic('沖縄', 2), '\n',
        get_traffic('その他', 2)        
    )
    pass
