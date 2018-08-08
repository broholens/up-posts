import time
import fire
from utils import CookieGetter


class HuPuCookieGetter(CookieGetter):
    """hupu.com  need to slide block by yourself"""
    def login(self):
        self.driver.get('https://passport.hupu.com/pc/login')
        time.sleep(3)
        self.driver.find_element_by_id('J_username').send_keys(self.username)
        self.driver.find_element_by_id('J_pwd').send_keys(self.passwd)
        while self.driver.current_url != 'https://www.hupu.com/':
            time.sleep(3)


class DouBanCookieGetter(CookieGetter):
    """douban.com"""
    def login(self):
        self.driver.get('https://www.douban.com/accounts/login')
        time.sleep(3)
        self.driver.find_element_by_id('email').send_keys(self.username)
        self.driver.find_element_by_id('password').send_keys(self.passwd)
        self.driver.find_element_by_id('remember').click()
        self.driver.find_element_by_class_name('btn-submit').click()
        while self.driver.current_url != 'https://www.douban.com/':
            time.sleep(3)


def start(name, username, password):
    getter = {'douban': DouBanCookieGetter, 'hupu': HuPuCookieGetter}.get(name)
    if not getter:
        print('name is invalid!')
        return
    getter(name, username, password)


if __name__ == '__main__':
    fire.Fire(start)