from datetime import datetime
from tqdm import tqdm
import requests
import re

url = input('\nEnter the URL of Facebook Video: ')
check = re.match(r'^(https:|)[/][/]www.([^/]+[.])*facebook.com', url)

if check:
    html = requests.get(url).content.decode('utf-8')
else:
    print('\nThis is not a Facebook Video URL!')

_qualityHD = re.search('hd_src:"https', html)
_qualitySD = re.search('sd_src:"https', html)
_HD = re.search('hd_src:null', html)
_SD = re.search('sd_src:null', html)

listData = []
_theList = [_qualityHD, _qualitySD, _HD, _SD]
for id, value in enumerate(_theList):
    if value != None:
        listData.append(id)


blockSize = 1024

def download_hd():
    print('\nDownloading the video in HD quality')
    videoURL = re.search(r'hd_src:"(.+?)"', html).group(1)
    fileSizeRequest = requests.get(videoURL, stream=True)
    fileSize = int(fileSizeRequest.headers['Content-Length'])
    fileName = datetime.strftime(datetime.now(), '%Y-%m-%d-%H-%M-%S')
    t = tqdm(total=fileSize, unit='B', unit_scale=True, desc=fileName, ascii=True)
    with open(fileName + '.mp4', 'wb') as f:
        for data in fileSizeRequest.iter_content(blockSize):
            t.update(len(data))
            f.write(data)
    t.close()
    print('Video downloaded succesfully!!!')

def download_sd():
    print('\nDownloading the video in SD quality')
    videoURL = re.search(r'sd_src:"(.+?)"', html).group(1)
    fileSizeRequest = requests.get(videoURL, stream=True)
    fileSize = int(fileSizeRequest.headers['Content-Length'])
    fileName = datetime.strftime(datetime.now(), '%Y-%m-%d-%H-%M-%S')
    t = tqdm(total=fileSize, unit='B', unit_scale=True, desc=fileName, ascii=True)
    with open(fileName + '.mp4', 'wb') as f:
        for data in fileSizeRequest.iter_content(blockSize):
            t.update(len(data))
            f.write(data)
    t.close()
    print('Video downloaded succesfully!!!')

try:
    if len(listData) == 2:
        if 0 in listData and 1 in listData:
            _getInputOne = str(input('\nPress "A" to download the video in HD quality.\nPress "B" to download the video in SD quality.\n ')).upper()
            if _getInputOne == 'A':
                download_hd()
            if _getInputOne == 'B':
               download_sd()
    if len(listData) == 2:
        if 1 in listData and 2 in listData:
            _getInputTwo = str(input('This video is not available in HD quality. Would you like to download it? ("Y" or "N"): ')).upper()
            if _getInputTwo == 'Y':
                download_sd()
            if _getInputTwo == 'N':
                exit()
    if len(listData) == 2:
        if 0 in listData and 3 in listData:
            _getInputTwo = str(input('This video is not available in HD quality. Would you like to download it? ("Y" or "N"): ')).upper()
            if _getInputTwo == 'Y':
                download_hd()
            if _getInputTwo == 'N':
                exit()

except(KeyboardInterrupt):
    print('Failed')