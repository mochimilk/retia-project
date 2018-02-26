# -*- coding: utf-8 -*-
from mastodon import Mastodon, StreamListener
import re
import random

global mastodon
MyUserName = 'v_idol_retia' #このユーザーのトゥー稿には反応しない
tag_cutter = re.compile(r"<[^>]*?>") #htmlタグ許すまじ
display_name_cutter = re.compile(r"(?:@|#|http.*:\/\/)") #display_nameでのいたずら防止


# 過去の投稿との重複チェック（連投防止）
def toot_check(tooo, lim=3):
    my_dict = mastodon.account_verify_credentials()
    my_toots = mastodon.account_statuses(my_dict['id'], limit=lim)

    """
    my_toots0 = tag_cutter.sub("", my_toots[0]['content'])
    my_toots1 = tag_cutter.sub("", my_toots[1]['content'])
    my_toots2 = tag_cutter.sub("", my_toots[2]['content'])
    cklist = [my_toots0, my_toots1, my_toots2]

    if tooo in cklist:
        ckt = True
    else:
        ckt = False
    return ckt
    """

    i = 0
    ckt = False
    while i < lim + 1:
        my_toots0 = tag_cutter.sub("", my_toots[0]['content'])
        if tooo == my_toots0:
            ckt = True
            return ckt
            break
        i += 1
    return ckt


# 自分の投稿に反応しない
def self_check(my_name):
    tl = mastodon.timeline(timeline='local', limit=1, max_id=None)
    if my_name == tl[0]['account']['username']:
        selfCK = True
    else:
        selfCK = False
    return selfCK


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


# れてぃあたん
def is_retia(content: str) -> bool:
    return bool(re.search(r"れてぃあたん", content))

def retia_tan(converted_text):
    toot_string = ''
    if self_check(MyUserName):
        print('RetiaCK: ERR: 自分のトゥーに反応')
        toot_string = ''
    elif is_retia(converted_text):
        print('RetiaCK: 呼んだ？')
        toot_string = '呼んだ？　#れてぃあたん'
    else:
        print('RetiaCK: No Retia')
        toot_string = ''
    return toot_string


# 〇〇と聞いて
def is_kiite(content: str):
    return re.search(r"(カラオケ)|(ヒトカラ)|(メイド)|(お[ね姉][えー]*ちゃん)|((?:可愛い|かわいい)[女男]の[子娘])|(彼[女氏][ぁ-んァ-ン０-９a-zA-Z0-9\-]*[ほ欲]しい)", content)

def to_kiite(converted_text):
    toot_string = ''
    mKiite = is_kiite(converted_text)
    if self_check(MyUserName):
        print('KiiteCK: ERR: 自分のトゥーに反応')
        toot_string = ''
    elif mKiite:
    #if mKiite:
        print('KiiteCK: 聞こえた')
        toot_string = mKiite.group() + 'と聞いて　#れてぃあたん'
    else:
        print('KiiteCK: No Match')
        toot_string = ''
    return toot_string


# 〇〇さんかわいい
def is_kawaii(content: str) -> bool:
    return bool(re.search(r"(.+(?:とき|時).+るから|(おしゅし)|((?:た|だ)けどね.?？$)|(なんちゃって.?$)|.+(ましゅ.+)$|.+(しゅき).*)", content))

def oo_kawaii(converted_text, usr_name):
    toot_string = ''
    if self_check(MyUserName):
        print('KawaiiCK: ERR: 自分のトゥーに反応')
        toot_string = ''
    elif is_kawaii(converted_text):
    #if is_kawaii(converted_text):
        print('KawaiiCK: かわいい')
        toot_string = usr_name + 'さんかわいい☆　#れてぃあたん'
    else:
        print('KawaiiCK: No Sweetie')
        toot_string = ''
    return toot_string


# れてぃあたんかわいい⇒〇〇さん大好き
def is_retikawa(content: str) -> bool:
    return bool(re.search(r"(れてぃあたん(?:かわいい|可愛い))", content))

def retikawa(converted_text, usr_name):
    toot_string = ''
    if self_check(MyUserName):
        print('RetiKawaCK: ERR: 自分のトゥーに反応')
        toot_string = ''
    elif is_retikawa(converted_text):
    #if is_retikawa(converted_text):
        print('RetiKawaCK: 大好き')
        toot_string = usr_name + 'さん大好き☆　#れてぃあたん'
    else:
        print('RetiKawaCK: Zenzen Sweetie Janai')
        toot_string = ''
    return toot_string


# ストリーム取得して実際に何かするところ
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
        #tl = mastodon.timeline(timeline='local', limit=1, max_id=None)
        tl = [status]
        tl_cont = tag_cutter.sub("", tl[0]['content'])
        #tl_display_name = tl[0]['account']['display_name']
        tl_display_name = display_name_cutter.sub("☆", tl[0]['account']['display_name'])

        print("{},{:%Y-%m-%d %H:%M:%S}/{}/{}".format(
            'UP',
            tl[0]['created_at'],
            tl_display_name,
            tl_cont
            )
        )

        #トゥー内容初期化
        my_next_toot = ''

        #トゥー生成
        if babu_haibu(tl_cont) != '':
            my_next_toot = babu_haibu(tl_cont)
        elif oo_kawaii(tl_cont, tl_display_name) != '':
            my_next_toot = oo_kawaii(tl_cont, tl_display_name)
        elif to_kiite(tl_cont) != '':
            my_next_toot = to_kiite(tl_cont)
        elif retikawa(tl_cont, tl_display_name) != '':
            my_next_toot = retikawa(tl_cont, tl_display_name)
        elif retia_tan(tl_cont) != '':
            my_next_toot = retia_tan(tl_cont)


        #生成した内容が過去トゥーと一致したらトゥーしない
        #何も生成してない場合もトゥーしない
        print('Next:', my_next_toot)
        print('PASTCK:', toot_check(my_next_toot, 3))
        if toot_check(my_next_toot, 3):
            print('TOOT: ERR: 重複')
            my_next_toot = ''
        elif my_next_toot == '':
            print('TOOT: No Toot.')
            my_next_toot = ''
        else:
            print('TOOT: Toot OK.')
            mastodon.status_post(status = my_next_toot)

        pass

    def on_delete(self, status_id):
        #self.logger.info(f"status delete_event: {status_id}")
        print(f"status delete_event: {status_id}")
        pass


if __name__ == '__main__':
    mastodon = Mastodon(
        client_id="XXXXX.txt",
        access_token="XXXXX.txt",
        api_base_url = "https://mstdn-workers.com"
    )

    listener = MyStreamListener()
    mastodon.stream_local(listener)
