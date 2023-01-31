#Simple Bilibili Downloader
import requests
import re
import json
import subprocess
import ffmpeg
import sys
import os

headers = {
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
}

def download_response(url):
    response = requests.get(url=url,headers=headers)
    return response

def get_response(video_url):
    print('Fetching Video Data from Bilibili...')
    response = requests.get(url=video_url,headers=headers)
    json_data = re.findall('window.__playinfo__=(.*?)</script>', response.text)[0]
    title = re.findall('<title data-vue-meta="true">(.*?)_哔哩哔哩_bilibili</title>', response.text)[0]
    title = re.sub('[^A-Za-z0-9\u4e00-\u9fff\u3010-\u3011]+', '', title)
    print('Video Title: ',title)
    json_object = json.loads(json_data)
    video_url = json_object['data']['dash']['video'][0]['baseUrl']
    audio_url = json_object['data']['dash']['audio'][0]['baseUrl']
    save(title,video_url,audio_url)
    return title
    
def save(title, video_url, audio_url):
    print('Downloading Audio and Video...')
    audio_content = download_response(audio_url).content
    video_content = download_response(video_url).content
    with open(title + '.mp3', mode='wb') as f:
        f.write(audio_content)
    with open(title + '.mp4', mode='wb') as f:
        f.write(video_content)
      
def merge(filename):
    print('Merging Audio and Video...')
    cmd = f'ffmpeg -y -i {filename}.mp4 -i {filename}.mp3 -c:v copy -c:a aac -strict experimental {filename}_merged.mp4'
    subprocess.call(cmd, shell=True)
    print('Merging Completed...')

filename = get_response('https://www.bilibili.com/video/'+sys.argv[1])
merge(filename)
print('Cleanup raw Video and Data file...')
os.remove(filename+'.mp3')
os.remove(filename+'.mp4')