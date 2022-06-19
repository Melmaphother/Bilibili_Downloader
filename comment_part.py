import requests
import urllib3
import time
import re
import sys
import os

import output


urllib3.disable_warnings()

hd = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36",
}

table = 'fZodR9XQDSUm21yCkr6zBqiveYah8bt4xsWpHnJE7jL5VG3guMTKNPAwcF'
tr = {}
for i in range(58):
    tr[table[i]] = i
s = [11, 10, 3, 8, 4, 6]
xor = 177451812
add = 8728348608

sleep_time = 2.1  # 访问网页间隔，防止IP被禁，若运行程序后出现无法访问网页版BILIBILI评论区的现象，等待2小时即可~_~!

def dec(x):
    r = 0
    for i in range(6):
        r += tr[x[s[i]]] * 58 ** i
    return (r - add) ^ xor

def get_oid(BV_CODE: str) -> str:

    return dec(BV_CODE)


def get_data(page: int, oid: str):
    time.sleep(sleep_time)  # 减少访问频率，防止IP封禁
    api_url = f"https://api.bilibili.com/x/v2/reply?jsonp=jsonp&pn={page}&type=1&oid={oid}&sort=2&_={int(time.time())}"
    # print(f'正在处理:{api_url}')  # 由于需要减缓访问频率，防止IP封禁，打印访问网址以查看访问进程
    r = requests.get(api_url, headers=hd, verify=False)
    r.raise_for_status()
    return r.json()['data']['replies'], r.json()['data']['page']['count']


def get_folded_reply(page: int, oid: str, root: int):
    time.sleep(sleep_time)  # 减少访问频率，防止IP封禁
    url = f'https://api.bilibili.com/x/v2/reply/reply?jsonp=jsonp&pn={page}&type=1&oid={oid}&ps=10&root={root}&_={int(time.time())}'
    # print(f'正在处理:{url}')  # 由于需要减缓访问频率，防止IP封禁，打印访问网址以查看访问进程
    r = requests.get(url, headers=hd, verify=False)
    r.raise_for_status()
    return r.json()['data']


def re_reply2(temp, root):
    _ = []
    for item in temp:
        if item[2] == root:
            _.append((item[1], 'FIRST'))
            continue
        for item2 in temp:
            if item[2] == item2[1]:
                _.append((item[1], item2[1]))
                break
        else:  # 回复对象被删除
            _.append((item[1], None))
    return _


def loop_folded_reply(root: int, rcount: int):
    temp = []
    temp2 = {}
    end_page = (rcount - 1) // 10 + 1 if (rcount-1) // 10 + 1 <= pages2 else pages2
    for page in range(1, end_page + 1):
        data = get_folded_reply(page, oid=oid, root=root)
        if not data['replies']:
            continue
        for item in data['replies']:
            mid = item['mid']
            rpid = item['rpid']
            parent = item['parent']
            dialog = item['dialog']
            rcount = item['rcount']
            like = item['like']
            ctime = item['ctime']
            name = item['member']['uname']
            # message = item['content']['message']
            message = re.sub(r'\t|\n|回复 @.*? :', '', item['content']['message'])
            # print(dialog, rpid, parent, name, message)
            temp.append([dialog, rpid, parent, name, message])
            temp2[rpid] = [mid, message, name, like, ctime]
        # else:
        #     break
    pointer = re_reply2(temp, root)

    def loop(pid, tab):
        # 用于递归查找单指
        for item in pointer:
            if pid == item[1]:
                mid, message, name, like, ctime = temp2[item[0]]
                f.write(
                    '|\t' * tab + f'|->\t点赞：{like}\t评论："{message}"\tUSER：{name}(UID：{mid})\t{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(ctime))}\n')
                loop(item[0], tab + 1)

    for rpid in [i for i, j in pointer if j == 'FIRST']:
        mid, message, name, like, ctime = temp2[rpid]
        f.write(
            f'|\t|->\t点赞：{like}\t评论："{message}"\tUSER：{name}(UID：{mid})\t{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(ctime))}\n')
        loop(rpid, tab=1)

    for ii, rpid in enumerate([i for i, j in pointer if not j]):
        if ii == 0:
            f.write(f'|\t|->\t评论已被删除\n')
        mid, message, name, like, ctime = temp2[rpid]
        f.write(
            f'|\t|\t|->\t点赞：{like}\t评论："{message}"\tUSER：{name}(UID：{mid})\t{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(ctime))}\n')
        loop(rpid, tab=3)


def get_reply(data, tab=0):
    if not data:
        return
    for item in data:
        mid = item['mid']
        rpid = item['rpid']
        count = item['count']
        rcount = item['rcount']
        like = item['like']
        ctime = item['ctime']
        name = item['member']['uname']
        message = re.sub(r'\t|\n|回复 @.*? :', '', item['content']['message'])
        f.write(
            '|\t' * tab + f'|->\t点赞：{like}\t评论："{message}"\tUSER：{name}(UID：{mid})\t{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(ctime))}\n')
        # print(f'处理评论:UID-{mid}\tUSER-{name}\t点赞-{like}')
        if 0 < rcount <= 3:
            get_reply(item['replies'], tab=1)
        elif rcount > 3:
            loop_folded_reply(root=rpid, rcount=rcount)


def run(bv, pages_1, pages_2):
    global pages1, pages2, f, oid
    pages1= int(pages_1)
    pages2 = int(pages_2)
    BV_CODE = bv  # 视频的BV号
    path = output.file_setup(bv , 'comment');
    f = open(os.path.join(path , f'Comment of {bv}.txt'), 'w', encoding='utf-8')
    oid = get_oid(BV_CODE)
    page = 1
    while True:
        try:
            data, reply_num = get_data(page, oid)
            get_reply(data)  # 遍历所有回复
            end_page = reply_num // 20 + 1 if reply_num // 20 + 1 <= pages1 else pages1
            if page == end_page:
                print('程序运行完毕')
                break
            page += 1
        except Exception as e:
            print('ERROR:', e)
            print('退出循环 结束')
            break
    f.close()
    return 1