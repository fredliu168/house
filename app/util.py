# -*- coding: utf-8 -*-
# 公共函数
# 2018.3.13
import hashlib
import json
from collections import namedtuple


def MD5(src):
    # md5 加密
    m = hashlib.md5()
    m.update(src.encode())
    return m.hexdigest()


def is_number(s):
    #判断是否为数字
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False


def mkdir(path):
    '''
    创建文件夹目录
    :param path:
    :return:
    '''
    # 引入模块
    import os

    # 去除首位空格
    path = path.strip()
    # 去除尾部 \ 符号
    path = path.rstrip("\\")

    # 判断路径是否存在
    # 存在     True
    # 不存在   False
    isExists = os.path.exists(path)

    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        print(path + ' 创建成功')
        # 创建目录操作函数
        os.makedirs(path)
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        print(path + ' 目录已存在')
        return False

def _json_object_hook(d):
    return namedtuple('X', d.keys())(*d.values())


def json2obj(data):
    return json.loads(data, object_hook=_json_object_hook)


# 字典转对象
def dict2obj(d, obj):
    if isinstance(d, list):
        d = [dict2obj(x) for x in d]
    if not isinstance(d, dict):
        return d

    class C(object):
        pass

    # o = Room()
    for k in d:
        obj.__dict__[k] = dict2obj(d[k], obj)
    return obj
