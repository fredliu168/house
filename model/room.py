# -*- coding: utf-8 -*-
# 房间类
# 20180313

import json


class Room():
    # 发布用户信息
    #user = User()
    sha_identity = '' #标识符md5(title+phone)
    title = ''  # 标题
    phone = '' # 联系电话
    # 房间类型
    post_time = ''  # 发布时间
    start_time = ''  # 开始时间
    end_time = ''  # 结束时间
    # 房屋信息
    house_name = '' # 楼盘名称
    config = '' #房屋配置
    position = '' #房屋地址位置

    price = 0  # 价格
    area = 0  # 面积
    floor = 0  # 楼层
    total_floor = 0  # 总层高
    has_kitchen_bath = 0  # 是否有厨卫
    five_year = 0  # 产权是否满五年
    mark = ''  # 其他描述信息
    # 房屋图片
    #images = []

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)

    def descript(self):
        #self.user.descript()
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
        #print(self.images)