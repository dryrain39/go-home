from korail2 import *
import json
import codecs
import collections
import requests
from time import sleep


def load_setting():
    data_file = codecs.open('setting.json', 'r', 'utf-8')
    return json.loads(data_file.read(), object_pairs_hook=collections.OrderedDict)


setting = load_setting()


def push_send(msg, bot_token=setting['tgBotToken'], chat_id=setting['chatId']):
    requests.get('https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + chat_id + '&text=' + msg)


korail = Korail(setting['userId'], setting['password'])

dep = '서울'
arr = '동대구'
date = '20190204'
time = '130000'
# date = '20190118'
# time = '190000'

catch = False

while catch is False:
    sleep(1)
    try:
        trains = korail.search_train(dep, arr, date, time, train_type=100, include_no_seats=False)
        for train in trains:
            try:
                korail.reserve(train, option=ReserveOption.GENERAL_ONLY)
                catch = True
                push_send('예약완료!!!! 20분내로 결제하세요.')
                push_send(str(train))
                break
            except SoldOutError:
                print('No Seats!! T.T')
                pass
            except Exception as e:
                push_send('ERROR In your code.')
                push_send(str(e))
                pass

    except NoResultsError as e:
        print('No Seats!! T.T')
        pass

    except Exception as e:
        push_send('ERROR In your code.')
        push_send(str(e))
        pass
