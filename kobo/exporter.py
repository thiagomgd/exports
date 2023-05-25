import os
import re
import time
from pathlib import Path
from urllib.request import urlopen
from pprint import pprint

# from dotenv import load_dotenv
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import traceback
import random 
# load_dotenv()

def human_type(element, text):
    for char in text:
        time.sleep(random.randint(0,1)) #fixed a . instead of a ,
        element.send_keys(char)

class KoboWishlistDownloader(object):
    def __init__(self, username=None, password=None, download_dir=None, headless=True, browser=None):
        # self.LOGIN_URL = 'https://authorize.kobo.com/ca/en/Signin?returnUrl=https%3a%2f%2fwww.kobo.com%2f'
        self.LOGIN_URL = 'https://kobo.com'
        self.WISHLIST_URL = "https://www.kobo.com/ca/en/account/wishlist"
        self.username = username
        self.password = password
        self.download_dir = download_dir
        # If not specified, try using env vars.
        # if self.username is None:
        # 	self.username = os.getenv("TWITTER_USERNAME")
        # if self.password is None:
        # 	self.password = os.getenv("TWITTER_PASSWORD")
        # if self.download_dir is None:
        # 	self.download_dir = os.getenv("TWITTER_DOWNLOAD_PATH")

        # Webdriver setup
        options = FirefoxOptions()
        if headless:
            options.add_argument("--headless")
        self.browser = webdriver.Firefox(options=options)

    # def __del__(self):
    #     self.browser.quit()

    def login(self):
        # self.browser.add_cookie(
        #     {
        #         "name":"sessionId",
        #         "value":"sessionid=b7afc242-6670-4e19-aecf-337874d1b2f2",
        #         "domain":".kobo.com",
        #         # "expiry":"2023-01-30T05:17:44.495Z",
        #         "secure":True
        #         })
        # self.browser.add_cookie(
        #     {
        #         "name":"session",
        #         "value":"ipCountry=CA&ip=70.36.62.60&affiliateid=514c8b9a-1fd8-4e35-9ffb-907fef14eee2&partnerid=00000000-0000-0000-0000-000000000001&platformid=00000000-0000-0000-0000-ffffffff0000&currency=CAD&merchcountry=CA&ult=&uid=Sf875HRepsKOcZ663KK_-bUAEYA=",
        #         "domain":".kobo.com",
        #         # "expiry":"Session",
        #         "secure":True
        #         })

        self.browser.get(self.LOGIN_URL)

        # # Wait till page is loaded
        # try:
        #     WebDriverWait(self.browser, 10).until(
        #         EC.presence_of_element_located((By.NAME, "LogInModel.UserName"))
        #         # EC.presence_of_element_located(('input[autocomplete=email]'))
        #     )
        # # Timeout of 10 seconds
        # except TimeoutException:
        #     return Exception("Page didn't load")

        # uname = self.browser.find_element_by_css_selector('input[autocomplete=email]') #self.browser.find_element_by_name("username")
        # try:
        #     time.sleep(random.randint(3,5))
        #     uname.click()
        #     human_type(uname, self.username)
        #     # uname.send_keys(self.username)
        #     # nextButton = self.browser.find_element_by_css_selector('input[autocomplete=current-password]')
        #     # nextButton.click()
        #     # try:
        #     #     WebDriverWait(self.browser, 10).until(
        #     #         EC.presence_of_element_located((By.NAME, "password"))
        #     # )
        #     # # Timeout of 10 seconds
        #     # except TimeoutException:
        #     #     return Exception("Page didn't load")
        #     time.sleep(random.randint(3,5))
        #     pword = self.browser.find_element_by_name("LogInModel.Password")
        #     pword.click()
        #     human_type(pword, self.password)
        #     # pword.send_keys(self.password)
        # except TypeError:
        #     raise ValueError("Missing username/password")

        # # Find the submit button
        # # self.browser.find_element_by_xpath(
        # #     "/html/body/div/div/div/div/main/div/div/form/div/div[3]/div/div"
        # # ).click()
        # self.browser.find_element_by_css_selector("button.sign-in-cta").click()

        # time.sleep(1)

        # if self.browser.current_url == self.LOGIN_URL:
        #     raise Exception("Authentication Error")
        # # elif "locked" in self.browser.current_url:
        # #     raise Exception("Account locked")

        # authenticated = False
        # while not authenticated:
        #     if "login_verification" in self.browser.current_url:
        #         auth_code = self.browser.find_element_by_name("challenge_response")
        #         auth_code.clear()
        #         code = input("Enter 2fa code: ")
        #         auth_code.send_keys(code)
        #         self.browser.find_element_by_id("email_challenge_submit").click()
        #     else:
        #         authenticated = True

    def get_bookmarks(self):
        self.browser.get(self.WISHLIST_URL)
        time.sleep(1)

        time.sleep(1)
        images = self.browser.find_elements_by_tag_name("img")
        urls = [img.get_attribute("src") for img in images]

        if not os.path.isdir(self.download_dir):
            os.mkdir(self.download_dir)

        for url in urls:
            if "media" in url:
                # driver.get(url)
                filename, format_ = os.path.split(url)[1].split("?")
                ext = re.findall("format=\w{3}", format_)[0].split("=")[1]
                img_data = urlopen(url).read()
                path = Path(self.download_dir, f"{filename}.{ext}")
                with open(path, "wb") as f:
                    f.write(img_data)
                print(f"Downloaded file to: {path}")

    def save_delete_bookmark(self, tweets_csv):
    #   tweet = self.browser.find_element_by_xpath("//*[@id='react-root']/div/div/div[2]/main/div/div/div/div[1]/div/div[2]/div/section/div/div/div")
        tweet = self.browser.find_element_by_css_selector('article[data-testid="tweet"]')
        # for tweet in tweets:
        tweet_link = tweet.find_element_by_css_selector('a[role="link"][dir="auto"],a[role="link"][dir="ltr"]')
        tweet_url = tweet_link.get_attribute("href")

        # tweet_profile = tweet.find_element_by_xpath('div/div/article/div/div/div/div[2]/div[2]/div[1]/div/div[1]/div[1]/div[1]/a/div/div[2]/div/span')
        # profile = tweet_profile.text[1:]
        tweet_id = tweet_url.split('/')[-1]
        profile = tweet_url.split('/')[-3]
        
        print(tweet_url, profile)
        # print(profile)

        images = tweet.find_elements_by_tag_name("img")
        img_urls = [img.get_attribute("src") for img in images]
        # pprint(img_urls)

        has_images = False
        # DOWNLOAD IMAGES
        for url in img_urls:
            if "media" in url:
                has_images = True
                # driver.get(url)
                filename, format_ = os.path.split(url)[1].split("?")
                fn = "{}_{}_{}".format(profile, tweet_id, filename)
                ext = re.findall("format=\w{3}", format_)[0].split("=")[1]
                img_data = urlopen(url).read()
                path = Path(self.download_dir, f"{fn}.{ext}")
                with open(path, "wb") as f:
                    f.write(img_data)
                print(f"Downloaded file to: {path}")

        # check if is video, link
        video = tweet.find_elements_by_css_selector("div[aria-label='Embedded video']")
        has_video = len(video) > 0 

        link_element = tweet.find_elements_by_css_selector("div[data-testid='card.wrapper']")
        has_link = len(link_element) > 0

        tweet_type = "textTweet"
        if has_link:
            tweet_type = "linkTweet"
        elif has_video:
            tweet_type = "videoTweet"
        elif has_images:
            tweet_type = "imageTweet"
      
        print('appending:',tweet_url, profile, tweet_type)
        # url,folder,tags
        tweets_csv.write('{},{},"Twitter: {},{}"\n'.format(tweet_url, 'Tweets', profile, tweet_type))

        # click share
        tweet.find_element_by_css_selector("div[aria-label='Share Tweet'][role='button']").click()
        # tweet.find_element_by_xpath('//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/div[2]/div/section/div/div/div[1]/div/div/article/div/div/div/div[2]/div[2]/div[2]/div[3]/div[4]/div').click()
        time.sleep(1)

        # remove bookmark
        # pprint(tweet.find_element_by_css_selector("div[data-testid='Dropdown']"))
        dropdown = tweet.find_element_by_xpath('//*[@id="layers"]/div[2]/div/div/div/div[2]/div/div[3]/div/div/div')
        # pprint(dropdown)
        # pprint(dropdown.find_elements_by_css_selector("div[role='menuitem']")[-1])
        dropdown.find_elements_by_css_selector("div[role='menuitem']")[-1].click()

        time.sleep(2)

    def scroll_down(self):
        self.browser.execute_script("window.scrollTo(0,document.body.scrollHeight/4)")
        time.sleep(1)
        self.browser.execute_script("window.scrollTo(0,document.body.scrollHeight/2)")
        time.sleep(1)
        self.browser.execute_script("window.scrollTo(0,document.body.scrollHeight/1.25)")
        time.sleep(1)
        self.browser.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        time.sleep(1)

    def scroll_up(self):
        self.browser.execute_script("window.scrollTo(0,document.body.scrollHeight/1.25)")
        time.sleep(1)
        self.browser.execute_script("window.scrollTo(0,document.body.scrollHeight/2)")
        time.sleep(1)
        self.browser.execute_script("window.scrollTo(0,document.body.scrollHeight/4)")
        time.sleep(1)
        self.browser.execute_script("window.scrollTo(0,0)")
        time.sleep(1)

    def scroll_up_and_down(self, times=5):
        for _ in range(times):
            self.scroll_down()
            self.scroll_up()
        
    def small_scroll(self):
        self.browser.execute_script("window.scrollTo(0,document.body.scrollHeight/4)")
        time.sleep(1)
        self.browser.execute_script("window.scrollTo(0,0)")
        time.sleep(1)

    def save_and_delete_bookmarks(self):
        with open("{}_tweets.csv".format(self.username), "a") as tweets_csv:
            self.browser.get(self.WISHLIST_URL)
            time.sleep(3)

            force_load = True

            while force_load:
                self.scroll_up_and_down(20)
                
                keep_going = input('Continue trying? y/n ')
                force_load = keep_going == 'y'


            for itr in range(15):
                print("ITR: {}".format(itr))

                try:
                    for _ in range(100):
                        self.save_delete_bookmark(tweets_csv)
                        time.sleep(2)
                except Exception:
                    traceback.print_exc()
                    self.small_scroll()

                    # self.browser.refresh()
                    # time.sleep(4)


