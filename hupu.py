import time
import logging
from random import choice
from queue import Queue
import fire
from utils import send_mail, load_cookies, request, config_log, config_driver


class HuPu:

    # 本日回帖数量
    comment_count = 0

    commentary = [
        '回收各种球鞋 aj 喷泡 椰子 实战 急用鞋换钱 闲置清理空间 全新二手皆可 打包优先 寻求多方合作 更多精彩尽在: clpro7',
        '朋友圈每日更新 各种秒价第一时间了解:clpro7',
        '最大限度发挥球鞋价值 接各种套现寄卖 全新二手都可以 加微信:clpro7 秒价实时更新',
        '加微信:clpro7 ',
        '接各种套现寄卖 全新二手都可以',
        '寻求多方合作',
        '回收各种球鞋',
        '急用鞋换钱 闲置清理空间 全新二手皆可'
    ]

    user_id = '131348617043133'

    post_count = 0

    def __init__(self, username):
        self.driver = config_driver()
        self.posts = Queue()
        self.max_error_num = 5
        self.username = str(username)
        config_log(self.username)
        load_cookies(self.driver, self.username)
        self.comment_posts()

    def retry(self):
        logging.error('retrying...')
        self.driver.quit()
        self.__init__(self.username)

    def get_posts_address(self):
        try:
            self.request('https://www.hupu.com/')
            if not self.user_id:
                self.user_id = self.driver.find_element_by_id('g_m').get_attribute('iuid')
            return 'https://my.hupu.com/{}/topic'.format(self.user_id)
        except:
            self.retry()

    def store_posts(self):
        try:
            posts_address = self.get_posts_address()
            self.request(posts_address)
            xp = '//table[@class="mytopic topiclisttr"]//a'
            links = self.driver.find_elements_by_xpath(xp)
            if self.post_count != 0:
                if self.post_count * 2 <= len(links):
                    links = links[:self.post_count * 2]
            posts, plates = links[::2], links[1::2]
            posts = [
                post.get_attribute('href')
                for post, plate in zip(posts, plates)
                if plate.text in ['二手交易区']
            ]
            for post in posts:
                self.posts.put(post)
            logging.info('posts have been updated!')
        except:
            self.retry()

    def request(self, url):
        request(self.driver, url, self.username)

    def comment_post(self, url, commentary):
        """添加评论"""
        self.request(url)
        self.driver.find_element_by_id('atc_content').send_keys(choice(commentary))
        self.driver.find_element_by_id('fastbtn').click()

    def comment_posts(self):
        element_error_counter = 0
        comment_error_counter = 0
        while True:
            while self.posts.empty():
                self.store_posts()
            post_url = self.posts.get()
            try:
                self.comment_post(post_url, self.commentary)
            except:
                logging.error('find element error %s', post_url)
                if element_error_counter > self.max_error_num:
                    logging.info('sending mail...')
                    send_mail('find element error too many times!')
                    self.retry()
                else:
                    element_error_counter += 1
                continue
            element_error_counter = 0
            time.sleep(60)

            if 'post.php?action=reply' in self.driver.current_url:
                failed_reason = self.driver.find_element_by_xpath(
                    '//*[@id="search_main"]//span').text
                logging.error('%s %s!', failed_reason, post_url)
                if '银行总资产少于' in failed_reason:
                    logging.info('sending mail...')
                    send_mail(failed_reason)
                    exit(0)
                else:
                    if comment_error_counter > self.max_error_num:
                        logging.info('sending mail...')
                        send_mail(f'连续回帖{self.max_error_num}次出错')
                        exit(0)
                    else:
                        comment_error_counter += 1
            elif '-last.html#o' in self.driver.current_url:
                self.comment_count += 1
                logging.info('评论 %s 成功!　已评论: %s', post_url, self.comment_count)
                comment_error_counter = 0
            else:
                logging.warning('unknown state %s', self.driver.current_url)
                comment_error_counter += 1

            time.sleep(60 * 3)


if __name__ == '__main__':
    fire.Fire(HuPu)
