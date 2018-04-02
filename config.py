# -*- coding: utf-8 -*-
# 配置文件
# 2018.3.13

import os

basedir = os.path.abspath(os.path.dirname(__file__))


# 注意 配置需要大写才能加到配置项里去 2018.3.30
class Config:
    image_dir = '{}/upload/images'.format(basedir)  # 图片的存储路径

    ROOM_IMG_DIR = '{}/room'.format(image_dir)  # 保存房产图片的路径
    AVATAR_DIR = '{}/avatar'.format(image_dir)  # 保存头像路径
    DEFAULT_ROOM_DIR = '{}/default_room.jpg'.format(image_dir)  # 默认房屋图片
    DEFAULT_AVATAR_DIR = '{}/default_avatar.jpg'.format(image_dir)  # 默认用户头像图片
    BANNER_DIR = '{}/banner/banner.jpg'.format(image_dir)
    # 获取资源文件
    SOURCE_IMG_DIR = '{}/source'.format(image_dir)

    # mysql
    DB_PWD = 'fred123456'
    DB_DATABASE = 'house'
    DB_USER = 'root'
    DB_HOST = '127.0.0.1'
    DB_PORT = 3306

    @staticmethod
    def init_app(app):
        pass


class DockerConfig(Config):
    DB_HOST = 'mysql'

    # mysqlserver

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)


class ProductionConfig(Config):
    @classmethod
    def init_app(cls, app):
        Config.init_app(app)


config = {'docker': DockerConfig,
          'default': ProductionConfig}
