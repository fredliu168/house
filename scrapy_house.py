# -*- coding: UTF-8 -*-

from bs4 import BeautifulSoup
import requests
import os
import codecs
import json
import convertChineseDigitsToArabic as cn2a
import json

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:58.0) Gecko/20100101 Firefox/58.0'
}


def scrap(url,user_dic):

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

    #user_dic = {}

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

                    # print(td)
                    # print('\n\r')
                    # print(img)
                    print(href)

                    room_detail = scrap_detail(href)

                    user = room_detail.user

                    user_dic[user.tel_phone] = json.loads(user.toJSON())
                    #user.descript()
                    #room_detail.descript()


                elif td.get('class') == ['tl']:

                    for tag_sup in td.find_all('sup'): tag_sup.decompose()

                    # print(td)
                    # print('\n\r')
                    tag_span = td.find('span')
                    tag_p = td.find('p')

                    price = tag_span.get_text()  # 价格
                    area = tag_p.get_text().replace(' ', '').split(':')[1].replace('m', '')  # 面积

                    house_node['price'] = float(price)
                    house_node['area'] = float(area)

                    # print(price)
                    # print(area)

                else:
                    for tag_sup in td.find_all('span'): tag_sup.decompose()

                    tag_a = td.find('a', href=True)
                    tag_div = td.find('div')

                    # print(td)
                    # print('\n\r')
                    title = tag_a.get_text()  # 获取标题
                    attrs = tag_div.get_text().replace(' ', '').replace('\r', '').split('\n')  # 获取房屋属性
                    attrs.pop(0)

                    house_node['title'] = title
                    house_node['attrs'] = attrs
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
    #print(house_json)
    #print(user_dic)

    #print(json.dumps(user_dic, ensure_ascii=False, indent=2))
    # print(json.dumps(house_json))

    #return user_dic

class User():
    # 用户信息
    user_name = ''  # 发布人信息
    tel_phone = ''  # 联系方式
    user_name_type = ''  # 用户特征 个人/经纪人
    ava_img_url = ''  # 用户头像信息
    user_verify = 0  # 用户是否认证
    # 公司信息
    cop_name = ''  # 公司名称
    cop_addr = ''  # 公司地址

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)

    def descript(self):

        print(self.user_name)
        print(self.tel_phone)
        print(self.user_name_type)
        print(self.ava_img_url)
        print(self.user_verify)
        print(self.cop_name)
        print(self.cop_addr)

class Room():
    # 发布用户信息
    user = User()

    # 房间类型
    post_time = ''  # 发布时间
    start_time = ''  # 开始时间
    end_time = ''  # 结束时间
    # 房屋信息
    area = '' #面积
    floor = 0  # 楼层
    total_floor = 0  # 总层高
    has_kitchen_bath = 0  # 是否有厨卫
    has_property_five = 0  # 产权是否满五年
    # 房屋图片
    images = []

    def descript(self):
        print(self.post_time)
        print(self.start_time)
        print(self.end_time)

        self.user.descript()
        # print(self.user_name)
        # print(self.tel_phone)
        # print(self.user_name_type)
        # print(self.ava_img_url)
        # print(self.user_verify)

        # print(self.cop_name)
        # print(self.cop_addr)
        print(self.area)
        print(self.floor)
        print(self.total_floor)
        print(self.has_kitchen_bath)
        print(self.has_property_five)

        print(self.images)


def scrap_detail(url):
    room = Room()



    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.content, 'lxml')
    # print(soup.prettify())

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
    end_time = subtitle_infos[2].strip().split(':')[1].strip()  # 结束时间

    room.post_time = post_time
    room.start_time = start_time
    room.end_time = end_time

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
    user_name_type = user_name_infos[1]
    # print(user_name)
    # print(user_name_type)  # 是否经济人还是个人发布

    room.user.user_name = user_name
    room.user.user_name_type = user_name_type
    room.user.ava_img_url = ava_img_url

    # 公司信息
    cop_infos = index_content_extracontact_userinfo.find('table', class_='fix')
    cop_infos_text = cop_infos.get_text()
    #print(cop_infos_text)

    user_verify = 1  # 经纪人是否身份认证
    if cop_infos_text.find('未认证') != -1:
        user_verify = 0



    cop_index_begin = cop_infos_text.find('经纪公司:')


    if cop_index_begin != -1:

        cop_index_end = cop_infos_text.find('公司地址:')
        cop_name = cop_infos_text[cop_index_begin + len('经纪公司:'):cop_index_end].strip()
        cop_addr_end = cop_infos_text.find('联系QQ:')
        cop_addr = cop_infos_text[cop_index_end + len('公司地址:'):cop_addr_end].strip()

        room.user.cop_name = cop_name
        room.user.cop_addr = cop_addr

    room.user.user_verify = user_verify


    # print(user_verify)
    # print(cop_name)
    # print(cop_addr)

    # 获取房屋信息

    index_content_extracontact_extra = soup.find('div', class_='index_content_extracontact_extra')
    #print(index_content_extracontact_extra)

    tel_phone = index_content_extracontact_extra.find('span', class_='dt-agent-num')
    tel_phone_txt = tel_phone.get_text()
    # print(tel_phone_txt)
    # print(index_content_extracontact_extra.get_text().replace(' ', '').replace('\n', ''))

    room.user.tel_phone = tel_phone_txt.replace('\n', '').replace('\r', '')

    room_infos = index_content_extracontact_extra.find('table',class_='fix')

    #print(room_infos)

    for tag_sup in room_infos.find_all('sup'): tag_sup.decompose()
    for tag_a in room_infos.find_all('a'): tag_a.decompose()

    tds = room_infos.find_all('td')

    choices = {"房屋面积:":room.area,}

    for td in tds:
        # print('')
        # print(td)
        des = td.find('span',class_='des')
        val = td.find('span', class_='val')

        des_txt = ''
        val_txt = ''

        if des != None:
            des_txt = des.get_text().replace('\n', '').replace('\r', '').replace('\n','').strip()

        if val != None:
            val_txt = val.get_text().replace('\n', '').replace('\r', '').replace('\n','').strip()

        if des_txt == '房屋面积':
            pass

        obj = choices.get(des_txt,None)
        if obj != None:
            obj = val_txt
            print(obj)
        print(des_txt)
        print(val_txt)


    contact_extra = index_content_extracontact_extra.get_text().replace(' ', '').replace('\n', '')

    print()

    index_floor_begin = contact_extra.find('当前楼层:')
    index_floor_end = contact_extra.find('总楼层:')
    floor = contact_extra[index_floor_begin + len('当前楼层:'):index_floor_end]

    index_total_floor_end = contact_extra.find('房屋厨卫:')
    total_floor = contact_extra[index_floor_end + len('总楼层:'):index_total_floor_end]
    has_kitchen_bath_end = contact_extra.find('产权满五:')

    has_kitchen_bath = 0

    if contact_extra[index_total_floor_end + len('房屋厨卫:'):has_kitchen_bath_end] == '有':
        has_kitchen_bath = 1

    has_property_five = 0  # 有产权满五

    if contact_extra[has_kitchen_bath_end + len('产权满五:'):has_kitchen_bath_end + len('产权满五:') + 1] == "是":
        has_property_five = 1

    # print(floor)
    # print(total_floor)
    # print(has_kitchen_bath)
    # print(has_property_five)

    room.floor = floor
    room.total_floor = total_floor
    room.has_kitchen_bath = has_kitchen_bath
    room.has_property_five = has_property_five

    # 获取图片信息

    tuan_box_tab_images = soup.find_all('div', class_='post_img')

    images = []
    for img in tuan_box_tab_images:
        # print(img.get('href'))
        images.append(img.get('href'))

        # print(tuan_box_tab)

    room.images = images

    return room

    # room.descript()


if __name__ == '__main__':

    user_dic = {}

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

    # url = 'https://www.dehuaca.com/house.php?mod=list&profile_type_id=3&page={index}'.format(index=1)
    # print(url)
    # scrap(url, user_dic)

    url = 'https://www.dehuaca.com/house.php?mod=view&post_id=501384'
    # url = 'https://www.dehuaca.com/house.php?mod=view&post_id=504870'
    #url = 'https://www.dehuaca.com/house.php?mod=view&post_id=499246'
    room_detail = scrap_detail(url)
    room_detail.descript()
    # print(cn2a.convertChineseDigitsToArabic('二'))
    #pass
