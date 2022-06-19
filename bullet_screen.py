import requests
import re
import jieba
import wordcloud
import time
import sys
import os
from bs4 import BeautifulSoup

import output

class Bilibili:
    def __init__(self, bv, videourl, page, img_path):
        self.bv = bv
        self.page = page
        self.img_path = img_path
        self.baseurl = videourl.split('?')[0]
        self.videourl = videourl
    # 爬取弹幕和评论
    def getAidAndCid(self):
        cidurl = self.baseurl + "?p=" + self.page
        cidRegx = '{"cid":([\d]+),"page":%s,' % (self.page)
        aidRegx = '"aid":([\d]+),'
        r = requests.get(cidurl)
        r.encoding = 'utf-8'
        # try:

        self.cid = re.findall(cidRegx, r.text)[0]
        self.aid = re.findall(aidRegx, r.text)[int(self.page) - 1]
        # except:
        #     print('视频序号输入有误，请保证序号在1到最大值之间！')
        #     time.sleep(3)
        #     sys.exit()

    def getBarrage(self):
        # print('正在获取弹幕......')

        commentUrl = 'https://comment.bilibili.com/' + self.cid + '.xml'

        # 获取并提取弹幕 #
        r = requests.get(commentUrl)
        r.encoding = 'utf-8'
        content = r.text
        # 正则表达式匹配字幕文本
        comment_list = re.findall('>(.*?)</d><d ', content)
        # comment_path = os.path.join(sys.path[0], '{comment}.txt')
        # file_path = open(comment_path, 'w', encoding='utf-8')
        path = output.file_setup(self.bv, 'bullet_screen')
        file_path = open(os.path.join(path, f'Barrage of {self.bv}.txt'), 'w', encoding='utf-8')

        if len(comment_list):
            for i in range(1, len(comment_list)):
                file_path.write(str(i) + '. ' + comment_list[i] + '\n')
            del comment_list[0]
        else:
            return 0
        # jieba分词
        self.barrage = "".join(comment_list)
        return 1

    def getComment(self, x, y):
        for i in range(x, y + 1):
            r = requests.get(
                'https://api.bilibili.com/x/v2/reply?pn={}&type=1&oid={}&sort=2'.format(i, self.aid)).json()
            replies = r['data']['replies']
            print('------评论列表------')
            for repliy in replies:
                print(repliy['content']['message'] + '\n')

        pass

    def genWordCloud(self, width, height, min_font_size, max_font_size, max_words, background_color,fonts):
        # print('正在分词......')

        text = "".join(jieba.lcut(self.barrage))
        # 调用字体
        path1 = 'C:/Windows/Fonts/simkai.ttf'
        path2 = 'C:/Windows/Fonts/simhei.ttf'
        path3 = 'C:/Windows/Fonts/STHUPO.TTF'
        path4 = 'C:/Windows/Fonts/simfang.ttf'
        path5 = 'C:/Windows/Fonts/STXINGKA.TTF'
        Path = path1
        if fonts == '楷体':  # 楷体
            Path = path1
        if fonts == '黑体':  # 黑体
            Path = path2
        if fonts == '华文琥珀':  # 华文琥珀
            Path = path3
        if fonts == '仿宋':  # 仿宋
            Path = path4
        if fonts == '华文行楷':  # 华文行楷
            Path = path5
        # 实例化词云，
        wc = wordcloud.WordCloud(
            # 选择字体路径，没有选择的话，中文无法正常显示
            font_path=Path,
            width=int(width),
            height=int(height),
            min_font_size=int(min_font_size),
            max_font_size=int(max_font_size),
            max_words=int(max_words),
            background_color=background_color
        )
        # 文本中生成词云
        wc.generate(text)
        # 保存成图片
        path = output.file_setup(self.bv, 'bullet_screen')
        wc.to_file(os.path.join(path, self.img_path + '.jpg'))
        # wc.to_file(self.img_path + '.jpg')
        # print('词云生成完毕，图片名称：{}.jpg'.format(self.img_path))


def checkUrl(url):
    try:
        r = requests.get(url)
    except:
        return 0
    r.encoding = 'utf-8'
    # 视频名称正则表达式
    regx = '"part":"(.*?)"'
    r.encoding = 'utf-8'
    result = re.findall(regx, r.text)
    count = 0
    if len(result) > 0:
        print('------视频列表------')
        for i in result:
            count += 1
            print("视频" + str(count) + " : " + i)
        return 1
    return 0


def run(bv, url, page, img_path, width, height, min_font_size, max_font_size, max_words, background_color,font):
    # if checkUrl(videourl):


    # 计时
    start_time = time.time()

    # 实例化类
    b = Bilibili(bv,url, page, img_path)

    # 获取aid和cid
    b.getAidAndCid()

    # 获取弹幕
    barrage=b.getBarrage()
    if not barrage:
        return 0


    # 获取评论 起始页和结束页
    # b.getComment(1, 4)

    # 生成词云
    b.genWordCloud(width, height, min_font_size, max_font_size, max_words, background_color,font)

    return 1
    # print('程序运行完毕，耗时:{:.2f}s'.format(time.time() - start_time))
    # else:
    #     print('视频地址无效')
