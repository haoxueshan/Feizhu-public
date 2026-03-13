from olderls import quest_olders
from orderinfo import quest_orderinfo
from operate import quest_operate
from feizhu_cookie import feizhucookie
from feizhu_unit.emaill import Alarm
import time
from feizhu_unit.sqlserver import SQLserver
import traceback
import re

# orderDict = {'orderId': '', 'poiName': '', 'checkIn': '', 'checkOut': '', 'roomName': '', 'breakfast': '',
#              'roomCount': '', 'guest_name': '', 'guest_num': '', 'floorPrice': '', 'status': '', 'payTime': '',
#              'operator': '', 'channel': ''}
reqb = True
email = Alarm()
# 操作人列表
OperatorNameLs = ['hotel961527', 'hotel961260', 'hotel961258', 'hotel958422', 'hotel959060']

run_sleep = 240  # 程序等待时间，单位秒。


def save_data():
    global reqb, OperatorNameLs
    try:
        while reqb:
            print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
            sqldb = SQLserver()
            req_cookie2 = feizhucookie()
            cookie2 = req_cookie2.rcookie()
            req_olders = quest_olders(cookie2)
            if req_olders[0]:
                orders_Data = req_olders[1]
            else:
                if req_cookie2.wcookie():
                    continue
                email.send_mail(time.strftime("%Y-%m-%d %p %H:%M:%S", time.localtime()), '飞猪登录失效')
                reqb = False
                break  # 登录错误退出程序

            # 分割
            q = 0
            order_Data_Ls = []

            # 判断是否存在订单
            if orders_Data['data']['count'] == 0:
                print('没有订单')
                time.sleep(run_sleep)
                continue
            for order in orders_Data['data']['hotelOrderList']:
                tid = order['tid']
                # req_orderinfo = quest_orderinfo(tid, cookie2)  # 订单详情
                req_operate = quest_operate(tid, cookie2)  # 操作详情
                if req_operate[0]:
                    operate_Info = req_operate[1]
                else:
                    if req_cookie2.wcookie():
                        continue
                    reqb = False
                    break  # 登录错误退出程序

                guesName = ''
                for i in order['guestInfo']['guestList']:
                    if guesName != '':
                        guesName = guesName + ','
                    guesName = guesName + i['name']

                operateName = ''
                try:
                    for i in operate_Info['data']['opLogDOList']:
                        # 使用正则表达式提取字母和数字
                        result = re.findall(r'[a-zA-Z0-9]+', i['operatorName'])

                        # 将结果连接成一个字符串
                        cleaned_text = ''.join(result)
                        if 'hotel' in cleaned_text:
                            operateName = cleaned_text
                        if operateName != '':
                            break
                except:
                    print(operate_Info.get('data'))
                # 判断是否更新
                operateName='fz2023'
                print(tid)
                select_id = sqldb.select_fetchone("select * from review where orderId=" + tid)
                if select_id != None:
                    if select_id['status'].encode('latin1').decode('gbk') != (order['orderStatusDesc'].split('('))[0]\
                            :# or select_id['operator'].encode('latin1').decode('gbk') != operateName:
                        olderUp = "update review set  status='{}',operator='{}'  WHERE orderId ='{}'"
                        olderUp = olderUp.format((order['orderStatusDesc'].split('('))[0], operateName, tid)
                        sqldb.m_update(olderUp)
                    continue
                # 将订单添加入列表

                order_Data_Ls.append((order['tid'], order['hotelName'],
                                      time.strftime("%Y-%m-%d",
                                                    time.localtime(
                                                        float(order['orderTimeInfo']['checkInDate']) / 1000)),
                                      time.strftime("%Y-%m-%d",
                                                    time.localtime(
                                                        float(order['orderTimeInfo']['checkOutDate']) / 1000)),
                                      order['roomTypeName'],
                                      order['orderBreakfastDO']['breakfastDesc'], '%s' % order['roomNumber']['value'],
                                      guesName, '%s' % len(order['guestInfo']['guestList']),
                                      float(order['bookingRoomPrice']['showAmount']) * 0.9,
                                      (order['orderStatusDesc'].split('('))[0],
                                      time.strftime("%Y-%m-%d %H:%M:%S",
                                                    time.localtime(float(order['orderTimeInfo']['bookTime']) / 1000)),
                                      operateName, '飞猪'
                                      ))
                print(order_Data_Ls[q])
                q = q + 1
            inesrt_re = "insert into review(orderId, poiName, checkIn, checkOut, roomName, breakfast,roomCount," \
                        " guest_name, guest_num,floorPrice,status,payTime,operator,channel)" \
                        " values (%s, %s, %s, %s,%s, %s,%s, %s,%s,%s,%s,%s,%s,%s)"
            sqldb.m_insert(inesrt_re, order_Data_Ls)
            print(f'飞猪新增{q}个订单')
            print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
            time.sleep(run_sleep)
        return False, '登录错误'
    except:
        e = traceback.format_exc()
        print(e)
        return True, e


runSave = save_data()
if runSave[0]:
    email.send_mail(runSave[1], '飞猪异常错误')
email.send_mail(runSave[1], '飞猪登录失效')

