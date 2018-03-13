# -*- coding: utf-8 -*-
# 图片类
# 20180313

import json
import os
import requests
import hashlib

g_room_img_dir = '' #保存房产图片的路径

def MD5(src):
    m = hashlib.md5()
    m.update(src.encode())
    return m.hexdigest()

class RoomImage():
    room_sha_identity = '' # 房屋sha_identity外键
    name = '' # 图片名称

    def save_image(url):
        # 保存房产图片

        url_path, img_name = os.path.split(url)
        avatar_name = "{image_name}.{type}".format(image_name=MD5(url), type=img_name.split('.')[1])

        # 保存头像到本地
        image_save_path = '{}/{}'.format(g_room_img_dir, avatar_name)

        ret = requests.get(url)

        if ret.status_code == 200:
            with open(image_save_path, 'wb') as file:
                file.write(ret.content)
            return avatar_name

        return ''

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)


