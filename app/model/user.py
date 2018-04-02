# -*- coding: utf-8 -*-
# 用户类
# 20180313
import json
import os
import requests
from app import util
from .. import dbManager
from .. import config
from flask import current_app

class User():
    # 用户信息
    name = ''  # 发布人信息
    phone = ''  # 联系方式
    user_type = 0  # 用户特征 个人/经纪人
    avatar = ''  # 用户头像信息md5值,内容存放到qiniu
    verify = 0  # 用户是否认证
    # 公司信息
    company_name = ''  # 公司名称
    company_addr = ''  # 公司地址

    def save_avatar(self,url):
        # 保存用户头像

        url_path, img_name = os.path.split(url)
        avatar_name = "{image_name}.{type}".format(image_name=util.MD5(url), type=img_name.split('.')[1])

        # 保存头像到本地
        image_save_path = '{}/{}'.format(current_app.config['AVATAR_DIR'], avatar_name)

        ret = requests.get(url)

        if ret.status_code == 200:
            with open(image_save_path, 'wb') as file:
                file.write(ret.content)
            return avatar_name

        return ''

    # @staticmethod
    # def save_user2db(users_dic):
    #     # 把数据保存到数据库
    #     insert_data = []
    #
    #     for user_dic in users_dic.values():
    #         #print(user_dic)
    #         user = User()
    #         util.dict2obj(user_dic, user)
    #         #print(user.avatar)
    #
    #         user.avatar = save_avatar(user.avatar)
    #         insert_data.append(json.loads(user.toJSON()))
    #
    #     dbManager.insert('user', insert_data=insert_data)

    def save(self):

        self.avatar = self.save_avatar(self.avatar)
        users = []
        users.append(json.loads(self.toJSON()))
        dbManager.insert('user', insert_data=users)

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)

    def descript(self):
        print(self.name)
        print(self.phone)
        print(self.user_type)
        print(self.avatar)
        print(self.verify)
        print("company_name:{}".format(self.company_name))
        print("company_addr:{}".format(self.company_addr))