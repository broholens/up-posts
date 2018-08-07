import json
import time
import logging
import requests
from selenium import webdriver


def save_cookies(driver, username):
    """save driver cookie to file"""
    json_cookies = json.dumps(driver.get_cookies())
    with open(username+'.json', 'w') as f:
        f.write(json_cookies)


def load_cookies(driver, username):
    """load file cookies to driver"""
    with open(username+'.json', 'r') as f:
        cookies = json.loads(f.read())
    driver.get('https://www.baidu.com/')
    driver.delete_all_cookies()

    for cookie in cookies:
        driver.add_cookie(cookie)


def request(driver, url, username):
    """driver request and update cookie"""
    try:
        driver.get(url)
        time.sleep(3)
        # update cookies
        save_cookies(driver, username)
    except:
        time.sleep(60)


def config_log(username):
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname)s %(message)s',
        datefmt='%d %b %Y %H:%M:%S',
        filename=username + '.log',
        filemode='a'
    )
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter(
        '%(asctime)s %(levelname)s %(message)s',
        datefmt='%d %b %Y %H:%M:%S'
    )
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)


def config_driver(headless=True):
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'
    opts = webdriver.ChromeOptions()
    opts.add_argument(f'user-agent={user_agent}')
    if headless is True:
        opts.add_argument('headless')
        opts.add_argument('no-sandbox')
    driver = webdriver.Chrome(chrome_options=opts)
    driver.set_page_load_timeout(3 * 60)
    return driver


def send_mail(content):
    mail_uri = 'http://39.107.86.245:5000'
    mail = {
        'recipient': 'zzwcng@126.com',
        'subject': 'HuPu',
        'content': content
    }
    requests.post(mail_uri, mail)

