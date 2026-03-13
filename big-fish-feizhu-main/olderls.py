import datetime
import requests

"""
    订单列表
"""
def quest_olders(cookies):
    """
    获取订单列表
    :param cookies:
    :return:
    """
    # 先获得时间数组格式的日期
    startDate = (datetime.datetime.now() - datetime.timedelta(days=3))
    startDate = startDate.strftime("%Y-%m-%d")

    endDate = (datetime.datetime.now() + datetime.timedelta(days=1))
    endDate = endDate.strftime("%Y-%m-%d %H:%M:%S")

    url = "https://hotel.fliggy.com/ebooking/orderlist/searchOrderList.do"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/114.0",
        "Accept": "*/*",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Accept-Encoding": "gzip, deflate, br",
        "Referer": "https://hotel.fliggy.com/ebooking/hotelBaseInfoUv.htm",
        "x-requested-with": "XMLHttpRequest",
        "X-XSRF-TOKEN": "----------",
        "bx-v": "2.5.1",
        "Connection": "keep-alive",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        'cookie': f'{cookies}',
        "TE": "trailers"

    }

    payload = {
        '_input_charset': 'UTF-8',
        'pageSize': '50',
        'hid': '0',
        'dateType': '3',
        'orderStatus': '0',
        'payType': '0',
        'sortType': '1',
        'startDate': f'{startDate}',
        'endDate': f'{endDate}',
        'groupType': 0,
        'currentPage': 1,
        '_input_charset': 'UTF-8'
    }

    response = requests.request("GET", url, headers=headers, params=payload)
    text = response.text
    try:
        text = response.json()
    except:
        # 提示cookie过期
        isinstance(text, dict)
        print('')
    if isinstance(text, dict):
        return True, text
    else:
        return False, -1


if __name__ == '__main__':
    from feizhu_cookie import feizhucookie

    cookie = feizhucookie()
    cookie = cookie.rcookie()

    print(quest_olders(cookie)[1])