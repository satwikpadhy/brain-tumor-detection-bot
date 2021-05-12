import requests
import os
from brainTumorDetection import prediction
def brainTumorPicDownload(endpoint, message, chat_id, token, path, file_id):
    method_resp = 'getFile'
    query_resp = {'file_id' : file_id}
    response = requests.get(endpoint + '/' + method_resp, params=query_resp)
    json = response.json()
    reply_text = str(json)
    if json['ok'] == True:
        file_path = json['result']['file_path']
        temp = file_path.split('/')
        file_name = temp[1]
        print(file_name)
        url = 'https://api.telegram.org/file/bot' + token + '/' + file_path
        r = requests.get(url, allow_redirects=True)
        open(path + 'input/brain-mri-images-for-brain-tumor-detection/' + file_name , 'wb').write(r.content)
        try:
            os.rename(path + 'input/brain-mri-images-for-brain-tumor-detection/' + file_name, path + 'input/brain-mri-images-for-brain-tumor-detection/detection_file.jpg')
        except FileExistsError:
            os.remove(path + 'input/brain-mri-images-for-brain-tumor-detection/detection_file.jpg')
            os.rename(path + 'input/brain-mri-images-for-brain-tumor-detection/' + file_name, path + 'input/brain-mri-images-for-brain-tumor-detection/detection_file.jpg')
        reply_text = prediction('detection_file.jpg')
        os.remove(path + 'input/brain-mri-images-for-brain-tumor-detection/detection_file.jpg')
    else:
        reply_text = 'Json error'
    return reply_text
