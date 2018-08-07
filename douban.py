import time
import logging
from uuid import uuid4
from itertools import count
import fire
import requests
from config import posts
from utils import config_log, load_cookies, request, config_driver


class DouBan:

    def __init__(self, username):
        self.driver = config_driver()
        self.username = str(username)
        config_log(self.username)
        load_cookies(self.driver, self.username)
        self.posts = posts.get(self.username)
        self.up_posts()

    def request(self, url):
        logging.info('requesting %s', url)
        request(self.driver, url, self.username)

    def up_posts(self):
        len_posts = len(self.posts)
        for index in count(1):
            url = self.posts[index % len_posts]
            if self.up_post(url) is False:
                continue
            time.sleep(10 * 60)

    def up_post(self, url):
        self.request(url)
        self.driver.find_element_by_class_name('comment_textarea').send_keys(str(uuid4()))
        time.sleep(5)
        try:
            img_url = self.driver.find_element_by_id('captcha_image').get_attribute('src')
            word = requests.post('http://39.107.86.245:5001/', data={'img_url': img_url}).text
            word = word.replace('"', '').replace('\n', '').strip()
            while 1:
                logging.info('word %s    img_url: %s', word, img_url)
                if word:
                    break
                self.driver.refresh()
                logging.info('refresh %s', url)
                time.sleep(61)
                img_url = self.driver.find_element_by_id('captcha_image').get_attribute('src')
                word = requests.post('http://39.107.86.245:5001/', data={'img_url': img_url}).text

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