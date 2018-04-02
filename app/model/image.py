# -*- coding: utf-8 -*-
# 图片类
# 20180313

import json
import os

import requests
from flask import current_app

from app import util
from .. import dbManager


class RoomImage():

    def __init__(self):
        self.room_sha_identity = ''  # 房屋sha_identity外键
        self.name = ''  # 图片名称
        self.post_time = ''  # 上传照片时间
        self.path = ''  # 图片存放路径
        self.url= ''

    def _fetch(self):
        # 保存房产图片到本地目录

        url_path, img_name = os.path.split(self.name)
        room_img_name = "{image_name}.{type}".format(image_name=util.MD5(self.name), type=img_name.split('.')[1])
        # 保存图像到本地
        image_save_path = '{}/{}/{}'.format(current_app.config['ROOM_IMG_DIR'], self.post_time.split(' ')[0], room_img_name)
        # 创建保存路径
        util.mkdir('{}/{}'.format(current_app.config['ROOM_IMG_DIR'], self.post_time.split(' ')[0]))

        self.url = self.name
        ret = requests.get(self.name)

        if ret.status_code == 200:
            with open(image_save_path, 'wb') as file:
                file.write(ret.content)
            self.name = room_img_name
            self.path = "{}/{}".format(self.post_time.split(' ')[0], room_img_name)
            return True

        self.name = ''
        return False

    def _saveDb(self):
        # 保存内容到数据库
        dbManager.insert('image', insert_data=[
            {"room_sha_identity": self.room_sha_identity, "name": self.name, "post_time": self.post_time,
             "path": self.path,"url":self.url}])

    def save(self):
        # 把图片保存本地,相关字段保存到数据库
        self._fetch()
        self._saveDb()

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)


if __name__ == '__main__':
    roomImage = RoomImage()

    roomImage.post_time = '2018-03-13 08:50:00'
    roomImage.name = "https://att.dehuaca.com/house/201803/05/105924f4o3on9n4i56t496.jpg"
    roomImage.room_sha_identity = '841e61348cc394645fd19d6f65621f6b'

    # name = roomImage._fetch()
    # roomImage._saveDb()

    roomImage.save()

    # print(name)

    # post_time = '2018-03-13 08:50:00'
    #
    # date_post_time = datetime.datetime.strptime(post_time, '%Y-%m-%d %H:%M:%S')
    #
    # post_time = date_post_time.strftime('%Y-%m-%d')
    #
    # print(post_time)
