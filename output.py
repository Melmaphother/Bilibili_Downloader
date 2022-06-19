import os,sys

def creat(path):
    folder = os.path.exists(path)
    if not folder:  # 判断是否存在文件夹如果不存在则创建为文件夹
        os.makedirs(path)  # makedirs 创建文件时如果路径不存在会创建这个路径
        print("---  new folder...  ---")
        print("---  OK  ---")
    else:
        print("---  There is this folder!  ---")

def file_setup(bv,classification):
    path = os.path.join(os.path.dirname(sys.executable), 'output' , bv ,classification)
    creat(path)
    print("爬取的内容所在目录为：" + path)
    return path     #返回路径
