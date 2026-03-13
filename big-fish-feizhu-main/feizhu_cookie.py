import random
import time
import os
from selenium.webdriver import Firefox
from selenium.webdriver import FirefoxProfile
from selenium.webdriver import FirefoxOptions
from selenium.webdriver import ActionChains


# 获取当前脚本的绝对路径
current_path = os.path.abspath(__file__)
directory = os.path.dirname(current_path)
login_url = 'https://login.taobao.com/member/login.jhtml?redirectURL=https%3A%2F%2Fhotel.fliggy.com%2Febooking%2FhotelBaseInfoUv.htm#/ebk/order/list'
# login_url = 'https://bot.sannysoft.com/'
username = 'your username'
password = 'your password'


class feizhucookie():
    """
    生成cookie
    """

    def fzcookie(self):

        profile = FirefoxProfile()
        options = FirefoxOptions()
        options.log.level = "fatal"
        # 将dom.webdriver.enabled设置为False,可隐藏window.navigator.webdriver这一DOM属性
        profile.set_preference("dom.webdriver.enabled", False)
        profile.set_preference("window.navigator.webdriver", False)
        profile.set_preference('permissions.default.stylesheet', 2)
        profile.set_preference('permissions.default.image', 2)
        profile.set_preference("javascript.enabled", False)
        profile.set_preference("browser.download.folderList", 2)

        driver = Firefox(executable_path=f"{directory}/google/geckodriver.exe", firefox_profile=profile, options=options)
        # driver.get('https://login.taobao.com/member/login.jhtml')
        driver.get(login_url)
        with open(f'{directory}/google/stealth.min.js') as f:
            js = f.read()
        driver.execute_script(js)
        time.sleep(3)
        driver.find_element_by_xpath('//*[@id="fm-login-id"]').send_keys(username)
        time.sleep(1)
        driver.find_element_by_xpath('//*[@id="fm-login-password"]').send_keys(password)
        time.sleep(3)
        self.slider_unit(driver)
        driver.find_element_by_xpath('//*[@id="login-form"]/div[4]/button').click()
        time.sleep(5)

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
        time.sleep(10)
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
            if cookie.get("name") == 'cookie2' or cookie.get("name") == 'x5se':
                coo = "{}={};".format(cookie.get("name"), cookie.get("value"))
                cookies += coo
        print(cookies)
        return cookies

    def wcookie(self):
        # 写入cookie
        fzcookie = self.fzcookie()
        if fzcookie == 'cookie失效':
            return False
        fo = open(f"{directory}/feizhu_unit/cookie2.txt", "w")
        fo.write(fzcookie)
        fo.close()
        return True

    def rcookie(self):
        # 读取文件cookie
        fo = open(f"{directory}/feizhu_unit/cookie2.txt", "r")
        fzcookie = fo.readline()
        fo.close()
        return fzcookie
    def slider_unit(self, driver):
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
