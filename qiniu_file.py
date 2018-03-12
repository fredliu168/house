# -*- coding: utf-8 -*-
# flake8: noqa
# 七牛文件存储

from qiniu import Auth
from qiniu import BucketManager
import hashlib
import os

access_key = '9Iq0O8PRfdhsFQ8P6RYmTAPYwqLJx4KdFl_LUM0G'
secret_key = '44T_PSNoNPNw3MwyUQEogYbBDSsqegLDXUHpNDdj'

def MD5(src):
    m = hashlib.md5()
    m.update(src.encode())
    return  m.hexdigest()

def fetch_pic(url):
    # 保存网络图片
    bucket_name = 'house'
    q = Auth(access_key, secret_key)
    bucket = BucketManager(q)
    url_path, img_name = os.path.split(url)

    key = "{image_name}.{type}".format(image_name=MD5(url),type = img_name.split('.')[1])
    #
    ret, info = bucket.fetch(url, bucket_name, key)
    #print(ret)
    #print(info)
    # assert ret['key'] == key

    if ret == None:
        return False,key
    elif ret['key'] == key:
        return True,key
    else:
        return False,key

if __name__ == '__main__':

    url = 'https://uc1.dehua.net/data/avatar/000/32/80/24_avatar_big.jpg'
    ret,image_name = fetch_pic(url)
    print(ret)
    print(image_name)
