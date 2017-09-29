from selenium import webdriver
import selenium.webdriver.support.ui as ui
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
import os

class YoutubePlayer:
    url = "https://www.youtube.com/"
    def __init__(self):
        #driver = webdriver.PhantomJS(executable_path="/home/douasin/youtube_skip/phantomjs-2.5.0-beta-ubuntu-xenial/bin/phantomjs")
        self.black_sheet = self.load_black_sheet()
        self.has_ad = False
        self.current = None
        self.duration = None
        self.driver = webdriver.Chrome("../chromedriver")
        self.wait = ui.WebDriverWait(self.driver, 10)
        self.go_to_youtube_homepage()
        self.total_skip_ad = 0

    def load_black_sheet(self):
        black_sheet = []
        if os.path.exists('black_sheet.txt'):
            print("Find Black Sheet")
            with open('black_sheet.txt', 'r') as finn:
                for i in  finn.readlines():
                    black_sheet.append(i.strip())

        else:
            print("Doesn't find black_sheet.txt.")
            print("You can create one.")

        return black_sheet

    def go_to_youtube_homepage(self):
        self.driver.get(YoutubePlayer.url)
        sleep(1)

    def choose_do(self):
        print("1: Search Song")
        print("2: Start or Stop")
        #youtube.next_button.click()

    def search_box(self):
        #return self.driver.find_element_by_class_name(
        #        "ytd-searchbox")
        return self.driver.find_element_by_id("search")

    def lookup_time(self):
        self.hover_on_video()
        sleep(0.2)
        self.current  = self.left_time()
        self.duration = self.right_time()
        self.hover_out()

    def left_time(self):
        try:
            time_current = self.driver.find_element_by_class_name(
                    "ytp-time-current")
            return time_current.get_attribute('textContent')
            #return time_current.text
        except:
            return None

    def right_time(self):
        try:
            time_duration = self.driver.find_element_by_class_name(
                    "ytp-time-duration")
            self.hover_out()
            return time_duration.get_attribute('textContent')
            #return time_duration.text
        except:
            return None

    def check_end(self):
        if self.current and self.duration:
            return self.current == self.duration
        else:
            return False

    def player(self):
        return self.driver.find_element_by_class_name(
                "html5-video-container")

    def time_display(self):
        return self.driver.find_element_by_class_name(
                "ytp-time-display")

    def play_button(self):
        return self.driver.find_element_by_class_name(
                "ytp-play-button")

    def next_button(self):
        return self.driver.find_element_by_class_name(
                "ytp-next-button")

    def next_video(self):
        videos = self.driver.find_elements_by_id(
                "video-title")
        videos = [i for i in videos if i.is_displayed()]

        return videos[0]

    def go_next_video(self):
        self.current = None
        self.duration = None
        self.next_video().click()
        sleep(1)

    def title(self):
        return self.driver.title

    def search_and_go_first(self, search_word):
        search_box = self.driver.find_element_by_id('search')
        search_box.send_keys(search_word)
        search_box.send_keys(Keys.ENTER)
        sleep(1)
        video_items = self.driver.find_elements_by_id("thumbnail")
        video_items = [i for i in video_items if i.is_displayed()]
        video_items[0].click()
        sleep(1)

    def hover_on_video(self):
        hover = ActionChains(self.driver).move_to_element(
                self.driver.find_element_by_class_name(
                    "html5-main-video"))
        hover.perform()

    def hover_out(self):
        hover = ActionChains(self.driver).move_to_element(
                self.driver.find_element_by_class_name(
                    "yt-view-count-renderer"))
        hover.perform()

    def check_ad(self):
        try:
            self.driver.find_element_by_class_name("videoAdUiPreSkipButton").click()
            self.has_ad = True
            return self.driver.find_element_by_class_name("videoAdUiPreSkipText").text
        except:
            return None

    def skip_ad(self):
        try:
            self.has_ad = False
            self.total_skip_ad += 1
            print("已跳過{}個廣告".format(self.total_skip_ad))
            self.driver.find_element_by_class_name("videoAdUiSkipButton").click()
            sleep(1)
            #return self.driver.find_element_by_class_name("videoAdUiSkipButtonExperimentalText").text
        except:
            return None

    def check_hate(self):
        title = self.title().lower()
        for hate in self.black_sheet:
            if hate in title:
                return True
        return False

if __name__ == "__main__":
    def prints(text):
        print(" "*os.get_terminal_size().columns, end="\r")
        print(text, end="\r")

    def print_hr():
        print("-"*os.get_terminal_size().columns)

    youtube = YoutubePlayer()
    search_word = input("Please input a keyword: ")
    now_title = youtube.title()

    youtube.search_and_go_first(search_word)
    while True:
        if now_title != youtube.title():
            print_hr()
            now_title = youtube.title()
            print(now_title)
            try:
                print("next: {}".format(youtube.next_video().text))
            except:
                pass

        else:
            youtube.lookup_time()
            prints("{}/{}".format(youtube.current, youtube.duration))

        ad_word = youtube.check_ad()
        if youtube.has_ad:
            if ad_word:
                print(ad_word)
            else:
                youtube.skip_ad()

        elif youtube.check_end():
            youtube.go_next_video()

        elif youtube.check_hate():
            print("You hate '{}'".format(youtube.title()))
            print("Skipping....")
            youtube.go_next_video()

        #youtube.choose_do()
        sleep(1)
