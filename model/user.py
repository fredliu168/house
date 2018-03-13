# -*- coding: utf-8 -*-
# 用户类
# 20180313


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

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)

    def descript(self):
        print(self.name)
        print(self.phone)
        print(self.user_type)
        print(self.avatar)
        print(self.verify)
        print(self.company_name)
        print(self.company_addr)