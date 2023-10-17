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

from datetime import date

import traceback
# load_dotenv()


class TwitterTweetUnliker(object):
    def __init__(self, username=None, password=None, download_dir=None, headless=True, browser=None):
        self.LOGIN_URL = "https://twitter.com/login"
        self.PROFILE_URL = "https://twitter.com/{}/likes".format(username)
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
        self.browser.get(self.LOGIN_URL)

        # Wait till page is loaded
        try:
            WebDriverWait(self.browser, 10).until(
                EC.presence_of_element_located((By.NAME, "text"))
                # EC.presence_of_element_located(('input[autocomplete=username]'))
            )
        # Timeout of 10 seconds
        except TimeoutException:
            return Exception("Page didn't load")

        uname = self.browser.find_element(By.CSS_SELECTOR, ('input[autocomplete=username]')) #self.browser.find_element_by_name("username")
        try:
            uname.send_keys(self.username)
            nextButton = self.browser.find_element(By.XPATH, "//span[.='Next']")
            nextButton.click()
            try:
                WebDriverWait(self.browser, 10).until(
                    EC.presence_of_element_located((By.NAME, "password"))
            )
            # Timeout of 10 seconds
            except TimeoutException:
                return Exception("Page didn't load")
            pword = self.browser.find_element(By.NAME,"password")
            pword.send_keys(self.password)
        except TypeError:
            raise ValueError("Missing username/password")

        # Find the submit button
        # self.browser.find_element_by_xpath(
        #     "/html/body/div/div/div/div/main/div/div/form/div/div[3]/div/div"
        # ).click()
        self.browser.find_element(By.CSS_SELECTOR, "div[data-testid='LoginForm_Login_Button']").click()

        time.sleep(1)

        if self.browser.current_url == self.LOGIN_URL:
            raise Exception("Authentication Error")
        elif "locked" in self.browser.current_url:
            raise Exception("Account locked")

        authenticated = False
        while not authenticated:
            if "login_verification" in self.browser.current_url:
                auth_code = self.browser.find_element(By.NAME, "challenge_response")
                auth_code.clear()
                code = input("Enter 2fa code: ")
                auth_code.send_keys(code)
                self.browser.find_element(By.ID, "email_challenge_submit").click()
            else:
                authenticated = True

    def unlike_tweets(self):
    #   tweet = self.browser.find_element_by_xpath("//*[@id='react-root']/div/div/div[2]/main/div/div/div/div[1]/div/div[2]/div/section/div/div/div")
        # tweets = self.browser.find_elements(By.CSS_SELECTOR, 'article[data-testid="tweet"]')
        unlikes = self.browser.find_elements(By.CSS_SELECTOR, 'div[data-testid="unlike"]')
        print(len(unlikes))
        # for tweet in tweets:
        time.sleep(1)

        for unlike in unlikes:
            # unlike = tweet.find_element(By.CSS_SELECTOR, 'div[data-testid="unlike"]')
            self.browser.execute_script('arguments[0].scrollIntoView({block: "center"})', unlike)
            time.sleep(1)
            unlike.click()

            time.sleep(2)

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

    def unlike(self):
        

        # force_load = False

        # while force_load:
        #     self.scroll_up_and_down(20)
            
        #     keep_going = input('Continue trying? y/n ')
        #     force_load = keep_going == 'y'


        for itr in range(15):
            print("ITR: {}".format(itr))
            self.browser.get(self.PROFILE_URL)
            time.sleep(3)
            try:
                for _ in range(100):
                    self.unlike_tweets()
                    time.sleep(2)
            except Exception:
                traceback.print_exc()
                # self.browser.execute_script("window.scrollTo(0,0)")
                # self.browser.execute_script("window.scrollTo(0,700)")
                self.small_scroll()
