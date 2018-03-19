# -*- coding: utf-8 -*-
# 提供数据接口
# 2018.3.14

from flask import Flask, Response, jsonify
import datetime
from mysql_db.mysql import *
import util
import config
from  model.room import *


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

    img_local_path = "{}/{}".format(config.g_source_img_dir,image_name)

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
    if imageid == 'default':  # 设置默认图片
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

    if obj_room.company_name!=None and len(obj_room.company_name) > 10:
        room['company_name'] = obj_room.company_name[:10] + '...'

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

    if len(obj_room.company_name) >10:
        room['company_name'] = obj_room.company_name[:10]+'...'

    ret = dbManager.exec_sql(image_sql)

    room['image'] = ret

    # print(room)

    result["value"] = room
    result["msg"] = "获取数据成功"

    return result

@app.route("/rent-house/<int:page>")
def rent_house(page=1):
    # 返回出租房屋
    result = {"code": 10000, "value": "", "msg": ""}

    if page <= 0:
        result = {"code": -10000, "value": "", "msg": "page 必须大于0"}
        return result

    sql = """select r.id,area,rent_type,sha_identity,title,price,r.phone,r.post_time,start_time,end_time,house_name,position,
    floor,total_floor,has_kitchen_bath,lobby,live_room,orientation,
    r.type,mark,name,u.type as utype,avatar,verify,company_name,company_addr  from rent_room r left join user u on
    r.phone = u.phone ORDER BY r.`post_time` DESC  LIMIT {page}, {offset}""".format(
        page=(page - 1) * 10, offset=10)

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

        ret = dbManager.exec_sql(image_sql)
        #
        # print(ret)
        #
        room['image'] = ret

    result["value"] = rooms
    result["msg"] = "获取数据成功"

    return result

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

    # get_room_detail('bdcb8013124c18f1fb72755d12f19e0d')
    # rooms = get_house(1)
    # #
    # # print(rooms)
    # print(json.dumps(rooms, ensure_ascii=False, indent=2))
