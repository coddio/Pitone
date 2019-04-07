from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep,time
import re


browser=webdriver.Chrome('chromedriver.exe')


#funzione che logga su twitter dati username e password
def login(username,password):
    browser.get('https:/twitter.com/login')

    username_field = browser.find_element_by_class_name('js-username-field')
    password_field = browser.find_element_by_class_name('js-password-field')

    username_field.send_keys(username)
    password_field.send_keys(password)

    password_field.send_keys(Keys.ENTER)


#la funzione cerca un determinato hashtag su twitter dato e legge e salva in una lista un numero max di tweet procede poi a rifinire i tweet
def readtweets(hashtag,max):
    browser.get('https://twitter.com/search?src=typd&q=%23'+hashtag)
    tweets = browser.find_elements_by_class_name('tweet-text')
    actionChain = webdriver.ActionChains(browser)
    regexurl = r"(http:\/\/www\.|https:\/\/www\.|http:\/\/|https:\/\/)?[a-z0-9]+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,5}(:[0-9]{1,5})?(\/.*)?"

    chrono1 = time()
    temp=len(tweets)
    while len(tweets) < max:
        actionChain.key_down(Keys.SPACE).key_up(Keys.SPACE).perform()
        tweets = browser.find_elements_by_class_name('tweet-text')
        print(len(tweets))
        if time() - chrono1 > 10:
            if temp == len(tweets):
                break
            else:
                chrono1=time()
                temp=len(tweets)
    texts=[]

    for tweet in tweets:
        text = tweet.text.lower()

        #pulizia della stringa
        re.sub(r'\s',' ',text)
        text = re.sub(r"[#@][^\s]+", "", text)
        text = re.sub(regexurl, "", text)
        text = re.sub(r'[^a-zàèéòàùì ]', ' ', text)
        text = re.sub(r"[\s]+"," ",text)

        texts.append(text)
        print('\n'+text)

        if len(texts) == max:
            break
    out=[]
    for el in texts:
        el = el.split()
        out+=el

    return out

#funzione simile a readtweets ma per google maps (NON ANCORA PRESENTE PARTE DI RIFINITURA STRINGA)
def readmaps(place,ty,max):
    regexurl = r"(http:\/\/www\.|https:\/\/www\.|http:\/\/|https:\/\/)?[a-z0-9]+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,5}(:[0-9]{1,5})?(\/.*)?"
    la=place.split()
    Url="https://www.google.com/maps/search/"
    for el in la:
       Url+=el
    browser.get(Url)
    sleep(5)
    href= browser.find_element_by_class_name('widget-pane-link')
    href.click()
    sleep(2)
    try:
        combo = browser.find_element_by_class_name('section-tab-info-stats-button-flex')
        combo.click()
        sleep(1)
        if ty == "bad":
            lowest = browser.find_element_by_xpath('//*[@id="action-menu"]/div[4]')
            lowest.click()
        elif ty == "good":
            highest = browser.find_element_by_xpath('//*[@id="action-menu"]/div[3]/div[2]')
            highest.click()
    except:
        combo = browser.find_element_by_class_name('section-dropdown-menu-button-caption')
        combo.click()
        sleep(1)
        if ty == "bad":
            lowest = browser.find_element_by_xpath('//*[@id=":j"]/div')
            lowest.click()
        elif ty == "good":
            highest = browser.find_element_by_xpath('//*[@id=":i"]/div')
            highest.click()

    sleep(2)
    actionChain = webdriver.ActionChains(browser)
    desel=browser.find_element_by_class_name('section-tab-info-stats-button-helper-text')
    actionChain.move_to_element_with_offset(desel, 5, 2)
    actionChain.click()
    actionChain.perform()
    rewiews = browser.find_elements_by_class_name('section-review-text')
    while len(rewiews)<max:
        actionChain.key_down(Keys.SPACE).key_up(Keys.SPACE).perform()
        rewiews = browser.find_elements_by_class_name('section-review-text')
    if len(browser.find_elements_by_class_name("section-expand-review"))!=0:
        for el in browser.find_elements_by_class_name("section-expand-review"):
            el.click()
        rewiews = browser.find_elements_by_class_name('section-review-text')

    out=[]
    for fun in rewiews:
        if fun.text != "":
            text=fun.text.lower()
            # pulizia della stringa
            re.sub(r'\s', ' ', text)
            text = re.sub(r"[#@][^\s]+", "", text)
            text = re.sub(regexurl, "", text)
            text = re.sub(r'[^a-zàèéòàùì ]', ' ', text)
            text = re.sub(r"[\s]+", " ", text)

            out += text.split()
        if len(out)==max:
            break
    return out

def mapsboth(place,max):
    out=[]
    out.append(readmaps(place,'good',max))
    sleep(1)
    out.append(readmaps(place, 'bad', max))
    return out

def analyzesaveboth(lst):
    savedata('good',analyzelist(lst[0]))
    savedata('bad', analyzelist(lst[1]))

#crea un dizionario e assegna a ogni parola, presa una sola volta, della lista un valore dato dal numero di volte che compare
def analyzelist(lst):
    dic = {}
    for el in lst:
        if el not in dic:
            dic[el]=1
        else:
            dic[el]+=1
    return(dic)


#salvail dizionario in un file negativo o positivo o lo aggiunge al file se giá esistente
def savedata(gb,dic):
    try:
        if gb=='bad':
            file=open('badfile.biasbot')
        elif gb =='good':
            file=open('goodfile.biasbot')

        for line in file:
            read=eval(line)
        file.close()
    except:
        read = {}

    if type(read) != dict:
        read = {}

    for i in dic:
        if i in read:
            read[i] += dic[i]
        else:
            read[i] = dic[i]

    if gb == 'bad':
        file = open('badfile.biasbot','w')
    elif gb == 'good':
        file = open('goodfile.biasbot','w')

    file.write(str(read))





lst = mapsboth("mcdonalds milano duomo",50)
print (lst)
analyzesaveboth(lst)

browser.close()
