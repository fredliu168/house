# -*- coding: utf-8 -*-
# 配置文件
# 2018.3.13

import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    g_room_img_dir = '{}/static/images/room'.format(basedir)  # 保存房产图片的路径
    g_avatar_dir = '{}/static/images/avatar'.format(basedir)  # 保存头像路径
    g_default_room_dir = '{}/static/images/default_room.jpg'.format(basedir)  # 默认房屋图片
    g_default_avatar_dir = '{}/static/images/default_avatar.jpg'.format(basedir)  # 默认用户头像图片
    # 标题栏图片
    g_banner_dir = '{}/static/images/banner/banner.png'.format(basedir)
    # 获取资源文件
    g_source_img_dir = '{}/static/images/source'.format(basedir)

    # mysql
    mysql_passwd = 'house'
    mysql_db = 'fred123456'
    mysql_user = 'root'
    mysql_host = '127.0.0.1'
    mysql_port = 3306

    @staticmethod
    def init_app(app):
        pass


class ProductionConfig(Config):
    pass


config = {'default': ProductionConfig}
