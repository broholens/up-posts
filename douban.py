import time
import logging
from uuid import uuid4
from itertools import count
import fire
import requests
from config import douban
from utils import config_log, load_cookies, request, config_driver


class DouBan:

    def __init__(self, username):
        self.driver = config_driver()
        self.username = str(username)
        self.name = 'douban_' + self.username
        config_log(self.name)
        load_cookies(self.driver, self.name)
        self.posts = douban['posts'].get(self.username)
        self.up_posts()

    def request(self, url):
        logging.info('requesting %s', url)
        request(self.driver, url, self.name)

    def up_posts(self):
        len_posts = len(self.posts)
        for index in count(1):
            url = self.posts[index % len_posts]
            if self.up_post(url) is False:
                continue
            time.sleep(5 * 60)

    def up_post(self, url):
        identify_url = 'http://localhost:5001/'
        self.request(url)
        self.driver.find_element_by_class_name('comment_textarea').send_keys(str(uuid4()))
        time.sleep(5)
        try:
            img_url = self.driver.find_element_by_id('captcha_image').get_attribute('src')
            resp = requests.post(identify_url, data={'img_url': img_url})
            word = resp.json().get('word')
            while 1:
                logging.info('word %s    img_url: %s', word, img_url)
                if word:
                    break
                self.driver.refresh()
                logging.info('refresh %s', url)
                time.sleep(61)
                img_url = self.driver.find_element_by_id('captcha_image').get_attribute('src')
                word = requests.post(identify_url, data={'img_url': img_url}).json().get('word')

            captcha = self.driver.find_element_by_id('captcha_field')
            captcha.clear()
            captcha.send_keys(word.strip('"'))
        except:
            pass
        self.driver.find_element_by_name('submit_btn').click()
        time.sleep(60)
        logging.info('url after submit: %s', self.driver.current_url)
        if 'post=ok#last' not in self.driver.current_url:
            logging.error('up posts error! %s', url)
            return False
        logging.info('up posts successfully! %s', url)
        return True


if __name__ == '__main__':
    fire.Fire(DouBan)
