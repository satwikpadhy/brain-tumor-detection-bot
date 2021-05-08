import requests
def brainTumorPicDownload(endpoint, chat_id):
    reply_text = 'Send a Picture of the MRI'
    method_resp = 'sendMessage'
    query_resp = {'chat_id' : chat_id, 'text' : reply_text}
    requests.get(endpoint + '/' + method_resp, params=query_resp)
    return reply_text