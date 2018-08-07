import time
import fire
from utils import save_cookies, config_driver


class CookieGetter:
    """login and save cookie to json file"""
    def __init__(self, username, passwd):
        self.driver = config_driver(headless=False)
        self.username = str(username)
        self.passwd = str(passwd)
        self.save_cookies()

    def login(self):
        pass

    def save_cookies(self):
        self.login()
        save_cookies(self.driver, self.username)
        print('cookies saved!')
        self.driver.quit()


class HuPuCookieGetter(CookieGetter):
    """hupu.com"""
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


def start(website, username, password):
    websites = {
        'hupu': HuPuCookieGetter,
        'douban': DouBanCookieGetter
    }
    website = websites.get(website)
    if not website:
        print('available websites: ')
        print('    ' + ', '.join(websites.keys()))
    else:
        website(username, password)


if __name__ == '__main__':
    fire.Fire(start)