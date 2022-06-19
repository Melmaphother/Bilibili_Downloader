import bilibili_video_download
import comment_part
import otherinfo
import comment_all
from PyQt5 import QtCore, QtWidgets, QtGui
# from PyQt5.Qt import *
from PyQt5.QtWidgets import QMessageBox
import sys
import GUI
# import bilibili_video_download_GUI
import bullet_screen
import image_Spider

class mainwindow(object):
    def __init__(self):
        app = QtWidgets.QApplication(sys.argv)
        MainWindow = QtWidgets.QMainWindow()
        self.ui = GUI.Ui_widget()
        self.ui.setupUi(MainWindow)

        self.ui.pushButton.clicked.connect(self.Video)
        self.ui.pushButton_6.clicked.connect(self.Barrage)
        self.ui.pushButton_7.clicked.connect(self.Comment)
        self.ui.pushButton_2.clicked.connect(self.All_comment)
        self.ui.pushButton_3.clicked.connect(self.Cover)
        self.ui.pushButton_4.clicked.connect(self.VideoInfo)

        MainWindow.show()
        sys.exit(app.exec_())


    def Video(self):
        # 调用下载视频程序
        bv = self.ui.lineEdit.text()
        quality = self.ui.comboBox_7.currentText()
        if quality == '1080p':
            quality = 80
        if quality == '720p':
            quality = 64
        if quality == '480p':
            quality = 32
        if quality == '360p':
            quality = 16
        if bv:
            msg_box = QMessageBox(QMessageBox.Information, '提示', '点下OK，下好告诉你\n   死机也别着急')
            msg_box.exec_()
            bilibili_video_download.download(bv,quality)
        else:
            msg_box = QMessageBox(QMessageBox.Information, '提示', '请输入BV号或视频链接')
            msg_box.exec_()


    def Barrage(self):
        # 获取参数
        bv = self.ui.lineEdit.text()
        page = self.ui.lineEdit_2.text()
        img_path = self.ui.lineEdit_3.text()
        width = self.ui.comboBox.currentText()
        height = self.ui.comboBox_2.currentText()
        min_font_size = self.ui.comboBox_3.currentText()
        max_font_size = self.ui.comboBox_4.currentText()
        max_words = self.ui.comboBox_5.currentText()
        background_color = self.ui.comboBox_6.currentText()
        font = self.ui.comboBox_8.currentText()
        # 字体类型对应参数转换

        # 背景颜色对应参数转换
        if background_color == '黑色':
            background_color = 'black'
        if background_color == '白色':
            background_color = 'white'
        if background_color == '粉色':
            background_color = 'pink'
        if background_color == '红色':
            background_color = 'red'
        if background_color == '橙色':
            background_color = 'orange'
        if background_color == '黄色':
            background_color = 'yellow'
        if background_color == '绿色':
            background_color = 'green'
        if background_color == '蓝色':
            background_color = 'blue'
        if background_color == '紫色':
            background_color = 'purple'

        if bv and int(page) > 0 and img_path:
            if bv[0:2] != 'BV':  # 若传入网址 截取BV号
                bv = bv[bv.index('BV') : bv.index('BV') + 12]
            url = 'https://www.bilibili.com/video/'+bv
            if bullet_screen.run(bv, url, page, img_path, width, height, min_font_size, max_font_size, max_words, background_color,font):
                msg_box = QMessageBox(QMessageBox.Information, '提示', '弹幕和词云已经下载到软件目录下')
                msg_box.exec_()
            else:
                msg_box = QMessageBox(QMessageBox.Critical, '提示', '视频无弹幕')
                msg_box.exec_()
        else:
            msg_box = QMessageBox(QMessageBox.Information, '提示', '   信息输入有误\n视频序号错了吗？\n信息输入完整吗？')
            msg_box.exec_()

    def Comment(self):
        # 获取参数
        bv = self.ui.lineEdit.text()
        pages_1 = self.ui.lineEdit_5.text()
        pages_2 = self.ui.lineEdit_6.text()
        # 转换为BV号
        if bv and int(pages_1) > 0 and int(pages_2) >=0:
            if bv[0:2] != 'BV':  # 若传入网址 截取BV号
                bv = bv[bv.index('BV') : bv.index('BV') + 12]
            msg_box = QMessageBox(QMessageBox.Information, '提示', '点下OK，下好告诉你\n   死机也别着急')
            msg_box.exec_()
            # 调用下载评论程序 下载完成提示
            if comment_part.run(bv, pages_1, pages_2):
                msg_box = QMessageBox(QMessageBox.Information, '提示', '评论已经下载到软件目录下')
                msg_box.exec_()
            else:
                msg_box = QMessageBox(QMessageBox.Critical, '错误', '下载错误')
                msg_box.exec_()
        else:
            msg_box = QMessageBox(QMessageBox.Information, '信息输入错误', '     请输入BV或网址\n    评论页数要大于‘0’\n评论回复页数不小于‘0’')
            msg_box.exec_()


    def All_comment(self):
        # 获取参数
        bv = self.ui.lineEdit.text()
        if bv:
            msg_box = QMessageBox(QMessageBox.Information, '提示', '点下OK，下好告诉你\n   死机也别着急')
            msg_box.exec_()
            if comment_all.main(bv):
                msg_box = QMessageBox(QMessageBox.Information, '提示', '所有评论已经下载到软件目录下')
                msg_box.exec_()
            else:
                msg_box = QMessageBox(QMessageBox.Critical, '错误', '下载错误')
                msg_box.exec_()
        else:
            msg_box = QMessageBox(QMessageBox.Information, '提示', '请输入BV号或网址')
            msg_box.exec_()


    def Cover(self):
        bv = self.ui.lineEdit.text()
        if bv:
            if bv[0:2] != 'BV':  # 若传入网址 截取BV号
                bv = bv[bv.index('BV'): bv.index('BV') + 12]
            if image_Spider.request_download(bv):
                msg_box = QMessageBox(QMessageBox.Information, '提示', '封面已下载到软件目录下')
                msg_box.exec_()
            else:
                msg_box = QMessageBox(QMessageBox.Critical, '错误', '下载错误')
                msg_box.exec_()
        else:
            msg_box = QMessageBox(QMessageBox.Information, '提示', '请输入BV号或视频链接')
            msg_box.exec_()


    def VideoInfo(self):
        bv = self.ui.lineEdit.text()
        if bv:
            if bv[0:2] != 'BV':  # 若传入网址 截取BV号
                bv = bv[bv.index('BV'): bv.index('BV') + 12]
            infodict = otherinfo.otherInfo(bv)
            self.ui.lineEdit_7.setText(infodict['bvid'])
            self.ui.lineEdit_8.setText(str(infodict['view']))
            self.ui.lineEdit_9.setText(str(infodict['danmuku_num']))
            self.ui.lineEdit_10.setText(str(infodict['reply_num']))
            self.ui.lineEdit_11.setText(str(infodict['favorite_num']))
            self.ui.lineEdit_12.setText(str(infodict['coin_num']))
            self.ui.lineEdit_13.setText(str(infodict['share_num']))
            self.ui.lineEdit_14.setText(str(infodict['like_num']))
        else:
            msg_box = QMessageBox(QMessageBox.Information, '提示', '请输入BV号或视频链接')
            msg_box.exec_()


if __name__ == "__main__":
    mainwindow()