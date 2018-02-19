# -*- coding: utf-8 -*-
from mastodon import Mastodon, StreamListener
import re
from numpy import *
from numpy.random import *


global mastodon
MyUserName = 'XXXXX' #このユーザーのトゥーには反応しない

#重複チェック
def toot_check(tooo, lim=3):
    my_dict = mastodon.account_verify_credentials()
    my_toots = mastodon.account_statuses(my_dict['id'], limit=lim)

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
    while i < lim:
        conv = re.compile(r"<[^>]*?>")
        my_toots0 = conv.sub("", my_toots[0]['content'])
        if tooo == my_toots0:
            ckt = True
            return ckt
            break
        i += 1
    return ckt
    """


#自分に反応しない
def self_check(u_name):
    tl = mastodon.timeline(timeline='local', limit=1, max_id=None)
    if u_name == tl[0]['account']['username']:
        selfCK = True
    else:
        selfCK = False
    return selfCK


#バ部は廃部
def babu_haibu(context):
    toot_string = ''
    if re.search(r"ママー+[ッ|!|！]", context):
        print('BBCK: 廃部')
        toot_string = 'みや「バ部は廃部」 #test'
    else:
        print('BBCK: No Babu')
        toot_string = ''
    return toot_string


#〇〇と聞いて
def to_kiite(context):
    toot_string = ''
    mKiite = re.search(r"(ヒトカラ)|(お(ねえ|姉|ねー)ちゃん)|(可愛い女の子)", context)
    #if self_check(MyUserName):
    #    print('KIITECK: ERR: 自分のトゥーに反応')
    #    toot_string = ''
    #elif mKiite:
    if mKiite:
        print('KIITECK: 聞こえた')
        toot_string = 'みや「' + mKiite.group() + 'と聞いて」 #test'
    else:
        print('KIITECK: No Match')
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
        elif to_kiite(tl_cont) != '':
            my_next_toot = to_kiite(tl_cont)


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
