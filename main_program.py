#!/usr/bin/env python3
import requests
import sys
import time
from decouple import config
from picDownload import brainTumorPicDownload

botapi_url = 'https://api.telegram.org/bot'
token = config('token_brain')
path = config('path_tumor')
endpoint = botapi_url + token
offset = 0
method = 'getUpdates'
request = endpoint + '/' + method
reply_text=''

while(True):
    try:
        query = {'offset': offset}
        response = requests.get(request, params=query)
        json = response.json()
        if(json['result']):
            result = json['result']
            for update in result:
                if 'message' in update:
                    message = update['message']
        
                    if 'text' in message:
                        text = message['text']
                        spl = text.split(' ')
                        chat_id = message['chat']['id']
                        command = spl[0]
                        reply_text = ''
                        
                        if(command == '/start'):
                            reply_text = 'Hello I am @braintumor_bot. Send /help to get a list of commands.'
                        elif(command == '/help'):
                            file_name = path + 'help'
                            f = open(file_name)
                            lines= f.readlines()
                            for line in lines:
                                reply_text += line
                        elif(command == '/tumor'):
                            reply_text = brainTumorPicDownload(endpoint, message, chat_id, token,path)

                        method_resp = 'sendMessage'
                        query_resp = {'chat_id' : chat_id, 'text' : reply_text}
                        requests.get(endpoint + '/' + method_resp, params=query_resp)
                offset = int(update['update_id']) + 1


    except ValueError:
        print(time.ctime(), ": Broken response: ", response)
        time.sleep(60)        
    except KeyboardInterrupt:
        print(time.ctime(), ": Ctrl-C pressed - exiting")
        exit(1)
    except:
        print(time.ctime(), ": Unexpected error", sys.exc_info()[0])
        time.sleep(90)