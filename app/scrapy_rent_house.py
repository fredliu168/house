# -*- coding: UTF-8 -*-
# 抓取出租的信息


import datetime

from bs4 import BeautifulSoup
from  app.model.room import *
from  app.model.user import *

from  app.model.image import *


class RentHouseScrap(object):
    # 抓取出租房屋信息

    def __init__(self):
        self.url = 'https://www.dehuaca.com/house.php?mod=list&profile_type_id=1&page={page}'  # 抓取租房信息
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:58.0) Gecko/20100101 Firefox/58.0'
        }

    def scrap(self):
        for page in range(1, 10):
            self._scrap(self.url.format(page=page))

    def _scrap(self, url):
        r = requests.get(url, headers=self.headers)
        soup = BeautifulSoup(r.content, 'lxml')
        house_table = soup.find('table', class_='dt ')
        house_trs = house_table.find_all('tr')

        for tr in house_trs:
            if tr.get('class') != None:
                tds = tr.find_all('td')
                for td in tds:
                    if td.get('class') == ['tdimg']:
                        tag_a = td.find('a', href=True)
                        href = tag_a.get('href')  # 获取房屋的详情链接
                        print(href)
                        self._scrap_detail(href)

    def _scrap_detail(self, url):
        room = RentRoom()
        user = User()

        room.url = url

        r = requests.get(url, headers=self.headers)
        soup = BeautifulSoup(r.content, 'lxml')
        # print(soup.prettify())

        # 获取标题 index_content_title
        index_content_title = soup.find('div', class_='index_content_title').find('h1').get_text().replace('[出租]',
                                                                                                           '').strip()

        # print(index_content_title)

        room.title = index_content_title

        # 获取子标题内容
        index_content_title_subtitle = soup.find('div', class_='index_content_title_subtitle cl')
        # print(index_content_title_subtitle)
        for tag_span in index_content_title_subtitle.find_all('span'): tag_span.decompose()

        subtitle_infos = index_content_title_subtitle.find('div', class_='z').get_text().strip().replace('\r',
                                                                                                         '').split(
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

        room.price = tag_price.get_text().replace('元', '')

        if room.price == '':
            room.price = 0

        tel_phone = index_content_extracontact_extra.find('span', class_='dt-agent-num')
        tel_phone_txt = tel_phone.get_text()
        # print(tel_phone_txt)
        # print(index_content_extracontact_extra.get_text().replace(' ', '').replace('\n', ''))

        # 用户电话号码
        user.phone = tel_phone_txt.replace('\n', '').replace('\r', '')
        room.phone = user.phone
        room.sha_identity = util.MD5(room.title + user.phone)  # 作为唯一标识

        room_infos = index_content_extracontact_extra.find('table', class_='fix')

        # print(room_infos)

        for tag_sup in room_infos.find_all('sup'): tag_sup.decompose()
        for tag_a in room_infos.find_all('a'): tag_a.decompose()

        tds = room_infos.find_all('td')

        dic_room_detail = {}

        dic_room_info_name = {'房屋面积': 'area', '房屋朝向': 'orientation', '房屋类型': 'type', '卧室': 'live_room',
                              '客厅': 'lobby', '当前楼层': 'floor', '总楼层': 'total_floor', '房屋厨卫': 'has_kitchen_bath',
                              '出租方式': 'rent_type',
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
                    val_txt = val.get_text().replace('\n', '').replace('\r', '').replace('\n', '').replace('M2',
                                                                                                           '').replace(
                        'm', '').strip()

                    print(val_txt)
                    if des_txt == '房屋面积':
                        if val_txt != '':
                            val_txt = val_txt[:-1]

                    if des_txt == '当前楼层':
                        if val_txt == '': val_txt = 0
                        val_txt = val_txt
                    if des_txt == '总楼层':
                        if val_txt == '': val_txt = 0
                        val_txt = val_txt

                    if des_txt == '房屋厨卫':
                        if val_txt == '是':
                            val_txt = 1
                        else:
                            val_txt = 0

                dic_room_detail[dic_room_info_name.get(des_txt)] = val_txt

        print(dic_room_detail)

        util.dict2obj(dic_room_detail, room)

        # print(room.pre_price)

        room.mark = soup.find('div', {"id": "b1"}).find('div', class_='cl').get_text().replace('?', '')

        # 获取图片信息

        tuan_box_tab_images = soup.find_all('div', class_='post_img')

        images = []

        if room.save():
            # 避免重复抓取数据
            for img in tuan_box_tab_images:
                # print(img.get('href'))
                # images.append(img.get('href'))
                # print(tuan_box_tab)
                image = RoomImage()
                image.post_time = room.post_time
                image.name = img.get('href')
                image.room_sha_identity = room.sha_identity
                images.append(json.loads(image.toJSON()))
                image.save()
            # room.images = images
            # 保存房间信息
            user.save()

        print(json.loads(room.toJSON()))

        print(json.loads(user.toJSON()))

        print(room.descript())
        print(user.descript())
        print(images)

        return room, user, images


if __name__ == '__main__':
    # url = 'https://www.dehuaca.com/house.php?mod=view&post_id=511357'
    url = 'https://www.dehuaca.com/house.php?mod=view&post_id=515491'

    rent_house = RentHouseScrap()
    # rent_house._scrap_detail(url)

    rent_house.scrap()
