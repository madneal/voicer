from aip import AipSpeech
from aip import AipOcr
import subprocess
import os
import sys
import time
import io
import yaml
from PIL import Image
from mutagen.mp3 import MP3


SCREENSHOT = 'screenshot.png'
AUDIO = 'audio.mp3'



def get_screenshort():
    if os.path.isfile(SCREENSHOT):
        try:
            os.remove(SCREENSHOT)
        except:
            pass
    process = subprocess.Popen('adb shell screencap -p',
    shell=True, stdout=subprocess.PIPE)
    binary_screenshot = process.stdout.read()
    binary_screenshot = binary_screenshot.replace(b'\r\n', b'\n')
    f = open(SCREENSHOT, 'wb')
    f.write(binary_screenshot)
    f.close()


def get_config():
    with open('config.yaml', 'r', encoding='utf8') as f:
        config = yaml.load(f)
    return config


def ocr_text(img):
    config_baidu = config['baidu']
    client = AipOcr(str(config_baidu['app_id']), config_baidu['api_key'], config_baidu['secret_key'])
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    image_data = img_byte_arr.getvalue()
    response = client.basicGeneral(image_data)
    words_result = response['words_result']
    texts = ''
    for x in words_result:
        texts += x['words']
    return texts


def generate_voice(text):
    if os.path.isfile(AUDIO):
        try:
            os.remove(AUDIO)
        except:
            pass
    config_baidu = config['baidu']
    client = AipSpeech(str(config_baidu['app_id']), config_baidu['api_key'], config_baidu['secret_key'])
    result = client.synthesis(text, 'zh', 1, {
        'vol': 5,
    })
    # 识别正确返回语音二进制 错误则返回dict 参照下面错误码
    if not isinstance(result, dict):
        with open('audio.mp3', 'wb') as f:
            f.write(result)
        f.close()


def get_voice_length():
    duration = int(MP3(AUDIO).info.length * 1000) + 500
    return str(duration)

def press(duration):
    command = 'adb shell input swipe 500 1000 500 1000 ' + duration
    process = subprocess.Popen(command,
    shell=True, stdout=subprocess.PIPE)


def play_mp3():
    subprocess.call(r'C:\Program Files\Windows Media Player\wmplayer.exe C:\Users\neal1\project\voicer\audio.mp3')

if __name__ == '__main__':
    get_screenshort()
    config = get_config()
    img = Image.open(SCREENSHOT)
    code_region = img.crop((10, 650, 1800, 900))
    code_region.show()
    text = ocr_text(code_region)
    print(text)
    generate_voice(text)
    duration = get_voice_length()
    press(duration)
    play_mp3()
