import requests
import os
import output

# 爬虫地址
alphabet = 'fZodR9XQDSUm21yCkr6zBqiveYah8bt4xsWpHnJE7jL5VG3guMTKNPAwcF'
def dec(x):  # BV号转换成AV号
    r = 0
    for i, v in enumerate([11, 10, 3, 8, 4, 6]):
        r += alphabet.find(x[v]) * 58 ** i
    return (r - 0x2_0840_07c0) ^ 0x0a93_b324


def get_cover_url(bv_id):

	# bv_id = input('请输入bv号：')
	av_id = str(dec(bv_id))
	url = "https://www.bilibili.com/video/av" + av_id
	headers = {'Host': 'www.bilibili.com',
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36'}
	text = requests.get(url, headers=headers).text
	begin_index = text.find('itemprop=\"image\"') + len('itemprop=\"image\" content=\"')
	end_index = text.find('\"', begin_index)
	cover_url = text[begin_index:end_index]
	return cover_url

# IMAGE_URL = get_cover_url()

def request_download(bv):

	r = requests.get(get_cover_url(bv))
	path = output.file_setup(bv, 'image')
	with open(os.path.join(path, 'image.jpg'), 'wb') as f:
		f.write(r.content)
	return 1

# request_download()