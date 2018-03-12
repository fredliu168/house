
# 从德化网采集房产信息,存入数据库进行房价分析

> 2018.3.12

# 数据结构定义


使用mysql存储数据

## USER 发布用户信息

```py
    # 用户信息
    tel_phone       string(20)  # 联系方式 primary key
    user_name       string(64)  # 发布人信息
    password        string(256) # 用户登录密码
    user_name_type  string(10)  # 用户特征 个人/经纪人
    #
    ava_img_url     string(64)  # 用户头像信息 上传到qiniu,md5值
    user_verify     int  # 用户是否认证 0 未认证, 1 认证
    # 公司信息
    cop_name        string(200)  # 公司名称
    cop_addr        string(512) # 公司地址

```

## Room 房屋信息

```py
    # 发布用户信息
    tel_phone   string(20) # 用户联系方式,关联用户 外键
    title       string(256)  # 标题
    # 房间类型
    post_time   datetime  # 发布时间
    start_time  datetime  # 开始时间
    end_time    datetime  # 结束时间
    # 房屋信息
    price       float  # 价格
    area        float  # 面积
    floor       int  # 楼层
    total_floor int  # 总层高
    has_kitchen_bath bool  # 是否有厨卫
    has_property_five bool  # 产权是否满五年
    mark        string(10240) #其他描述信息
    # 房屋图片介绍
    images = []

```

# 实现步骤:

1.采集数据

2.录入数据库

3.数据展示

4.用户注册发布数据

5.用户认领,绑定采集的手机号码

