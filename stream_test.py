# -*- coding: utf-8 -*-
from mastodon import Mastodon, StreamListener
import re
from numpy import *
from numpy.random import *


global mastodon
MyUserName = 'v_idol_retia' #このユーザーのトゥーには反応しない

#重複チェック
def toot_check(tooo, lim=3):
    my_dict = mastodon.account_verify_credentials()
    my_toots = mastodon.account_statuses(my_dict['id'], limit=lim)

    """
    conv = re.compile(r"<[^>]*?>")
    my_toots0 = conv.sub("", my_toots[0]['content'])
    my_toots1 = conv.sub("", my_toots[1]['content'])
    my_toots2 = conv.sub("", my_toots[2]['content'])
    cklist = [my_toots0, my_toots1, my_toots2]

    if tooo in cklist:
        ckt = True
    else:
        ckt = False
    return ckt
    """

    i = 0
    ckt = False
    conv = re.compile(r"<[^>]*?>")
    while i < lim:
        my_toots0 = conv.sub("", my_toots[i]['content'])
        if tooo == my_toots0:
            ckt = True
            return ckt
            break
        i += 1
    return ckt


#自分に反応しない
def self_check(u_name):
    tl = mastodon.timeline(timeline='local', limit=1, max_id=None)
    if u_name == tl[0]['account']['username']:
        selfCK = True
    else:
        selfCK = False
    return selfCK


def is_babu(content: str) -> bool:
    return bool(re.search(r"ママー+[ッ!！]", content))

#バ部は廃部
def babu_haibu(converted_text):
    toot_string = ''
    if is_babu(converted_text):
        print('BBCK: 廃部')
        toot_string = 'バ部は廃部　#れてぃあたん'
    else:
        print('BBCK: No Babu')
        toot_string = ''
    return toot_string


def is_retia(content: str) -> bool:
    return bool(re.search(r"れてぃあたん", content))

#れてぃあたん
def retia_tan(converted_text):
    toot_string = ''
    if self_check(MyUserName):
        print('MYCK: ERR: 自分のトゥーに反応')
        toot_string = ''
    elif is_retia(converted_text):
        print('MYCK: 呼んだ？')
        toot_string = '呼んだ？　#れてぃあたん'
    else:
        print('MYCK: No Retia')
        toot_string = ''
    return toot_string


def is_kiite(content: str):
    return re.search(r"(?|(カラオケ)|(ヒトカラ)|(メイド)|(お[ね姉][えー]*ちゃん)|([可か][愛わ]い*[女男]の[子娘])|(彼女.*[ほ欲]しい))", content)

#〇〇と聞いて
def to_kiite(converted_text):
    toot_string = ''
    mKiite = is_kiite(converted_text)
    #if self_check(MyUserName):
    #    print('KIITECK: ERR: 自分のトゥーに反応')
    #    toot_string = ''
    #elif mKiite:
    if mKiite:
        print('KIITECK: 聞こえた')
        toot_string = mKiite.group() + 'と聞いて　#れてぃあたん'
    else:
        print('KIITECK: No Match')
        toot_string = ''
    return toot_string

def is_kawaii(content: str) -> bool:
    return bool(re.search(r"(?|.+[とき|時].+るから|(おしゅし)|([ただ]けどね.?？)|(なんちゃって)|(ましゅ.))", content))

#〇〇さんかわいい
def oo_kawaii(converted_text, usr_name):
    toot_string = ''
    if is_kawaii(converted_text):
        print('KWIICK: かわいい')
        toot_string = usr_name + 'さんかわいい　#れてぃあたん'
    else:
        print('KWIICK: No Sweetie')
        toot_string = ''
    return toot_string


#ストリーム取得して実際に何かするところ
class MyStreamListener(StreamListener):
    def __init__(self):
        super(MyStreamListener, self).__init__()
        #self.logger = logging.getLogger(self.__class__.__name__)


    def handle_stream(self, response):
        try:
            super().handle_stream(response)
        except:
            # do something
            raise


    def on_update(self, status):
        #self.logger.info(status_info_string(status))
        conv = re.compile(r"<[^>]*?>")
        tl = mastodon.timeline(timeline='local', limit=1, max_id=None)
        tl_cont = conv.sub("", tl[0]['content'])

        print("{},{:%Y-%m-%d %H:%M:%S}/{}/{}".format(
            'UP',
            tl[0]['created_at'],
            tl[0]['account']['display_name'],
            tl_cont
            )
        )

        #トゥー内容初期化
        my_next_toot = ''

        #トゥー生成
        if babu_haibu(tl_cont) != '':
            my_next_toot = babu_haibu(tl_cont)
        elif retia_tan(tl_cont) != '':
            my_next_toot = retia_tan(tl_cont)
        elif to_kiite(tl_cont) != '':
            my_next_toot = to_kiite(tl_cont)
        elif oo_kawaii(tl_cont, tl[0]['account']['display_name']) != '':
            my_next_toot = oo_kawaii(tl_cont, tl[0]['account']['display_name'])



        #生成した内容が過去トゥーと一致したらトゥーしない
        #何も生成してない場合もトゥーしない
        print('Next:', my_next_toot)
        print('PASTCK:', toot_check(my_next_toot, 3))
        if toot_check(my_next_toot, 3):
            print('TOOT: ERR: 重複')
            my_next_toot == ''
        elif my_next_toot == '':
            print('TOOT: No Toot.')
            my_next_toot == ''
        else:
            print('TOOT:',my_next_toot)
            #mastodon.toot(my_next_toot)
            mastodon.status_post(status = my_next_toot)

        pass

    def on_delete(self, status_id):
        #self.logger.info(f"status delete_event: {status_id}")
        print('DELETE')
        pass

if __name__ == '__main__':
    mastodon = Mastodon(
        client_id="XXXXX.txt",
        access_token="XXXXX.txt",
        api_base_url = "https://mstdn-workers.com"
    )

    listener = MyStreamListener()
    mastodon.stream_local(listener)
