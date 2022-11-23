import os
import threading
import time
import requests
import re
import shutil
from tqdm import tqdm
from tkinter import *
from tkinter import messagebox
from Crypto.Cipher import AES
from concurrent.futures import ThreadPoolExecutor

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.42',
    'referer': 'https://www.bilibili.com/'
}


class bilibili_video_get:
    url_dcit = None
    url = 'https://www.bilibili.com/video/'
    url_dcit_obj = 'window.__playinfo.*?{(.*?)<'
    title_obj = '<h1 title="(.*?)" class="video-title tit">'
    video_obj = '"video".*?"baseUrl":"(.*?)","'
    audio_obj = '"audio".*?"baseUrl":"(.*?)","'

    def get_title(self, BV):
        global title
        resp = requests.get(url=self.url + BV, headers=headers).text
        title = re.findall(self.title_obj, resp)[0]
        return title

    def video_url_get(self, BV):
        try:
            resp = requests.get(url=self.url + BV, headers=headers).text
            self.url_dict = re.findall(self.url_dcit_obj, resp)[0]
            video_url = re.findall(self.video_obj, self.url_dict)[0]
            return video_url
        except Exception as error:
            return error

    def audio_url_get(self, BV):
        try:
            resp = requests.get(url=self.url + BV, headers=headers).text
            self.url_dict = re.findall(self.url_dcit_obj, resp)[0]
            audio_url = re.findall(self.audio_obj, self.url_dict)[0]
            return audio_url
        except Exception as error:
            return error

    @staticmethod
    def video_download(video_url):
        try:
            video_data = requests.get(url=video_url, headers=headers, stream=True)
            video_size = int(video_data.headers['Content-Length']) / 1024 / 1024
            with open(f'./{b1.get_title(en2.get())}.mp4', mode='wb') as video:
                for video_tqdm in tqdm(iterable=video_data.iter_content(1024 * 1024),
                                       total=video_size,
                                       unit='MB',
                                       desc='视频'):
                    video.write(video_tqdm)
        except Exception as error:
            return error

    @staticmethod
    def audio_download(audio_url):
        try:
            audio_data = requests.get(url=audio_url, headers=headers, stream=True)
            audio_size = int(audio_data.headers['Content-Length']) / 1024 / 1024
            with open(f'./{b1.get_title(en2.get())}.mp3', mode='wb') as audio:
                for audio_tqdm in tqdm(iterable=audio_data.iter_content(1024 * 1024),
                                       total=audio_size,
                                       unit='MB',
                                       desc='音频'):
                    audio.write(audio_tqdm)
        except Exception as error:
            return error

    @staticmethod
    def download(video_url, audio_url):
        try:
            video_data = requests.get(url=video_url, headers=headers, stream=True)
            video_size = int(video_data.headers['Content-Length']) / 1024 / 1024
            with open(f'./{b1.get_title(en2.get())}.mp4', mode='wb') as video:
                for video_tqdm in tqdm(iterable=video_data.iter_content(1024 * 1024),
                                       total=video_size,
                                       unit='MB',
                                       desc='视频'):
                    video.write(video_tqdm)
            audio_data = requests.get(url=audio_url, headers=headers, stream=True)
            audio_size = int(audio_data.headers['Content-Length']) / 1024 / 1024
            with open(f'./{b1.get_title(en2.get())}.mp3', mode='wb') as audio:
                for audio_tqdm in tqdm(iterable=audio_data.iter_content(1024 * 1024),
                                       total=audio_size,
                                       unit='MB',
                                       desc='音频'):
                    audio.write(audio_tqdm)
        except Exception as error:
            return error


class bilibili_collection_video_get:
    url_dcit = None
    url = 'https://www.bilibili.com/video/'
    url_dcit_obj = 'window.__playinfo.*?{(.*?)<'
    video_obj = '"video".*?"baseUrl":"(.*?)","'
    audio_obj = '"audio".*?"baseUrl":"(.*?)","'
    title_obj = '<h1 title="(.*?)" class="video-title tit">'
    part_title_obj = '"part":"(.*?)","'

    def get_title(self, BV):
        resp = requests.get(url=self.url + BV, headers=headers).text
        title = re.findall(self.title_obj, resp)[0]
        return title

    def get_part_title(self, BV):
        resp = requests.get(url=self.url + BV, headers=headers).text
        title_list = re.findall(self.part_title_obj, resp)
        return title_list

    def video_url_get(self, BV, first, num):
        try:
            if num == 1:
                resp = requests.get(url=self.url + BV + f'?p={first + 1}', headers=headers).text
                self.url_dict = re.findall(self.url_dcit_obj, resp)[0]
                video_url = re.findall(self.video_obj, self.url_dict)[0]
                return video_url
            else:
                url_list = []
                for i in range(first + 1, first + num + 1):
                    resp = requests.get(url=self.url + BV + f'?p={i}', headers=headers).text
                    self.url_dict = re.findall(self.url_dcit_obj, resp)[0]
                    video_url = re.findall(self.video_obj, self.url_dict)[0]
                    url_list.append(video_url)
                    i += 1
                return url_list
        except Exception as error:
            return error

    def audio_url_get(self, BV, first, num):
        try:
            if num == 1:
                resp = requests.get(url=self.url + BV + f'?p={first + 1}', headers=headers).text
                self.url_dict = re.findall(self.url_dcit_obj, resp)[0]
                audio_url = re.findall(self.audio_obj, self.url_dict)[0]
                return audio_url
            else:
                url_list = []
                for i in range(first + 1, first + num + 1):
                    resp = requests.get(url=self.url + BV + f'?p={i}', headers=headers).text
                    self.url_dict = re.findall(self.url_dcit_obj, resp)[0]
                    audio_url = re.findall(self.audio_obj, self.url_dict)[0]
                    url_list.append(audio_url)
                    i += 1
                return url_list
        except Exception as error:
            return error


class yinhua:
    headers_yh = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.35",
        "referer": "http://www.yinghua8.com"
    }

    def title(self, url):
        title_obj = '<h1><a href=.*? target="_blank">(.*?)</a><span>(.*?)</span></h1>'
        page_text = requests.get(url=url, headers=self.headers_yh)
        page_text.encoding = 'utf-8'
        page_text = page_text.text
        title = re.findall(title_obj, page_text)[0][0]
        num = re.findall(title_obj, page_text)[0][1]
        return title

    def num(self, url):
        title_obj = '<h1><a href=.*? target="_blank">(.*?)</a><span>(.*?)</span></h1>'
        page_text = requests.get(url=url, headers=self.headers_yh)
        page_text.encoding = 'utf-8'
        page_text = page_text.text
        title = re.findall(title_obj, page_text)[0][0]
        num = re.findall(title_obj, page_text)[0][1]
        return num

    def url_get(self, url):
        url_obj = 'https:(.*?)mp4'
        page_text = requests.get(url=url, headers=self.headers_yh, timeout=5)
        page_text.encoding = 'utf-8'
        page_text = page_text.text
        url = 'https:' + re.findall(url_obj, page_text)[0]
        m3u8_url = url.replace('$', '')
        return m3u8_url

    def get_head(self, m3u8_url):
        head_obj = 'https://.*?/'
        head = re.findall(head_obj, m3u8_url)[0]
        return head

    def get_true_play_list(self, m3u8_url, head):
        fir_obj = '/.*?/.*?/.*?/.*?/.*'
        true_m3u8 = head + re.findall(fir_obj, requests.get(url=m3u8_url).text)[0]
        try:
            true_playlist = requests.get(url=true_m3u8).text
            true_playlist = re.findall(r'/.*?/.*?/.*?/.*?/.*?.*', true_playlist)
            true_playlist.pop(0)
            return true_playlist
        except Exception as error:
            return error

    def get_key(self, m3u8_url, head):
        fir_obj = '/.*?/.*?/.*?/.*?/'
        key_url = head + re.findall(fir_obj, requests.get(url=m3u8_url).text)[0] + 'key.key'
        key = requests.get(url=key_url).text
        return key

    def boom(self, src, src_new, key, title, num):
        print('视频使用AES-128加密')
        time.sleep(1)
        print('正在获取密钥...')
        time.sleep(1)
        print(f'密钥获取成功，key={key}\n正在解密..')
        time.sleep(1)
        iv = b'0000000000000000'
        f1 = open(src, 'rb')
        f2 = open(src_new, 'wb')
        play_list = f1.read()
        cipher = AES.new(key.encode('utf-8'), AES.MODE_CBC, iv)
        data = cipher.decrypt(play_list)
        if play_list:
            f2.write(data)
            print('解密完成！')

    def thread_download(self, playlist, title, num, i, head):
        try:
            fin_ts = head + playlist[i]
            ts = requests.get(url=fin_ts, stream=True, timeout=20).content
            with open(f'./{title}{num}缓存文件夹/{str("%04d" % i)}.ts', 'wb') as video:
                video.write(ts)
                print(f'节点{i}下载完成')
        except Exception as error:
            try:
                print(f'节点{i}请求超时，正在重试！')
                fin_ts = head + playlist[i]
                ts = requests.get(url=fin_ts, stream=True, timeout=20).content
                with open(f'./{title}{num}缓存文件夹/{str("%04d" % i)}.ts', 'wb') as video:
                    video.write(ts)
            except Exception as error2:
                print(f'节点{i}重试1次失败，2次重试中！')
                try:
                    fin_ts = head + playlist[i]
                    ts = requests.get(url=fin_ts, stream=True, timeout=20).content
                    with open(f'./{title}{num}缓存文件夹/{str("%04d" % i)}.ts', 'wb') as video:
                        video.write(ts)
                except Exception as error2:
                    print(f'节点{i}重试2次失败，3次重试中！')
                    try:
                        fin_ts = head + playlist[i]
                        ts = requests.get(url=fin_ts, stream=True, timeout=20).content
                        with open(f'./{title}{num}缓存文件夹/{str("%04d" % i)}.ts', 'wb') as video:
                            video.write(ts)
                    except Exception as error2:
                        print(f'节点{i}重试3次失败，停止重试！')

    def png_thread_download(self, ts_url_list, title, num, i):
        ts_url = 'https:' + ts_url_list[i] + 'png'
        try:
            ts = requests.get(url=ts_url, stream=True, timeout=30).content
            with open(f'./{title}{num}缓存文件夹/{str("%04d" % i)}.ts', 'wb') as video:
                video.write(ts)
                print(f'节点{i}下载完成')
        except Exception as error:
            print(f'节点{i}请求超时，正在重试！')
            try:
                ts = requests.get(url=ts_url, stream=True, timeout=30).content
                with open(f'./{title}{num}缓存文件夹/{str("%04d" % i)}.ts', 'wb') as video:
                    video.write(ts)
            except Exception as error:
                print(f'节点{i}重试1次失败，2次重试中！')
                try:
                    ts = requests.get(url=ts_url, stream=True, timeout=30).content
                    with open(f'./{title}{num}缓存文件夹/{str("%04d" % i)}.ts', 'wb') as video:
                        video.write(ts)
                except Exception as error:
                    print(f'节点{i}重试2次失败，3次重试中！')
                    try:
                        ts = requests.get(url=ts_url, stream=True, timeout=30).content
                        with open(f'./{title}{num}缓存文件夹/{str("%04d" % i)}.ts', 'wb') as video:
                            video.write(ts)
                    except Exception as error:
                        print(f'节点{i}重试3次失败，停止重试！')

    def download(self, m3u8_url, title, num, head):
        ts_obj = 'https:(.*?)png'
        try:
            print('正在解析...')
            play_list = requests.get(url=m3u8_url, headers=self.headers_yh, timeout=20).text
            if not os.path.exists(f'./{title}'):
                os.mkdir(f'./{title}')
            if not os.path.exists(f'./{title}{num}缓存文件夹'):
                os.mkdir(f'./{title}{num}缓存文件夹')
            if 'EXTINF' in play_list:
                if not os.path.exists(f'./{title}'):
                    os.mkdir(f'./{title}')
                ts_url_list = re.findall(ts_obj, play_list)
                print('1')
                print(len(ts_url_list))
                if len(ts_url_list) <= 1000:
                    a = 30
                else:
                    a = 50
                with ThreadPoolExecutor(max_workers=a) as pool1:
                    for pool_num in range(0, len(play_list)):
                        pool1.submit(acg.png_thread_download, ts_url_list, title, num, pool_num)
                    pool1.shutdown()
                    print('下载完成')
                os.system(f'cd ./{title}{num}缓存文件夹 && copy /b *.ts video.mp4')
                shutil.move(f'./{title}{num}缓存文件夹/video.mp4', f'./{title}/{title}{num}.mp4')
                shutil.rmtree(f'./{title}{num}缓存文件夹')
            else:
                playlist = acg.get_true_play_list(m3u8_url, head)
                print('2')
                print(len(playlist))
                if len(playlist) <= 1000:
                    a = 30
                else:
                    a = 50
                with ThreadPoolExecutor(max_workers=a) as pool2:
                    for pool_num in range(0, len(playlist)):
                        pool2.submit(acg.thread_download, playlist, title, num, pool_num, head)
                    pool2.shutdown()
                    print('下载完成')
                os.system(f'cd ./{title}{num}缓存文件夹 && copy /b *.ts video.mp4')
                key = acg.get_key(m3u8_url, head)
                acg.boom(f'./{title}{num}缓存文件夹/video.mp4', f'./{title}/{title}{num}.mp4', key, title, num)
                shutil.rmtree(f'./{title}{num}缓存文件夹')
        except Exception as error:
            pass


b1 = bilibili_video_get()
b2 = bilibili_collection_video_get()
acg = yinhua()


def back():
    f1.pack_forget()
    f2.pack(fill='both', expand=True)


def part():
    f2.pack_forget()
    f1.pack(fill='both', expand=True)


def num_list_get():
    if en1.get() != '':
        if not os.path.exists(f'./{b2.get_title(en1.get())}'):
            os.mkdir(f'./{b2.get_title(en1.get())}')
        path = f'./{b2.get_title(en1.get())}'
        num = len(l1.curselection())
        frist = list(l1.curselection())[0]
        if num <= 1:
            bv1.place_forget()
            Lb1.place(x=170, y=20)
            video_url = b2.video_url_get(en1.get(), frist, num)
            audio_url = b2.audio_url_get(en1.get(), frist, num)
            video_data = requests.get(url=video_url, headers=headers).content
            audio_data = requests.get(url=audio_url, headers=headers).content
            with open(f'./{path}/{frist + 1}.mp4', 'wb') as video:
                video.write(video_data)
            with open(f'./{path}/{frist + 1}.mp3', 'wb') as audio:
                audio.write(audio_data)
            Lb1.place_forget()
            bv1.place(x=160, y=20)
            messagebox.showinfo(title='提示', message=f'第{frist + 1}集下载完成！')
        else:
            bv1.place_forget()
            Lb1.place(x=170, y=20)
            video_url_list = b2.video_url_get(en1.get(), frist, num)
            audio_url_list = b2.audio_url_get(en1.get(), frist, num)
            n = frist + 1
            for i in range(0, num):
                video_url = video_url_list[i]
                audio_url = audio_url_list[i]
                video_data = requests.get(url=video_url, headers=headers).content
                audio_data = requests.get(url=audio_url, headers=headers).content
                with open(f'./{path}/{n}.mp4', 'wb') as video:
                    video.write(video_data)
                with open(f'./{path}/{n}.mp3', 'wb') as audio:
                    audio.write(audio_data)
                messagebox.showinfo(title='提示', message=f'第{n}集下载完成！')
                n += 1
            i += 1
            Lb1.place_forget()
            bv1.place(x=160, y=20)
    else:
        messagebox.showerror(title='错误', message='BV号不能为空！')


def part_title_get():
    l1.delete(first=0, last=END)
    if en1.get() != '':
        a = b2.get_part_title(en1.get())
        for part_title in a:
            l1.insert(END, part_title)
    else:
        messagebox.showerror(title='错误', message='BV号不能为空！')


def download():
    if en2.get() != '':
        bv2.place_forget()
        Lb2.place(x=100, y=20)
        b1.download(b1.video_url_get(en2.get()), b1.audio_url_get(en2.get()))
        Lb2.place_forget()
        messagebox.showinfo(title='提示', message='下载完成!')
        bv2.place(x=80, y=18)
    else:
        messagebox.showerror(title='错误', message='BV号不能为空！')


def video_download():
    if en2.get() != '':
        bv2.place_forget()
        Lb2.place(x=100, y=20)
        b1.video_download(b1.video_url_get(en2.get()))
        messagebox.showinfo(title='提示', message='下载完成!')
        Lb2.place_forget()
        bv2.place(x=80, y=18)
    else:
        messagebox.showerror(title='错误', message='BV号不能为空！')


def audio_download():
    if en2.get() != '':
        bv2.place_forget()
        Lb2.place(x=100, y=20)
        b1.audio_download(b1.audio_url_get(en2.get()))
        messagebox.showinfo(title='提示', message='下载完成!')
        Lb2.place_forget()
        bv2.place(x=80, y=18)
    else:
        messagebox.showerror(title='错误', message='BV号不能为空！')


def update():
    global img_src
    f2.pack_forget()
    f3 = Frame(root, bg='#cdc1ef')
    f3.pack(fill='both', expand=True)
    l_up = Label(f3, fg='red', bg='#cdc1ef', text='正在生成二维码', font=('黑体', 20))
    l_up.pack(anchor='center', pady=90)
    params = {
        'data': 'https://github.com/GC-Ruth/bilibili',
        'size': 4
    }
    QRapi = 'https://api.wrdan.com/qr'
    QR_image = requests.get(url=QRapi, params=params, headers=headers).content
    with open('./update.png', 'wb') as QR:
        QR.write(QR_image)
    img_src = PhotoImage(file='./update.png')
    l_up.pack_forget()
    Label(f3, image=img_src).pack()
    Label(f3, fg='red', bg='#cdc1ef', text='网页无法打开请使用加速器', font=('黑体', 10)).pack(side='bottom',
                                                                                               anchor='center')
    Button(f3, text='返回', font=('黑体', 20),
           command=lambda: [f3.pack_forget(), f2.pack(fill='both', expand=True), os.remove('./update.png')]).place(
        x=160, y=180)


def animation():
    os.system('start http://www.yinghua8.com/japan/')
    f2.pack_forget()
    Facg = Frame(root, bg='#cdc1ef')
    Facg.pack(fill='both', expand=True)
    en3 = Entry(Facg, width=40)
    en3.place(x=100, y=50)
    Label(Facg, text='粘贴网址', font=('黑体', 12), bg='#cdc1ef').place(x=20, y=50)
    Button(Facg, text='开始下载', font=('黑体', 25), bg='#cdc1ef', command=lambda: thread(acg_download)).place(x=120,y=120)
    Button(Facg, text='返回', font=('黑体', 20), bg='#cdc1ef', command=lambda: [Facg.pack_forget(),f2.pack(fill='both', expand=True)]).place(x=160, y=185)

    def acg_download():
        try:
            url = en3.get()
            l1 = Label(Facg, text='正在下载', font=('黑体', 18), bg='#cdc1ef', fg='red')
            l1.place(x=150, y=75)
            pool = ThreadPoolExecutor(max_workers=10)
            m3u8_url = pool.submit(acg.url_get, url)
            title = pool.submit(acg.title, url)
            head = pool.submit(acg.get_head, acg.url_get(url))
            num = pool.submit(acg.num, url)
            m3u8_url = m3u8_url.result()
            head = head.result()
            title = title.result()
            title = title.replace(':', '：')
            num = num.result()
            acg.download(m3u8_url, title, num, head)
            messagebox.showinfo(title='提示', message='下载完成！！！')
            l1.place_forget()
        except Exception as error:
            l1.place_forget()
            messagebox.showerror(title='错误', message=error)


def thread(func):
    t = threading.Thread(target=func)
    t.setDaemon(True)
    t.start()


root = Tk()
root.title('B站视频下载器')
root.attributes('-alpha', 0.95)
root.geometry('400x250+400+300')
f1 = Frame(root, bg='#cdc1ef')
en1 = Entry(f1)
en1.place(x=244, y=20)
bv1 = Label(f1, text='输入BV号', font=('黑体', 14), bg='#cdc1ef')
bv1.place(x=158, y=18)
l1 = Listbox(f1, selectmode=EXTENDED, width=30, bd=2, bg='#b3dff7')
l1.place(x=172, y=50)
s = Scrollbar(l1, relief='raised')
l1.config(yscrollcommand=s.set)
s.config(command=l1.yview)
s.place(x=197, y=0, height=181, width=14)
Lb1 = Label(f1, text='正在下载中...', fg='red', bg='#cdc1ef')
Label(f1, text='合集下载模式', font=('黑体', 16), fg='red', relief='groove').place(x=14, y=16)
Button(f1, text='点击查询', bg='#8c98b0', width=18, height=2, command=lambda: thread(part_title_get)).place(x=15, y=60)
Button(f1, text='下载选中', bg='#8c98b0', width=18, height=2, command=lambda: thread(num_list_get)).place(x=15, y=120)
Button(f1, text='返回', bg='#8c98b0', width=18, height=2, command=lambda: thread(back)).place(x=15, y=180)
f2 = Frame(root, bg='#cdc1ef')
f2.pack(fill='both', expand=True)
Lb2 = Label(f2, text='正在下载中...', fg='red', bg='#cdc1ef')
bv2 = Label(f2, text='输入BV号', bg='#cdc1ef', font=('黑体', 15))
bv2.place(x=80, y=18)
en2 = Entry(f2)
en2.place(x=180, y=20)
Button(f2, text='下载视频', bg='#8c98b0', width=18, height=2, command=lambda: thread(video_download)).place(x=40, y=60)
Button(f2, text='下载音频', bg='#8c98b0', width=18, height=2, command=lambda: thread(audio_download)).place(x=40, y=120)
Button(f2, text='合集下载', bg='#8c98b0', width=18, height=2, command=lambda: thread(part)).place(x=40, y=180)
Button(f2, text='下载视频音频', bg='#8c98b0', width=18, height=2, command=lambda: thread(download)).place(x=220, y=59)
Button(f2, text='樱花动漫下载', bg='#8c98b0', width=18, height=2, command=lambda: thread(animation)).place(x=220, y=119)
Button(f2, text='检查更新', bg='#8c98b0', width=18, height=2, command=lambda: thread(update)).place(x=220, y=179)
root.mainloop()
