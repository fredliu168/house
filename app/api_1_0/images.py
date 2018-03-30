# -*- coding: utf-8 -*-
# 图片数据
# 20180330
from flask import Flask, Response, jsonify,current_app
import re
from app import scrapy_rent_house
from app import util
from app import scrapy_house
from app.model.room import *
from . import api


@api.route("/source/<image_name>")
def source_img(image_name):
    # 获取资源文件

    img_local_path = "{}/{}".format(current_app.config['SOURCE_IMG_DIR'], image_name)

    img_stream = ''

    print(img_local_path)

    with open(img_local_path, 'rb') as img_f:
        img_stream = img_f.read()

    resp = Response(img_stream, mimetype="image/jpeg")
    return resp


@api.route("/banner")
def banner():
    # 返回标题图片
    img_local_path = "{}".format(current_app.config['BANNER_DIR'])

    img_stream = ''

    print(img_local_path)

    with open(img_local_path, 'rb') as img_f:
        img_stream = img_f.read()

    resp = Response(img_stream, mimetype="image/jpeg")
    return resp


@api.route("/image/<imageid>")
def room_image(imageid):
    """
    返回房间的图片
    :param imageid:
    :return:
    """
    if imageid == 'default':  # 设置默认图片
        img_local_path = current_app.config['DEFAULT_ROOM_DIR']
    else:

        ret = dbManager.exec_sql("select path from image where name='{name}'".format(name=imageid))
        img_local_path = "{}/{}".format(current_app.config['ROOM_IMG_DIR'], ret[0]['path'])

    img_stream = ''

    print(img_local_path)

    with open(img_local_path, 'rb') as img_f:
        img_stream = img_f.read()

    resp = Response(img_stream, mimetype="image/jpeg")
    return resp


@api.route("/avatar/<imageid>")
def avatar(imageid):
    """
    返回头像
    :param imageid:
    :return:
    """
    if imageid == 'default' or imageid == 'null':  # 设置默认图片
        img_local_path = current_app.config['DEFAULT_AVATAR_DIR']
    else:
        img_local_path = "{}/{}".format(current_app.config['AVATAR_DIR'], imageid)

    print(img_local_path)
    img_stream = ''
    with open(img_local_path, 'rb') as img_f:
        img_stream = img_f.read()

    resp = Response(img_stream, mimetype="image/jpeg")
    return resp
