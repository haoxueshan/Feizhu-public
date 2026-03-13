import requests

"""
订单详情
"""
def quest_orderinfo(tid, cookie):
    """
    订单详情
    :param tid:
    :param cookie:
    :return:
    """
    url = "https://hotel.fliggy.com/ebooking/order/queryOrderDetailV2.do"
    payload = {
        'tid': f'{tid}',
        '_input_charset': 'UTF-8'
    }
    headers = {
        'authority': 'hotel.fliggy.com',
        'accept': '*/*',
        'accept-language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        'bx-v': '2.5.0',
        'cache-control': 'no-cache',
        'cookie': f'{cookie}',
        'pragma': 'no-cache',
        'referer': 'https://hotel.fliggy.com/ebooking/hotelBaseInfoUv.htm',
        'sec-ch-ua': '"Google Chrome";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
        'x-xsrf-token': '---------'
    }
    response = requests.request("GET", url, headers=headers, params=payload)
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
    print(quest_orderinfo('3387248713494950404', cookie))
