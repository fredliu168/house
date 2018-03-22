# -*- coding: utf-8 -*-
# 提供数据接口
# 2018.3.14

from flask import Flask, Response, jsonify
import datetime
from mysql_db.mysql import *
import util
import config
from  model.room import *
import re


class MyResponse(Response):
    @classmethod
    def force_type(cls, response, environ=None):
        if isinstance(response, (list, dict)):
            response = jsonify(response)
        return super(Response, cls).force_type(response, environ)


app = Flask(__name__)
app.response_class = MyResponse


@app.route("/source/<image_name>")
def source_img(image_name):
    # 获取资源文件

    img_local_path = "{}/{}".format(config.g_source_img_dir, image_name)

    img_stream = ''

    print(img_local_path)

    with open(img_local_path, 'rb') as img_f:
        img_stream = img_f.read()

    resp = Response(img_stream, mimetype="image/jpeg")
    return resp


@app.route("/banner")
def banner():
    # 返回标题图片
    img_local_path = "{}".format(config.g_banner_dir)

    img_stream = ''

    print(img_local_path)

    with open(img_local_path, 'rb') as img_f:
        img_stream = img_f.read()

    resp = Response(img_stream, mimetype="image/jpeg")
    return resp


@app.route("/image/<imageid>")
def room_image(imageid):
    """
    返回房间的图片
    :param imageid:
    :return:
    """
    if imageid == 'default':  # 设置默认图片
        img_local_path = config.g_default_room_dir
    else:

        ret = dbManager.exec_sql("select path from image where name='{name}'".format(name=imageid))
        img_local_path = "{}/{}".format(config.g_room_img_dir, ret[0]['path'])

    img_stream = ''

    print(img_local_path)

    with open(img_local_path, 'rb') as img_f:
        img_stream = img_f.read()

    resp = Response(img_stream, mimetype="image/jpeg")
    return resp


@app.route("/avatar/<imageid>")
def avatar(imageid):
    """
    返回头像
    :param imageid:
    :return:
    """
    if imageid == 'default' or imageid == 'null':  # 设置默认图片
        img_local_path = config.g_default_avatar_dir
    else:
        img_local_path = "{}/{}".format(config.g_avatar_dir, imageid)

    print(img_local_path)
    img_stream = ''
    with open(img_local_path, 'rb') as img_f:
        img_stream = img_f.read()

    resp = Response(img_stream, mimetype="image/jpeg")
    return resp


@app.route("/rent-room/<sha_identity>")
def get_rent_room_detail(sha_identity):
    # 获取租赁信息
    result = {"code": 10000, "value": "", "msg": ""}
    sql = """
        select r.id,area, sha_identity,title,price,r.phone,r.post_time,start_time,end_time,house_name,position,floor,total_floor,has_kitchen_bath,lobby,live_room,orientation,
    r.type,mark,name,u.type as utype,avatar,verify,company_name,company_addr  from rent_room r left join user u on
    r.phone = u.phone where sha_identity = '{sha_identity}'
        """.format(sha_identity=sha_identity)

    print(sql)

    room = dbManager.exec_sql(sql)[0]

    # print(room[0])

    obj_room = Room()
    util.dict2obj(room, obj_room)

    image_sql = "select name from image i where i.room_sha_identity ='{room_sha_identity}'".format(
        room_sha_identity=obj_room.sha_identity)

    room['post_time'] = obj_room.post_time.strftime('%Y-%m-%d')
    room['start_time'] = obj_room.start_time.strftime('%Y-%m-%d')
    room['end_time'] = obj_room.end_time.strftime('%Y-%m-%d')

    if obj_room.company_name != None and len(obj_room.company_name) > 10:
        room['company_name'] = obj_room.company_name[:10] + '...'

    # print("room['company_name']:" + room['company_name'])
    if room['company_name'] == None:
        room['company_name'] = ''

    ret = dbManager.exec_sql(image_sql)

    room['image'] = ret

    print(room)

    result["value"] = room
    result["msg"] = "获取数据成功"

    return result


@app.route("/room/<sha_identity>")
def get_room_detail(sha_identity):
    result = {"code": 10000, "value": "", "msg": ""}
    sql = """
    select r.id,area, sha_identity,title,price,r.phone,r.post_time,start_time,end_time,house_name,position,
pre_price,floor,total_floor,has_kitchen_bath,five_year,lobby,live_room,orientation,
r.type,mark,name,u.type as utype,avatar,verify,company_name,company_addr  from room r left join user u on 
r.phone = u.phone where sha_identity = '{sha_identity}'
    """.format(sha_identity=sha_identity)

    # print(sql)

    room = dbManager.exec_sql(sql)[0]

    # print(room[0])

    obj_room = Room()
    util.dict2obj(room, obj_room)

    image_sql = "select name from image i where i.room_sha_identity ='{room_sha_identity}'".format(
        room_sha_identity=obj_room.sha_identity)

    room['post_time'] = obj_room.post_time.strftime('%Y-%m-%d')
    room['start_time'] = obj_room.start_time.strftime('%Y-%m-%d')
    room['end_time'] = obj_room.end_time.strftime('%Y-%m-%d')

    if obj_room.company_name!= None and len(obj_room.company_name) > 10:
        room['company_name'] = obj_room.company_name[:10] + '...'

    #print("room['company_name']:" + room['company_name'])
    if room['company_name'] == None:
        room['company_name'] = ''

    ret = dbManager.exec_sql(image_sql)

    room['image'] = ret

    # print(room)

    result["value"] = room
    result["msg"] = "获取数据成功"

    return result


def get_rent_house(sql, page):
    print(sql)
    result = {"code": 10000, "value": "", "msg": ""}

    if page <= 0:
        result = {"code": -10000, "value": "", "msg": "page 必须大于0"}
        return result

    rooms = dbManager.exec_sql(sql)

    for room in rooms:
        # print(room)
        obj_room = Room()
        util.dict2obj(room, obj_room)
        # print(obj_room.phone)
        image_sql = "select name from image i where i.room_sha_identity ='{room_sha_identity}'".format(
            room_sha_identity=obj_room.sha_identity)

        # print(user_sql)
        if len(obj_room.title) > 32:
            room['title'] = obj_room.title[:32] + '...'

        room['post_time'] = obj_room.post_time.strftime('%Y-%m-%d')
        room['start_time'] = obj_room.start_time.strftime('%Y-%m-%d')
        room['end_time'] = obj_room.end_time.strftime('%Y-%m-%d')

        # print("room['company_name']:"+room['company_name'])
        if room['company_name'] == None:
            room['company_name'] = ''

        ret = dbManager.exec_sql(image_sql)
        #
        # print(ret)
        #
        room['image'] = ret

    result["value"] = rooms
    result["msg"] = "获取数据成功"

    return result


@app.route("/rent-cond-house/<orderby>/<int:page>")
def rent_house_orderby(orderby, page):
    # 对租房信息进行排序 orderby = '1_1_1_1'
    # 第1个条件 1-5
    # {'id': 1, 'text': '价格从低到高'},
    # {'id': 2, 'text': '价格从高到低'},
    # {'id': 3, 'text': '面积从小到大'},
    # {'id': 4, 'text': '面积从大到小'},
    # {'id': 5, 'text': '发布时间'}
    # 第2个条件 1-4
    # {'id': 1, 'text': '1000元以下'},
    # {'id': 2, 'text': '1000元-2000元'},
    # {'id': 3, 'text': '2000元-3000元'},
    # {'id': 4, 'text': '3000元以上'}
    # 第3个条件 1-4
    # {'id': 1, 'text': '一房'},
    # {'id': 2, 'text': '两房'},
    # {'id': 3, 'text': '三房'},
    # {'id': 4, 'text': '四房'},
    # 第4个条件 1-3
    # {'id': 1, 'text': '住宅'},
    # {'id': 2, 'text': '商铺'},
    # {'id': 3, 'text': '写字楼'},

    condition = [
        {'0': '', '1': 'price < 1000', '2': 'price >= 1000 and price < 2000', '3': 'price >= 2000 and price < 3000',
         '4': 'price >= 3000 '},
        {'0': '', '1': 'live_room="一间"', '2': 'live_room="二间"', '3': 'live_room="三间"', '4': 'live_room="四间"'},
        {'0': '', '1': 'r.type=\"住宅\"', '2': 'r.type="商铺"', '3': 'r.type=\"写字楼\"'}]

    order_dic = {'0': '', '1': 'price', '2': 'price DESC', '3': 'area', '4': 'area DESC', '5': 'post_time'}

    # orderby = '1_0_0_1'

    conditions = orderby[2:].split('_')

    print(conditions)
    print(condition)

    str_cond = ''
    for index, element in enumerate(conditions):

        cond = condition[index][element]
        if cond != '':
            if str_cond == '':
                str_cond += ' where '
            str_cond += cond + ' and '

    if str_cond != '':
        str_cond = str_cond[:-len(' and ')]

    print(str_cond)

    order_by = 'r.post_time DESC'  # 默认按时间排序

    if order_dic[orderby[0:1]] != '':
        order_by = order_dic[orderby[0:1]]

    sql = """select r.id,area,rent_type,sha_identity,title,price,r.phone,r.post_time,start_time,end_time,house_name,position,
            floor,total_floor,has_kitchen_bath,lobby,live_room,orientation,
            r.type,mark,name,u.type as utype,avatar,verify,company_name,company_addr  from rent_room r left join user u on
            r.phone = u.phone {cond} ORDER BY {order_by}  LIMIT {page}, {offset}""".format(
        cond=str_cond, order_by=order_by,
        page=(page - 1) * 10, offset=10)

    print(sql)

    return get_rent_house(sql, page)


@app.route("/rent-search-house/<key_word>/<int:page>")
def rent_search_house(key_word, page):
    # 对字符进行过滤
    r1 = u'[a-zA-Z0-9’!"#$%&\'()*+,-./:;<=>?@，。?★、…【】《》？“”‘’！[\\]^_`{|}~]+'  # 用户也可以在此进行自定义过滤字符
    r2 = u'\s+;'

    key_word_temp = re.sub(r1, '', key_word)

    sql = """select r.id,area,rent_type,sha_identity,title,price,r.phone,r.post_time,start_time,end_time,house_name,position,
        floor,total_floor,has_kitchen_bath,lobby,live_room,orientation,
        r.type,mark,name,u.type as utype,avatar,verify,company_name,company_addr  from rent_room r left join user u on
        r.phone = u.phone where r.title like '%{key_word}%' or r.house_name like '%{key_word}%'  ORDER BY r.`post_time` DESC  LIMIT {page}, {offset}""".format(
        key_word=key_word_temp,
        page=(page - 1) * 10, offset=10)

    return get_rent_house(sql, page)


@app.route("/rent-house/<int:page>")
def rent_house(page=1):
    # 返回出租房屋

    sql = """select r.id,area,rent_type,sha_identity,title,price,r.phone,r.post_time,start_time,end_time,house_name,position,
    floor,total_floor,has_kitchen_bath,lobby,live_room,orientation,
    r.type,mark,name,u.type as utype,avatar,verify,company_name,company_addr  from rent_room r left join user u on
    r.phone = u.phone ORDER BY r.`post_time` DESC  LIMIT {page}, {offset}""".format(
        page=(page - 1) * 10, offset=10)

    return get_rent_house(sql, page)


@app.route("/sell-cond-house/<orderby>/<int:page>")
def sell_house_orderby(orderby, page):
    # 对买房信息进行排序 orderby = '1_1_1_1'
    # 第1个条件 1-5
    # {'id': 1, 'text': '价格从低到高'},
    # {'id': 2, 'text': '价格从高到低'},
    # {'id': 3, 'text': '面积从小到大'},
    # {'id': 4, 'text': '面积从大到小'},
    # {'id': 5, 'text': '发布时间'}
    # 第2个条件 1-4
    # {'id': 1, 'text': '30万以下'},
    # {'id': 2, 'text': '30万-60万'},
    # {'id': 3, 'text': '60万-100万'},
    # {'id': 4, 'text': '100万以上'}
    # 第3个条件 1-4
    # {'id': 1, 'text': '一房'},
    # {'id': 2, 'text': '两房'},
    # {'id': 3, 'text': '三房'},
    # {'id': 4, 'text': '四房'},
    # 第4个条件 1-3
    # {'id': 1, 'text': '住宅'},
    # {'id': 2, 'text': '商铺'},
    # {'id': 3, 'text': '写字楼'},

    condition = [
        {'0': '', '1': 'price < 30', '2': 'price >= 30 and price < 60', '3': 'price >= 60 and price < 100',
         '4': 'price >= 100 '},
        {'0': '', '1': 'live_room="一间"', '2': 'live_room="二间"', '3': 'live_room="三间"', '4': 'live_room="四间"'},
        {'0': '', '1': 'r.type=\"住宅\"', '2': 'r.type="商铺"', '3': 'r.type=\"写字楼\"'}]

    order_dic = {'0': '', '1': 'price', '2': 'price DESC', '3': 'area', '4': 'area DESC', '5': 'post_time'}

    # orderby = '1_0_0_1'

    conditions = orderby[2:].split('_')

    print(conditions)
    print(condition)

    str_cond = ''
    for index, element in enumerate(conditions):

        cond = condition[index][element]
        if cond != '':
            if str_cond == '':
                str_cond += ' where '
            str_cond += cond + ' and '

    if str_cond != '':
        str_cond = str_cond[:-len(' and ')]

    print(str_cond)

    order_by = 'r.post_time DESC'  # 默认按时间排序

    if order_dic[orderby[0:1]] != '':
        order_by = order_dic[orderby[0:1]]

    sql = """select r.id,pre_price,area,sha_identity,title,price,r.phone,r.post_time,start_time,end_time,house_name,position,
            floor,total_floor,has_kitchen_bath,lobby,live_room,orientation,
            r.type,mark,name,u.type as utype,avatar,verify,company_name,company_addr  from room r left join user u on
            r.phone = u.phone {cond} ORDER BY {order_by}  LIMIT {page}, {offset}""".format(
        cond=str_cond, order_by=order_by,
        page=(page - 1) * 10, offset=10)

    #print(sql)

    return get_rent_house(sql, page)


@app.route("/sell-search-house/<key_word>/<int:page>")
def sell_room_search(key_word, page):
    # 买房查询
    # 对字符进行过滤
    r1 = u'[a-zA-Z0-9’!"#$%&\'()*+,-./:;<=>?@，。?★、…【】《》？“”‘’！[\\]^_`{|}~]+'  # 用户也可以在此进行自定义过滤字符
    r2 = u'\s+;'

    key_word_temp = re.sub(r1, '', key_word)

    sql = """select r.id,area,pre_price,sha_identity,title,price,r.phone,r.post_time,start_time,end_time,house_name,position,
           floor,total_floor,has_kitchen_bath,lobby,live_room,orientation,
           r.type,mark,name,u.type as utype,avatar,verify,company_name,company_addr  from room r left join user u on
           r.phone = u.phone where r.title like '%{key_word}%' or r.house_name like '%{key_word}%'  ORDER BY r.`post_time` DESC  LIMIT {page}, {offset}""".format(
        key_word=key_word_temp,
        page=(page - 1) * 10, offset=10)

    return get_rent_house(sql, page)


@app.route("/house/<int:page>")
def house(page=1):
    # 返回格式
    result = {"code": 10000, "value": "", "msg": ""}

    if page <= 0:
        result = {"code": -10000, "value": "", "msg": "page 必须大于0"}
        return result

    sql = """select r.id,area, sha_identity,title,price,r.phone,r.post_time,start_time,end_time,house_name,position,
pre_price,floor,total_floor,has_kitchen_bath,five_year,lobby,live_room,orientation,
r.type,mark,name,u.type as utype,avatar,verify,company_name,company_addr  from room r left join user u on 
r.phone = u.phone ORDER BY r.`post_time` DESC  LIMIT {page}, {offset}""".format(
        page=(page - 1) * 10, offset=10)

    rooms = dbManager.exec_sql(sql)

    for room in rooms:
        # print(room)
        obj_room = Room()
        util.dict2obj(room, obj_room)
        # print(obj_room.phone)
        image_sql = "select name,path from image i where i.room_sha_identity ='{room_sha_identity}'".format(
            room_sha_identity=obj_room.sha_identity)

        # print(user_sql)
        if len(obj_room.title) > 32:
            room['title'] = obj_room.title[:32] + '...'

        room['post_time'] = obj_room.post_time.strftime('%Y-%m-%d')
        room['start_time'] = obj_room.start_time.strftime('%Y-%m-%d')
        room['end_time'] = obj_room.end_time.strftime('%Y-%m-%d')

        ret = dbManager.exec_sql(image_sql)
        #
        # print(ret)
        #
        room['image'] = ret

    result["value"] = rooms
    result["msg"] = "获取数据成功"

    return result


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

    # rent_house_orderby('1_1_1_1', 1)


    # get_room_detail('bdcb8013124c18f1fb72755d12f19e0d')
    # rooms = get_house(1)
    # #
    # # print(rooms)
    # print(json.dumps(rooms, ensure_ascii=False, indent=2))
