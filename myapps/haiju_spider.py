# -*- coding: utf8 -*-

import requests
import json
import pymysql

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'}
start_url = 'http://www.91haiju.com/index/House/housingDetail/?housing_id='
haiju_url = 'http://www.91haiju.com/index/House/housingList?ajax=1'

base_sql = """insert into haiju_house_info(gui_ge, title, high, price, update_time, special, housing_code, url) value (%s,%s,%s,%s,%s,%s,%s,%s)"""

site_list = [u'长城坐标城', u'中建大公馆', u'光谷理想城', u'北辰光谷里', u'中建康城', u'融科天域', u'红枫金座', u'金地·格林东郡', u'关山春晓', u'金地·太阳城',
             u'保利时代天悦',
             u'保利时代北区', u'保利时代', u'万科·城花璟苑', u'光谷理想城']


def process(key, cursor):
    data = {
        'house_name': key,
        'page': 1,
    }
    res = requests.post(url=haiju_url, headers=headers, data=data)
    datas = json.loads(res.text)
    tolpage = datas['tolpage']
    for page in range(1, tolpage + 1):
        other_data = {
            'house_name': key,
            'page': page,
        }
        response = requests.post(url=haiju_url, headers=headers, data=other_data)
        datas = json.loads(response.text)
        for data in datas['data']:
            gui_ge = data['gui_ge']  # 规格
            site = data['house_name']  # 地点
            housing_code = data['housing_code']  # 房子id
            high = data['lease_type']  # 楼层
            update_time = data['update_time']  # 上次更新时间
            price = data['rent']  # 费用
            special = ",".join(data['configure'])  # 特色
            house_url = start_url + str(housing_code)
            cursor.execute(base_sql, tuple(
                [gui_ge.encode('utf-8'), site.encode('utf-8'), high, price, update_time, special.encode('utf-8'),
                 housing_code, house_url]))


# 去重
update_sql = """DELETE FROM haiju_house_info WHERE id NOT IN( SELECT t.id FROM( SELECT max(id) as id FROM haiju_house_info GROUP BY housing_code) t);"""


def main():
    conn = pymysql.connect(host='localhost', port=3306, user='root', password='ll52283140', db='soos',
                           charset='utf8')
    cursor = conn.cursor()
    for key in site_list:
        process(key, cursor)
    cursor.execute(update_sql)
    conn.commit()
    conn.close()


if __name__ == '__main__':
    main()
