# -*- coding: UTF-8 -*-

from bs4 import BeautifulSoup
import requests
import os
import codecs
import json
import convertChineseDigitsToArabic as cn2a
import json
from collections import namedtuple
import hashlib
import os
from mysql_db.mysql import *
import datetime
import time

g_avatar_dir = '/Users/fred/PycharmProjects/house/avatar'  # 保存头像路径

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:58.0) Gecko/20100101 Firefox/58.0'
}


def scrap(url, user_dic):
    r = requests.get(url, headers=headers)
    # html_doc = r.text

    # html_doc = html_doc.replace("table","div")
    # html_doc = html_doc.replace("tr", "li")
    # html_doc = html_doc.replace("td", "div")

    # print(r.content)

    soup = BeautifulSoup(r.content, 'lxml')

    # print(soup.prettify())

    house_table = soup.find('table', class_='dt ')
    #
    # print(house_table)

    house_trs = house_table.find_all('tr')

    house_json = []

    # user_dic = {}

    for tr in house_trs:
        if tr.get('class') != None:

            house_node = {}

            # print(tr)
            # print('\n\r')
            tds = tr.find_all('td')

            for td in tds:

                if td.get('class') == ['tdimg']:
                    tag_a = td.find('a', href=True)
                    tag_img = td.find('img')

                    href = tag_a.get('href')  # 获取房屋的详情链接
                    img = tag_img.get('src')  # 获取房屋图片

                    house_node['link'] = href
                    house_node['image'] = img

                    print(href)

                    room_detail = scrap_detail(href)

                    user = room_detail.user

                    user_dic[user.phone] = json.loads(user.toJSON())
                    # user.descript()
                    # room_detail.descript()

                    house_node['attrs'] = json.loads(room_detail.toJSON())




                    # elif td.get('class') == ['tl']:
                    #
                    #     for tag_sup in td.find_all('sup'): tag_sup.decompose()
                    #
                    #     # print(td)
                    #     # print('\n\r')
                    #     tag_span = td.find('span')
                    #     tag_p = td.find('p')
                    #
                    #     price = tag_span.get_text()  # 价格
                    #     area = tag_p.get_text().replace(' ', '').split(':')[1].replace('m', '')  # 面积
                    #
                    #     house_node['price'] = float(price)
                    #     house_node['area'] = float(area)

                    # print(price)
                    # print(area)

                    # else:
                    #     for tag_sup in td.find_all('span'): tag_sup.decompose()
                    #
                    #     tag_a = td.find('a', href=True)
                    #     tag_div = td.find('div')
                    #
                    #     # print(td)
                    #     # print('\n\r')
                    #     title = tag_a.get_text()  # 获取标题
                    #     attrs = tag_div.get_text().replace(' ', '').replace('\r', '').split('\n')  # 获取房屋属性
                    #     attrs.pop(0)
                    #
                    #     house_node['title'] = title
                    #     house_node['attrs'] = attrs
                    # print(attrs)
                    # for index, attr in enumerate(attrs):
                    #
                    #     if index == 0:
                    #         house_node['type'] = attr
                    #     if index == 1:
                    #         house_node['room'] = cn2a.convertChineseDigitsToArabic(attr.split(':')[1].replace('间',''))
                    #     if index == 2:
                    #         house_node['lobby'] = cn2a.convertChineseDigitsToArabic(attr.split(':')[1].replace('间', ''))
                    #     if index == 3:
                    #         if attr.split(':')[1] == '有':
                    #             house_node['kitchen'] = 1
                    #         else:
                    #             house_node['kitchen'] = 0
                    #     if index == 4:
                    #         house_node['orientation'] = attr.split(':')[1]

                    # print(title)
                    # print('\n\r')
                    # print(attrs)
                    # print('\n\r')

            house_json.append(house_node)

            # break
            # print(house_json)
            # print(user_dic)

            # print(json.dumps(user_dic, ensure_ascii=False, indent=2))
    print(json.dumps(house_json, ensure_ascii=False, indent=2))

    # return user_dic


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


def MD5(src):
    m = hashlib.md5()
    m.update(src.encode())
    return m.hexdigest()


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


def save_avatar(url):
    # 保存用户头像

    url_path, img_name = os.path.split(url)
    avatar_name = "{image_name}.{type}".format(image_name=MD5(url), type=img_name.split('.')[1])

    # 保存头像到本地
    image_save_path = '{}/{}'.format(g_avatar_dir, avatar_name)

    ret = requests.get(url)

    if ret.status_code == 200:
        with open(image_save_path, 'wb') as file:
            file.write(ret.content)
        return avatar_name

    return ''




def scrap_detail(url):
    room = Room()
    user=  User()

    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.content, 'lxml')
    # print(soup.prettify())

    # 获取标题 index_content_title
    index_content_title = soup.find('div', class_='index_content_title').find('h1').get_text().replace('[出售]', '')

    # print(index_content_title)

    room.title = index_content_title

    # 获取子标题内容
    index_content_title_subtitle = soup.find('div', class_='index_content_title_subtitle cl')
    # print(index_content_title_subtitle)
    for tag_span in index_content_title_subtitle.find_all('span'): tag_span.decompose()

    subtitle_infos = index_content_title_subtitle.find('div', class_='z').get_text().strip().replace('\r', '').split(
        '\n')
    # subtitle_infos_txt = subtitle_infos
    subtitle_infos.pop(0)
    subtitle_infos.pop(3)
    post_time_label = subtitle_infos[0].strip()

    post_time = post_time_label[post_time_label.find(':') + 1:].strip()  # 发布时间
    start_time = subtitle_infos[1].strip().split(':')[1].strip()  # 开始时间
    end_time = subtitle_infos[2].strip().split(':')[1].strip()  # 结束时间S

    # 时间转成标准形式
    date_post_time = datetime.datetime.strptime(post_time, '%Y-%m-%d %H:%M')
    date_start_time = datetime.datetime.strptime(start_time, '%Y-%m-%d')
    date_end_time = datetime.datetime.strptime(end_time, '%Y-%m-%d')

    room.post_time = date_post_time.strftime('%Y-%m-%d %H:%M:%S')
    room.start_time = date_start_time.strftime('%Y-%m-%d %H:%M:%S')
    room.end_time = date_end_time.strftime('%Y-%m-%d %H:%M:%S')

    # print(post_time)
    # print(start_time)
    # print(end_time)

    # 获取经纪人信息
    index_content_extracontact_userinfo = soup.find('div', class_='index_content_extracontact_userinfo')
    # 获取头像和昵称
    index_content_extracontact_userinfo_ava = index_content_extracontact_userinfo.find('div',
                                                                                       class_='index_content_extracontact_userinfo_ava')

    ava_img_url = index_content_extracontact_userinfo_ava.find('img').get('src')
    # print(ava_img_url)
    user_name_infos = index_content_extracontact_userinfo_ava.find('p').get_text().replace('(', '').replace(')',
                                                                                                            '').split(
        ' ')
    # print(user_name_infos)
    user_name = user_name_infos[0]
    user_type = user_name_infos[1]
    # print(user_name)
    # print(user_name_type)  # 是否经济人还是个人发布

    if user_type == '个人':
        user.type = 0
    elif user_type == '经纪人':
        user.type = 1

    user.name = user_name
    user.avatar = ava_img_url

    # 公司信息
    cop_infos = index_content_extracontact_userinfo.find('table', class_='fix')
    cop_infos_text = cop_infos.get_text()
    # print(cop_infos_text)

    user_verify = 1  # 经纪人是否身份认证
    if cop_infos_text.find('未认证') != -1:
        user_verify = 0

    cop_index_begin = cop_infos_text.find('经纪公司:')

    if cop_index_begin != -1:
        cop_index_end = cop_infos_text.find('公司地址:')
        cop_name = cop_infos_text[cop_index_begin + len('经纪公司:'):cop_index_end].strip()
        cop_addr_end = cop_infos_text.find('联系QQ:')
        cop_addr = cop_infos_text[cop_index_end + len('公司地址:'):cop_addr_end].strip()

        user.company_name = cop_name
        user.company_addr = cop_addr

    user.verify = user_verify

    # 获取房屋信息

    index_content_extracontact_extra = soup.find('div', class_='index_content_extracontact_extra')
    # print(index_content_extracontact_extra)
    tag_price = index_content_extracontact_extra.find('span', class_='dt-agent-l').find('em')
    print(tag_price.get_text())

    room.price = tag_price.get_text()

    tel_phone = index_content_extracontact_extra.find('span', class_='dt-agent-num')
    tel_phone_txt = tel_phone.get_text()
    # print(tel_phone_txt)
    # print(index_content_extracontact_extra.get_text().replace(' ', '').replace('\n', ''))

    # 用户电话号码
    user.phone = tel_phone_txt.replace('\n', '').replace('\r', '')
    room.phone = user.phone
    room.sha_identity = MD5(room.title+user.phone) #作为唯一标识

    room_infos = index_content_extracontact_extra.find('table', class_='fix')

    # print(room_infos)

    for tag_sup in room_infos.find_all('sup'): tag_sup.decompose()
    for tag_a in room_infos.find_all('a'): tag_a.decompose()

    tds = room_infos.find_all('td')

    dic_room_detail = {}

    dic_room_info_name = {'房屋面积': 'area', '房屋单价': 'pre_price', '房屋朝向': 'orientation', '房屋类型': 'type', '卧室': 'live_room',
                          '客厅': 'lobby', '当前楼层': 'floor', '总楼层': 'total_floor', '房屋厨卫': 'has_kitchen_bath',
                          '产权满五': 'five_year',
                          '楼盘名称': 'house_name', '房屋配置': 'config', '所属区域': 'position'}

    for td in tds:
        # print('')
        # print(td)
        des = td.find('span', class_='des')
        val = td.find('span', class_='val')

        des_txt = ''
        val_txt = ''

        if des != None:
            des_txt = des.get_text().replace('\n', '').replace('\r', '').replace('\n', '').strip()
            des_txt = des_txt[:-1]

            if val != None:
                val_txt = val.get_text().replace('\n', '').replace('\r', '').replace('\n', '').strip()
                if des_txt == '房屋面积':
                    val_txt = float(val_txt[:-1])
                if des_txt == '房屋单价':
                    val_txt = float(val_txt[:-3])
                if des_txt == '当前楼层':
                    val_txt = int(val_txt)
                if des_txt == '总楼层':
                    val_txt = int(val_txt)

                if des_txt == '房屋厨卫':
                    if val_txt == '是':
                       val_txt = 1
                    else:
                       val_txt = 0
                if des_txt == '产权满五':
                    if val_txt == '是':
                       val_txt = 1
                    else:
                       val_txt = 0

            dic_room_detail[dic_room_info_name.get(des_txt)] = val_txt


    print(dic_room_detail)

    dict2obj(dic_room_detail, room)

    print(room.pre_price)

    room.mark = soup.find('div', {"id": "b1"}).find('div', class_='cl').get_text().replace('?', '')

    # 获取图片信息

    tuan_box_tab_images = soup.find_all('div', class_='post_img')

    images = []
    for img in tuan_box_tab_images:
        # print(img.get('href'))
        images.append(img.get('href'))

        # print(tuan_box_tab)

    #room.images = images

    return room,user

    # room.descript()


def save_user2db(users_dic):
    #把数据保存到数据库
    insert_data = []

    for user_dic in users_dic.values():
        user = User()
        dict2obj(user_dic, user)
        user.avatar = save_avatar(user.avatar)
        insert_data.append(json.loads(user.toJSON()))

    dbManager.insert('user', insert_data=insert_data)

def save_room2db(rooms):
    #把房产数据保存到数据库
    dbManager.insert('room', insert_data=rooms)

if __name__ == '__main__':
    users_dic = {}

    # for index in range(1,5):
    #
    #     url = 'https://www.dehuaca.com/house.php?mod=list&profile_type_id=3&page={index}'.format(index = index)
    #
    #     print(url)
    #
    #     scrap(url,user_dic)
    #
    # print(len(user_dic))
    # print(json.dumps(user_dic, ensure_ascii=False, indent=2))

    url = 'https://www.dehuaca.com/house.php?mod=list&profile_type_id=3&page={index}'.format(index=1)
    # print(url)
    #scrap(url, users_dic)
    #save_user2db(users_dic)


    # a = dbManager.get(table="user", show_list=['*'])
    # print(a)


    # url = 'https://www.dehuaca.com/house.php?mod=view&post_id=510104'
    # url = 'https://www.dehuaca.com/house.php?mod=view&post_id=501384'
    # url = 'https://www.dehuaca.com/house.php?mod=view&post_id=504870'
    url = 'https://www.dehuaca.com/house.php?mod=view&post_id=499246'
    room_detail,user = scrap_detail(url)
    room_detail.descript()
    #user.descript()
    #
    print(json.loads(room_detail.toJSON()))

    rooms = []
    rooms.append(json.loads(room_detail.toJSON()))
    save_room2db(rooms)

    # print(cn2a.convertChineseDigitsToArabic('二'))
    # pass
