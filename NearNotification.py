# encoding: utf-8

__author__ = 'zhourongyu'
import datetime
import time
import json
import requests
import objc
import Foundation
import sys

NSUserNotification = objc.lookUpClass('NSUserNotification')
NSUserNotificationCenter = objc.lookUpClass('NSUserNotificationCenter')


def notify(title, subtitle, info_text, delay=0, sound=False, userInfo={}):
    notification = NSUserNotification.alloc().init()
    notification.setTitle_(title)
    notification.setSubtitle_(subtitle)
    notification.setInformativeText_(info_text)
    notification.setUserInfo_(userInfo)
    if sound:
        notification.setSoundName_("NSUserNotificationDefaultSoundName")
    notification.setDeliveryDate_(Foundation.NSDate.dateWithTimeInterval_sinceDate_(delay, Foundation.NSDate.date()))
    NSUserNotificationCenter.defaultUserNotificationCenter().scheduleNotification_(notification)


def queryAndOrder(session_id, sid):
    url = "http://api.haojin.in/takeout_item_list?atag_id=0&offset=0&pagesize=10&region_id=55b9c9d4c69575999049b2b4"
    headers = {'content-type': 'application/json', 'User-Agent': 'User-Agent: QMMWD/1.3.6 iPhone/9.1 AFNetwork/1.1'}
    req = requests.get(url, headers=headers)
    content = json.loads(req.content)
    items = content['data']['sale_items']
    for item in items:
        price = item['price']
        title = item['title']
        origin_price = item['origin_price']
        end_time = item['end_time']
        quantity = item['quantity']
        activity_id = item['activity_id']
        e = datetime.datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")
        if float(price) < 2 and e > datetime.datetime.now() and quantity > 0:
            if (session_id is not None and sid is not None):
                order(activity_id, session_id, sid)
            else:
                notify(u"特价提醒!!", title, u"原价" + origin_price + u",现价:" + price, sound=True)


def order(aid, session_id, sid):
    addr_id = get_address(session_id)
    url = "http://mmwd.me/api/order/activity_buy"
    headers = {'content-type': 'application/json',
               'User-Agent': 'User-Agent: QMMWD/1.3.6 iPhone/9.1 AFNetwork/1.1',
               'Cookie': 'sid=' + str(sid)}
    payload = {"amount": "1", "activity_id": aid, "addr_id": addr_id, "remark": ""}
    r = requests.post(url, data=json.dumps(payload), headers=headers)
    data = json.loads(r.text)['data']
    notify(u"抢购成功", data['goods_name'], u"需支付金额: " + str(data['total_amt'] / 100), sound=True)


def get_address(session_id):
    url = "http://api.haojin.in/get_addr_list"
    headers = {'content-type': 'application/json',
               'User-Agent': 'User-Agent: QMMWD/1.3.6 iPhone/9.1 AFNetwork/1.1',
               'Cookie': 'sessionid=' + str(session_id)}
    req = requests.get(url, headers=headers)
    content = json.loads(req.content)['data']
    if (len(content['addrs']) > 0):
        return content['addrs'][0]['id']


if __name__ == '__main__':
    session_id = None
    sid = None
    if len(sys.argv) == 3:
        session_id = sys.argv[1]
        sid = sys.argv[2]

    while True:
        queryAndOrder(session_id, sid)
        time.sleep(30)
