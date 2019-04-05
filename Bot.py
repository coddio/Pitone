from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
import re


browser=webdriver.Chrome('chromedriver.exe')

def login(username,password):
    browser.get('https:/twitter.com/login')

    username_field = browser.find_element_by_class_name('js-username-field')
    password_field = browser.find_element_by_class_name('js-password-field')

    username_field.send_keys(username)
    password_field.send_keys(password)

    password_field.send_keys(Keys.ENTER)

def readtweets(hashtag,max):
    browser.get('https://twitter.com/search?src=typd&q=%23'+hashtag)
    tweets = browser.find_elements_by_class_name('tweet-text')
    actionChain = webdriver.ActionChains(browser)
    regexurl = r"(http:\/\/www\.|https:\/\/www\.|http:\/\/|https:\/\/)?[a-z0-9]+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,5}(:[0-9]{1,5})?(\/.*)?"

    while len(tweets) < max:
        actionChain.key_down(Keys.SPACE).key_up(Keys.SPACE).perform()
        tweets = browser.find_elements_by_class_name('tweet-text')
        print(len(tweets))
    texts=[]
    for tweet in tweets:
        text = tweet.text.lower()

        #pulizia della stringa
        re.sub(r'\s',' ',text)
        text = re.sub(r"[#@][^\s]+", "", text)
        text = re.sub(regexurl, "", text)
        text = re.sub(r'[^a-zàèéòàùì ]', ' ', text)

        texts.append(text)
        print(text)

        if len(texts) == max:
            break

    print(len(texts))


login('datruemenace@gmail.com', 'KarlOKonty')
readtweets('masterchef',50)

browser.close()