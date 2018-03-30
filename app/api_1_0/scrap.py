# -*- coding: utf-8 -*-
# 抓取数据
# 20180330
from flask import Flask, Response, jsonify,current_app
import re
from app import scrapy_rent_house
from app import util
from app import scrapy_house
from app.model.room import *
from . import api


@api.route("/scrap/sell-room")
def scrap_house():
    # 抓取更新房产数据
    result = {"code": 10000, "value": "", "msg": "抓取销售楼盘成功"}

    houseScrap = scrapy_house.HouseScrap()
    try:
        houseScrap.srcap()

    except ValueError as err:
        result['msg'] = "抓取销售楼盘错误:{}".format(err)
        result['code'] = -10000

    return result


@api.route("/scrap/rent-room")
def scrap_rent_house():
    # 抓取更新房产数据
    result = {"code": 10000, "value": "", "msg": "抓取租房成功"}

    rent_house = scrapy_rent_house.RentHouseScrap()

    try:
        rent_house.scrap()
    except ValueError as err:
        result['msg'] = "抓取销售楼盘错误:{}".format(err)
        result['code'] = -10000

    return result
