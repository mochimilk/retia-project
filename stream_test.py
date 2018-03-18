# -*- coding: utf-8 -*-
from mastodon import Mastodon, StreamListener
import re
import random
import json
import datetime
import threading

global mastodon

MyUserName = 'v_idol_retia' #自分のusername
tag_cutter = re.compile(r"<[^>]*?>") #htmlタグ許すまじ
display_name_cutter = re.compile(r"(?:@|#|http.*:\/\/)") #display_nameでのいたずら防止
tl_list = [] #重複チェック用キャッシュ
dupli_count = 3 #重複チェックカウンター（キャッシュに取り込むトゥート数）


# botの投稿に反応しない
def is_bot(app):
    if not app: return False
    bot_names = [
        'オフ会カレンダー',
        'off_bot',
        '安価bot',
        '不適切bot',
        "社畜丼トレンド",
        '色bot',
        'ダイスbot',
        'VRれてぃあ',
        '漣ちゃん',
        'Cordelia',
        'nekonyanApp'
    ] 

    print('BotCK:', app['name'])
    return app['name'] in bot_names


#ニックネーム機能
def convert_nick(u_name, d_name):
    f = open('nickname_list.json', 'r', encoding = 'utf-8')
    nick_dict = json.load(f)
    nickname = ''

    if u_name in nick_dict.keys():
        if u_name == 'daiotail':
            for i in range(1,random.randint(2, 16)):
                nickname = nickname + 'お'
            nickname = nickname + 'さん'
        else:
            nickname = nick_dict[u_name]
    else:
        nickname = d_name +'さん'

    f.close()
    return nickname


# 過去の投稿との重複チェック（連投防止）
#def toot_check(tooo, lim=3):
def toot_check(tooo, t_list, lim=3):
    """
    my_dict = mastodon.account_verify_credentials()
    my_toots = mastodon.account_statuses(my_dict['id'], limit=lim)
    
    my_toots0 = tag_cutter.sub("", my_toots[0]['content'])
    my_toots1 = tag_cutter.sub("", my_toots[1]['content'])
    my_toots2 = tag_cutter.sub("", my_toots[2]['content'])
    cklist = [my_toots0, my_toots1, my_toots2]

    cklist = tooo
    """
    #if tooo in cklist:
    #print("too:", tooo, "t_list:", t_list)
    if tooo in t_list:
        ckt = True
    else:
        ckt = False
    return ckt

    """
    i = 0
    ckt = False
    while i < lim + 1:
        my_toots0 = tag_cutter.sub("", my_toots[i]['content'])
        if tooo == my_toots0:
            ckt = True
            return ckt
            break
        i += 1
    return ckt
    """


# 素メンションテスト（LTLにでてくるやつV2
def retia_mention(content, mention_d_name):
    random.seed()
    tx_list = ['いまかわいいって言った？　#れてぃあたん', 'どしたの？　#れてぃあたん', 'それはダメだよ？　#れてぃあたん','なになに？　#れてぃあたん']
    tx = random.choice(tx_list)
    return tx


# バ部は廃部
def is_babu(content: str) -> bool:
    return bool(re.search(r"ママー+[ッ!！]", content))

def babu_haibu(converted_text):
    toot_string = ''
    if is_babu(converted_text):
        print('BBCK: 廃部')
        toot_string = 'バ部は廃部　#れてぃあたん'
    else:
        print('BBCK: No Babu')
        toot_string = ''
    return toot_string


# 〇〇と聞いて
def is_kiite(content: str):
    return re.search(r"(ダーツ)|(カラオケ)|((?:奢|おご)[りる])|(メイド)|(お(?:ねえ|姉|ねー)ちゃん)|((?:可愛い|かわいい)[女男]の[子娘])|(彼[女氏][ぁ-んァ-ン０-９0-9人金円万画像、。]*[ほ欲]しい)", content)

def to_kiite(converted_text):
    toot_string = ''
    mKiite = is_kiite(converted_text)
    if mKiite:
        print('KiiteCK: 聞こえた')
        toot_string = mKiite.group() + 'と聞いて　#れてぃあたん'
    else:
        print('KiiteCK: No Match')
        toot_string = ''
    return toot_string


# 〇〇さんかわいい
def is_kawaii(content: str) -> bool:
    return bool(re.search(r".+(?!時間)(?:とき|時).+るから|(おしゅし)|((?:た|だ)けどね.?？$)|(なんちゃって.?$)|.+(ましゅ.+)$|.+(しゅき).*$", content))

def oo_kawaii(converted_text, usr_name):
    toot_string = ''
    if is_kawaii(converted_text):
        print('KawaiiCK: かわいい')
        toot_string = usr_name + 'かわいい☆　#れてぃあたん'
    else:
        print('KawaiiCK: No Sweetie')
        toot_string = ''
    return toot_string


# 〇〇さんえっち
def is_ecchi(content: str) -> bool:
    return bool(re.search(r"(おっぱい.?[も揉](?:む|んで|みた))|(?:一緒|いっしょ)に寝[よて]|れてぃあ(?:たん)?、*(つきあって|付き合って|愛してる|の?えっち)", content))

def oo_ecchi(converted_text, usr_name):
    toot_string = ''
    if is_ecchi(converted_text):
        print('HCK: えっち')
        toot_string = usr_name + 'のえっち・・・　#れてぃあたん'
    else:
        print('HCK: No Ecchi')
        toot_string = ''
    return toot_string


# 何曜日？
def is_youbi(content: str) -> bool:
    return bool(re.search(r"(?:きょう|今日)(?:は|って)*何曜日", content))

def nani_youbi(converted_text):
    toot_string = ''
    youbi = ["月","火","水","木","金","土","日"]
    nowyobi = datetime.date.today()
    random.seed(nowyobi.weekday())
    y = random.randint(0,6)
    if is_youbi(converted_text):
        toot_string = youbi[y] + '曜日だよ☆　#れてぃあたん'
    else:
        toot_string = ''
    return toot_string


# れてぃあたんかわいい⇒〇〇さん大好き
def is_retikawa(content: str) -> bool:
    return bool(re.search(r"(れてぃあ(?:たん)?[は]?)(?!(?:かわい|可愛い)くない)(?:かわいい|可愛い|すてき|素敵|美人)(?!？|\?|ない|無い|とでも|、|で[は]?ない)", content))

def retikawa(converted_text, usr_name):
    random.seed()
    toot_string = ''
    tx_list = ['大好き☆','ありがと☆','・・・☆','のほうがかわいいよ☆',]
    tx = random.choice(tx_list)
    if is_retikawa(converted_text):
        print('RetiKawaCK: 大好き')
        toot_string = usr_name + tx + '　#れてぃあたん'
    else:
        print('RetiKawaCK: Zenzen Sweetie Janai')
        toot_string = ''
    return toot_string


# れてぃあたんかわいくない⇒怒り
def is_not_retikawa(content: str) -> bool:
    return bool(re.search(r"(れてぃあ(?:たん)?[は]?)(?:(?:かわいく|可愛いく|美人|すてき|素敵)[ではじゃ]?ない)", content))

def not_retikawa(converted_text, usr_name):
    random.seed()
    toot_string = ''
    tx_list = ['爆破してくるね☆','・・・','にブロッコリー刺してくる☆',]
    tx = random.choice(tx_list)
    if is_not_retikawa(converted_text):
        print('NoRetiKawaCK: 爆破')
        toot_string = 'ちょっと' + usr_name + tx + '　#れてぃあたん'
    else:
        print('NoRetiKawaCK: Sweetie')
        toot_string = ''
    return toot_string


# れてぃあたん
def retia_tan(converted_text):
    toot_string = ''
    if converted_text.find("れてぃあたん") >= 0:
        print('RetiaCK: 呼んだ？')
        toot_string = '呼んだ？　#れてぃあたん'
    else:
        print('RetiaCK: No Retia')
        toot_string = ''
    return toot_string


# ローカルタイムラインのストリーム取得
class MyStreamListener(StreamListener):
    def __init__(self):
        super(MyStreamListener, self).__init__()


    def handle_stream(self, response):
        try:
            super().handle_stream(response)
        except:
            # do something
            raise


    def on_update(self, status):
        tl_cont = tag_cutter.sub("", status['content'])
        tl_display_name = display_name_cutter.sub("☆", status['account']['display_name'])
        tl_display_name = convert_nick(status['account']['username'], tl_display_name) #ニックネーム
        #メンション用のidとaccount_name取得
        mention_to_id = ''
        match_acct = re.search(r"^(@v_idol_retia)[\s　](.+)", tl_cont)

        if match_acct:
            mention_to_id = status['id']
            mention_acct = status['account']['username']
        else:
            mention_to_id = ''
            mention_acct = ''

        #重複チェック用自分の投稿キャッシュ
        if status['account']['username'] == MyUserName:
            tl_list.append(tl_cont)
            if len(tl_list) > dupli_count:
                tl_list.pop(0)

        #タイムライン表示
        print("{},{:%Y-%m-%d %H:%M:%S}/{}/{}/{}".format(
            'UPDATE_LOCAL',
            status['created_at'],
            mention_to_id,
            tl_display_name,
            tl_cont
            )
        )

        #トゥー内容初期化
        my_next_toot = ''

        #トゥー生成
        if is_bot(status['application']): #botリストに入っているなら反応しない
            my_next_toot = ''
        elif status['spoiler_text'] != '': #CWなら反応しない
            my_next_toot = ''
        elif babu_haibu(tl_cont) != '': #バ部は廃部
            my_next_toot = babu_haibu(tl_cont)
        elif oo_kawaii(tl_cont, tl_display_name) != '': #〇〇さんかわいい
            my_next_toot = oo_kawaii(tl_cont, tl_display_name)
        elif oo_ecchi(tl_cont, tl_display_name) != '': #〇〇さんえっち
            my_next_toot = oo_ecchi(tl_cont, tl_display_name)
        elif nani_youbi(tl_cont) != '': #何曜日
            my_next_toot = nani_youbi(tl_cont)
        elif to_kiite(tl_cont) != '': #〇〇と聞いて
            my_next_toot = to_kiite(tl_cont)
        elif mention_to_id != '': #LTLに表示されるメンションに対する反応
            my_next_toot = '@' + mention_acct + ' ' + retia_mention(tl_cont, tl_display_name)
        elif retikawa(tl_cont, tl_display_name) != '': #れてぃあたんかわいい
            my_next_toot = retikawa(tl_cont, tl_display_name)
        elif not_retikawa(tl_cont, tl_display_name) != '': #れてぃあたん可愛くない
            my_next_toot = not_retikawa(tl_cont, tl_display_name)
        elif retia_tan(tl_cont) != '': #れてぃあたんを呼んだ場合
            my_next_toot = retia_tan(tl_cont)


        #生成した内容が過去トゥーと一致したらトゥーしない
        #何も生成してない場合もトゥーしない
        print('Next:', my_next_toot)
        print('PASTCK:', toot_check(my_next_toot, tl_list, 3))
        if toot_check(my_next_toot, tl_list, 3):
            print('TOOT: ERR: 重複')
            my_next_toot = ''
        elif my_next_toot == '':
            print('TOOT: No Toot.')
            my_next_toot = ''
        else:
            print('TOOT: Toot OK.', mention_to_id, '/', mention_acct)
            mastodon.status_post(
                status = my_next_toot,
                in_reply_to_id = mention_to_id,
                visibility='public'
            )
        pass


    def on_delete(self, status_id):
        #self.logger.info(f"status delete_event: {status_id}")
        print(f"status delete_event: {status_id}")
        pass


    def handle_heartbeat(self):
        """The server has sent us a keep-alive message. This callback may be
        useful to carry out periodic housekeeping tasks, or just to confirm
        that the connection is still open."""
        #print('Server: Keep-Alive.')
        pass


# ホームタイムラインのストリーム取得
class MyUserListener(StreamListener):
    def __init__(self):
        super(MyUserListener, self).__init__()


    def handle_stream(self, response):
        try:
            super().handle_stream(response)
        except:
            # do something
            raise

    def on_update(self, status):
        tl_cont = tag_cutter.sub("", status['content'])
        tl_display_name = display_name_cutter.sub("☆", status['account']['display_name'])
        tl_display_name = convert_nick(status['account']['username'], tl_display_name) #ニックネーム
        #メンション用のidとaccount_name取得
        mention_to_id = ''
        match_acct = re.search(r"^(@v_idol_retia)[\s　](.+)", tl_cont)

        if match_acct:
            mention_to_id = status['id']
            mention_acct = status['account']['username']
        else:
            mention_to_id = ''
            mention_acct = ''

        #タイムライン表示
        print("{},{:%Y-%m-%d %H:%M:%S}/{}/{}/{}".format(
            'UPDATE_HOME',
            status['created_at'],
            mention_to_id,
            tl_display_name,
            tl_cont
            )
        )
        pass

    def on_notification(self, notification):
        print("NOTICE:", notification)
        pass


# StreamListenerクラスを作る
class LTL():
    def __init__(self):
        pass

    def t_local():
        listener = MyStreamListener()
        mastodon.stream_local(listener)


class HTL():
    def __init__(self):
        pass

    def t_home():
        listener = MyUserListener()
        mastodon.stream_user(listener)


# ★メインの処理
if __name__ == '__main__':
    mastodon = Mastodon(
        client_id="xxxxxxx.txt",
        access_token="xxxxxxxx.txt",
        api_base_url = "https://mstdn-workers.com"
    )

ltl = threading.Thread(target=LTL.t_local, daemon = True)
htl = threading.Thread(target=HTL.t_home, daemon = True)
ltl.start()
htl.start()

while True:
    ltl.join(0.5)
    htl.join(0.5)
