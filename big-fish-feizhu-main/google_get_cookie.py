import random
import time

from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions
from selenium.webdriver import ActionChains

"""
谷歌驱动隐藏指纹获取cookie
"""

login_url = 'https://hotel.fliggy.com/ebooking/hotelBaseInfoUv.htm#/ebk/order/list'
username = 'your username'
password = 'your password'


class feizhucookie():
    """
    生成cookie
    """

    def fzcookie(self):
        options = ChromeOptions()
        # 隐藏正受到自动测试软件的控制。
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        options.add_experimental_option('useAutomationExtension', False)

        driver = Chrome(executable_path=r'./google/chromedriver.exe', options=options)

        with open('./google/stealth.min.js') as f:
            js = f.read()
        driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": js
        })

        # driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        #     "source": """
        #   Object.defineProperty(navigator, 'webdriver', {
        #     get: () => false
        #   })
        # """
        # })
        # driver.get('https://bot.sannysoft.com/')
        driver.get(login_url)
        driver.find_element_by_xpath('//*[@id="fm-login-id"]').send_keys(username)
        driver.find_element_by_xpath('//*[@id="fm-login-password"]').send_keys(password)
        span_background = driver.find_element_by_xpath('//*[@id="nc_1__scale_text"]/span')
        span_background_size = span_background.size

        # 滑块方法
        self.slider_unit(driver)
        driver.find_element_by_xpath('//*[@id="login-form"]/div[4]/button').click()
        time.sleep(3)
        is_reload = False
        try:
            if 'https://hotel.fliggy.com/ebooking/hotelBaseInfoUv.htm#/ebk' != driver.current_url:
                is_reload = False
            is_reload = True
            # 检测是否登录成功
        except:
            is_reload = False
        cookie2 = None
        if is_reload:
            # 登录成功获取cookie
            cookie2 = self.get_cookie(driver)
        time.sleep(5)
        print(cookie2)
        driver.close()
        if cookie2 != None:
            return cookie2
        else:
            return 'cookie失效'

    def get_cookie(self, page):
        """
      获取cookie
      :param:page page对象
      :return:cookies 处理后的cookie
      """
        cookie_list = page.get_cookies()
        cookies = ""
        for cookie in cookie_list:
            if cookie.get("name") == 'cookie2':
                coo = "{}={};".format(cookie.get("name"), cookie.get("value"))
                cookies += coo
        print(cookies)
        return cookies

    def wcookie(self):
        # 写入cookie
        fzcookie = self.fzcookie()
        if fzcookie == 'cookie失效':
            return False
        fo = open("./feizhu_unit/cookie2.txt", "w")
        fo.write(fzcookie)
        fo.close()
        return True

    def rcookie(self):
        # 读取文件cookie
        fo = open("./feizhu_unit/cookie2.txt", "r")
        fzcookie = fo.readline()
        fo.close()
        return fzcookie
    def slider_unit(self, driver):
        """
        滑块
        :param driver:
        :return:
        """
        s = "//span[contains(@class, 'btn_slide')]"
        try:
            driver.switch_to.frame("baxia-dialog-content")
            slider = driver.find_element_by_xpath(f"{s}")
            if slider.is_displayed():
                ActionChains(driver).click_and_hold(on_element=slider).perform()
                ActionChains(driver).move_by_offset(xoffset=258, yoffset=0).perform()
                ActionChains(driver).pause(0.5).release().perform()
                driver.switch_to.parent_frame()
                time.sleep(3)
        except Exception as e:
            print(e)
            pass

if __name__ == '__main__':
    feizhucookie = feizhucookie()
    feizhucookie.wcookie()
