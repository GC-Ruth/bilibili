import sys
import time
import os
import requests
import re
import ffmpeg
from lxml import etree
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 Edg/106.0.1370.52',
    'referer': 'https://www.bilibili.com/'
}       # UA伪装和防盗链


def 视频下载():
    url = f'https://www.bilibili.com/video/{input("输入BV号：")}'
    video_obj = '"video".*?"baseUrl":"(.*?)",".*?'
    audio_obj = '"audio".*?"baseUrl":"(.*?)",".*?'
    page_text = requests.get(url=url, headers=headers).text
    tree = etree.HTML(page_text)
    title = tree.xpath('/html/body/div[2]/div[4]/div[1]/div[1]/h1/text()')[0]   # 提取视频标题
    title = title.replace('/', '~')     # 防止路径出错
    title = title.replace('\\', '~')
    print(f'当前下载的视频是：{title}')
    time.sleep(1)
    all_base_url = tree.xpath('/html/head/script[3]/text()')[0]     # 视频资源总链接
    video_url = re.findall(video_obj, all_base_url)[0]      # 视频链接数据解析
    audio_url = re.findall(audio_obj, all_base_url)[0]      # 音频链接数据解析
    print('正在解析网址...')
    time.sleep(1)
    print('正在下载视频文件...')
    video_data = requests.get(url=video_url, headers=headers, stream=True).content      # 视频资源请求
    print('正在下载音频文件...')
    audio_data = requests.get(url=audio_url, headers=headers, stream=True).content      # 音频资源请求
    with open('./video.mp4', 'wb') as 视频:       # 保存视频到本地
        视频.write(video_data)
    with open('./audio.mp3', 'wb') as 音频:       # 保存音频到本地
        音频.write(audio_data)
    print('下载完成')
    time.sleep(0.5)
    print('正在合成视频，请等待...')
    time.sleep(1)
    video = ffmpeg.input('./video.mp4')
    audio = ffmpeg.input('./audio.mp3')
    out = ffmpeg.output(video, audio, f'./{title}.mp4')     #利用ffmpeg模块合成视频音频
    out.run()
    os.remove('./video.mp4')
    os.remove('./audio.mp3')
    print('视频已保存至当前目录！！！')


def 合集下载():
    BV = input('输入BV号：')
    title_url = f'https://www.bilibili.com/video/{BV}'
    title_resp = requests.get(url=title_url, headers=headers).text
    title_tree = etree.HTML(title_resp)
    title_list = title_tree.xpath('/html/head/title/text()')[0]
    title = title_list.replace('_哔哩哔哩bilibili', '')
    title = title.replace('\\', '~')
    title = title.replace('/', '~')
    title = title.replace('_哔哩哔哩_bilibili', '')
    if not os.path.exists(f'./{title}'):       # 如果视频文件夹目录不存在，则创建一个新的文件夹
        os.mkdir(f'./{title}')
    else:
        print(f'目录{title}已存在，文件将保存至{title}!!!')
    i = 1
    for i in range(1, int(input('输入下载的集数：')) + 1):      # 利用for循环遍历每一个合集内的视频
        url = f'https://www.bilibili.com/video/{BV}?p={i}'
        video_obj = '"video".*?"baseUrl":"(.*?)",".*?'
        audio_obj = '"audio".*?"baseUrl":"(.*?)",".*?'
        page_text = requests.get(url=url, headers=headers).text
        tree = etree.HTML(page_text)
        name_list = tree.xpath(f'/html/head/title/text()')[0]
        name = name_list.replace('_哔哩哔哩_bilibili', '')
        name = name.replace('\\', '~')
        name = name.replace('/', '~')
        print(f'当前下载的视频是：{name}')
        time.sleep(1)
        all_base_url = tree.xpath('/html/head/script[3]/text()')[0]
        video_url = re.findall(video_obj, all_base_url)[0]
        audio_url = re.findall(audio_obj, all_base_url)[0]
        print('正在解析网址...')
        time.sleep(1)
        print('正在下载视频文件...')
        video_data = requests.get(url=video_url, headers=headers, stream=True).content
        print('正在下载音频文件...')
        audio_data = requests.get(url=audio_url, headers=headers, stream=True).content
        with open(f'./{title}/video.mp4', 'wb') as 视频:
            视频.write(video_data)
        with open(f'./{title}/audio.mp3', 'wb') as 音频:
            音频.write(audio_data)
        print('下载完成')
        time.sleep(0.5)
        print('正在合成视频，请等待...')
        time.sleep(1)
        video = ffmpeg.input(f'./{title}/video.mp4')
        audio = ffmpeg.input(f'./{title}/audio.mp3')
        out = ffmpeg.output(video, audio, f'./{title}/{name}.mp4')
        out.run()
        os.remove(f'./{title}/video.mp4')
        os.remove(f'./{title}/audio.mp3')
        print(f'视频已保存至{title}！！！')
        i += 1


def 番剧下载():
    url = input('请输入完整链接：')
    video_obj = '"base_url":"(.*?)",".*?'
    audio_obj = '"audio".*?"base_url":"(.*?)","'
    vip_obj = '"data".*?"accept_format":"(.*?)","'
    page_text = requests.get(url=url, headers=headers).text
    tree = etree.HTML(page_text)
    title = tree.xpath('/html/head/meta[7]/@content')[0]
    title = title.replace('/', '~')
    title = title.replace('\\', '~')
    if not os.path.exists(f'./{title}'):
        os.mkdir(title)
    else:
        print(f'目录{title}已存在,文件将保存至{title}!!!')
    video_title = tree.xpath('/html/head/title/text()')[0]
    video_title = video_title.replace('-番剧-高清正版在线观看-bilibili-哔哩哔哩', '')
    video_title = video_title.replace('-番剧-高清独家在线观看-bilibili-哔哩哔哩', '')
    video_title = video_title.replace('\\', '~')
    video_title = video_title.replace('/', '~')
    all_url_list = tree.xpath('/html/body/script[4]/text()')[0]
    vip_list = re.findall(vip_obj, all_url_list)[0]
    if vip_list == 'mp4,mp4,mp4,mp4,mp4':
        os.rmdir(title)
        print('该视频需要大会员！！！')
        print('2秒后返回菜单')
        time.sleep(2)
        菜单()
    else:
        video_url = re.findall(video_obj, all_url_list)[0]
        audio_url = re.findall(audio_obj, all_url_list)[0]
        print('正在解析网址...')
        time.sleep(1)
        print('正在下载视频文件...')
        video_data = requests.get(url=video_url, headers=headers, stream=True).content
        print('正在下载音频文件...')
        audio_data = requests.get(url=audio_url, headers=headers, stream=True).content
        with open(f'./{title}/video.mp4', 'wb') as 视频:
            视频.write(video_data)
        with open(f'./{title}/audio.mp3', 'wb') as 音频:
            音频.write(audio_data)
        print('下载完成')
        time.sleep(0.5)
        print('正在合成视频，请等待...')
        time.sleep(1)
        video = ffmpeg.input(f'./{title}/video.mp4')
        audio = ffmpeg.input(f'./{title}/audio.mp3')
        out = ffmpeg.output(video, audio, f'./{title}/{video_title}.mp4')
        out.run()
        os.remove(f'./{title}/video.mp4')
        os.remove(f'./{title}/audio.mp3')
        print(f'视频已保存至{title}！！！')


def 菜单():
    print(''' ▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄            ▄▄▄▄▄▄▄▄▄▄▄       ▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄            ▄▄▄▄▄▄▄▄▄▄▄ 
▐░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░▌          ▐░░░░░░░░░░░▌     ▐░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░▌          ▐░░░░░░░░░░░▌
▐░█▀▀▀▀▀▀▀█░▌▀▀▀▀█░█▀▀▀▀ ▐░▌           ▀▀▀▀█░█▀▀▀▀      ▐░█▀▀▀▀▀▀▀█░▌▀▀▀▀█░█▀▀▀▀ ▐░▌           ▀▀▀▀█░█▀▀▀▀ 
▐░▌       ▐░▌    ▐░▌     ▐░▌               ▐░▌          ▐░▌       ▐░▌    ▐░▌     ▐░▌               ▐░▌     
▐░█▄▄▄▄▄▄▄█░▌    ▐░▌     ▐░▌               ▐░▌          ▐░█▄▄▄▄▄▄▄█░▌    ▐░▌     ▐░▌               ▐░▌     
▐░░░░░░░░░░▌     ▐░▌     ▐░▌               ▐░▌          ▐░░░░░░░░░░▌     ▐░▌     ▐░▌               ▐░▌     
▐░█▀▀▀▀▀▀▀█░▌    ▐░▌     ▐░▌               ▐░▌          ▐░█▀▀▀▀▀▀▀█░▌    ▐░▌     ▐░▌               ▐░▌     
▐░▌       ▐░▌    ▐░▌     ▐░▌               ▐░▌          ▐░▌       ▐░▌    ▐░▌     ▐░▌               ▐░▌     
▐░█▄▄▄▄▄▄▄█░▌▄▄▄▄█░█▄▄▄▄ ▐░█▄▄▄▄▄▄▄▄▄  ▄▄▄▄█░█▄▄▄▄      ▐░█▄▄▄▄▄▄▄█░▌▄▄▄▄█░█▄▄▄▄ ▐░█▄▄▄▄▄▄▄▄▄  ▄▄▄▄█░█▄▄▄▄ 
▐░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌     ▐░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌
 ▀▀▀▀▀▀▀▀▀▀  ▀▀▀▀▀▀▀▀▀▀▀  ▀▀▀▀▀▀▀▀▀▀▀  ▀▀▀▀▀▀▀▀▀▀▀       ▀▀▀▀▀▀▀▀▀▀  ▀▀▀▀▀▀▀▀▀▀▀  ▀▀▀▀▀▀▀▀▀▀▀  ▀▀▀▀▀▀▀▀▀▀▀ 
                                                                                                           --by 空白''')
    print('\n1.视频单个下载(输入1)\n2.视频合集下载(输入2)\n3.番剧下载(输入3)\n4.退出程序(输入4)')
    操作 = input('请输入操作：')
    if 操作 == '1':
        视频下载()
        菜单()
    elif 操作 == '2':
        合集下载()
        菜单()
    elif 操作 == '3':
        番剧下载()
        菜单()
    elif 操作 == '':
        print('请输入操作内容！！！')
        time.sleep(1)
        菜单()
    else:
        print('程序将在2秒后自动关闭！！！')
        time.sleep(2)
        sys.exit()
菜单()