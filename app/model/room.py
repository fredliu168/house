# -*- coding: utf-8 -*-
# 房间类
# 20180313

import json

from .. import dbManager

class BaseRoom(object):
    def __init__(self):
        self.sha_identity = ''  # 标识符md5(title+phone)
        self.title = ''  # 标题
        self.phone = ''  # 联系电话
        # 房间类型
        self.post_time = ''  # 发布时间
        self.start_time = ''  # 开始时间
        self.end_time = ''  # 结束时间
        # 房屋信息
        self.house_name = ''  # 楼盘名称
        self.config = ''  # 房屋配置
        self.position = ''  # 房屋地址位置

        self.price = 0  # 价格
        self.area = 0  # 面积
        self.floor = 0  # 楼层
        self.total_floor = 0  # 总层高
        self.has_kitchen_bath = 0  # 是否有厨卫
        self.mark = ''  # 其他描述信息

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)

    def descript(self):
        # self.user.descript()
        print(self.sha_identity)
        print(self.title)
        print(self.post_time)
        print(self.start_time)
        print(self.end_time)
        print(self.price)
        print(self.area)
        print(self.floor)
        print(self.total_floor)
        print(self.has_kitchen_bath)

        print(self.house_name)
        print(self.config)
        print(self.position)
        print(self.mark)


class RentRoom(BaseRoom):
    # 出租房屋信息
    def __init__(self):
        BaseRoom.__init__(self)
        self.rent_type = ''  # 出租方式
        self.url = '' # 采集的地址

    @staticmethod
    def save_room2db(rooms):
        # 把房产数据保存到数据库
        dbManager.insert('room', insert_data=rooms)

    def save(self):
        # 把房产数据保存到数据库
        rooms = []
        rooms.append(json.loads(self.toJSON()))
        return  dbManager.insert('rent_room', insert_data=rooms)

    def descript(self):
        BaseRoom.descript(self)
        print("rent_type:" + self.rent_type)

        # print(self.images)


class Room():
    # 发布用户信息
    # user = User()
    sha_identity = ''  # 标识符md5(title+phone)
    title = ''  # 标题
    phone = ''  # 联系电话
    # 房间类型
    post_time = ''  # 发布时间
    start_time = ''  # 开始时间
    end_time = ''  # 结束时间
    # 房屋信息
    house_name = ''  # 楼盘名称
    config = ''  # 房屋配置
    position = ''  # 房屋地址位置

    pre_price = 0  # 单价
    price = 0  # 价格
    area = 0  # 面积
    floor = 0  # 楼层
    total_floor = 0  # 总层高
    has_kitchen_bath = 0  # 是否有厨卫
    five_year = 0  # 产权是否满五年
    mark = ''  # 其他描述信息

    # 房屋图片
    # images = []

    @staticmethod
    def save_room2db(rooms):
        # 把房产数据保存到数据库
        dbManager.insert('room', insert_data=rooms)

    def save(self):
        # 把房产数据保存到数据库
        rooms = []
        rooms.append(json.loads(self.toJSON()))
        dbManager.insert('room', insert_data=rooms)

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)

    def descript(self):
        # self.user.descript()
        print(self.sha_identity)
        print(self.title)
        print(self.post_time)
        print(self.start_time)
        print(self.end_time)
        print(self.price)
        print(self.area)
        print(self.floor)
        print(self.total_floor)
        print(self.has_kitchen_bath)
        print(self.five_year)
        print(self.house_name)
        print(self.config)
        print(self.position)
        print(self.mark)
        # print(self.images)


if __name__ == '__main__':
    rent_room = RentRoom();

    rent_room.descript()
