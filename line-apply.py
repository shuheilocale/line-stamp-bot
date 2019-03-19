import os
import json
import codecs
from datetime import datetime as dt
import calendar
from selenium import webdriver
from selenium.webdriver.common.keys import Keys as keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver import FirefoxProfile
import time
import argparse

"""ドライバ生成"""
def create_driver():
    #driver = webdriver.Chrome("chromedriver.exe")
    custom_profile = FirefoxProfile()
    custom_profile.set_preference("dom.disable_beforeunload", True)
    driver = webdriver.Firefox(firefox_profile=custom_profile, executable_path="geckodriver.exe")
    driver.implicitly_wait(10)
    return driver


def find_element_by_css_selector_With_wait(driver, str, retry_count=10):
    for i in range(retry_count):
        try:
            elem = driver.find_element_by_css_selector(str)
            return elem
        except:
            time.sleep(2)
            pass
    return None

def find_elements_by_css_selector_With_wait(driver, str, retry_count=10):
    for i in range(retry_count):
        try:
            elem = driver.find_elements_by_css_selector(str)
            return elem
        except:
            time.sleep(2)
            pass
    return None

def line_login(driver, CONFIG):
    
    url = "https://creator.line.me/ja/"
    driver.get(url)


    # ラインアワード用
    #close_btn = driver.find_element_by_css_selector(".mdAwardPop2017BtnClose")
    #close_btn.click()

    # ログイン
    time.sleep(2)
    login_btn = driver.find_element_by_css_selector(".mdGHD02Manager > a")
    login_btn.click()
    time.sleep(1)

    addr = driver.find_element_by_css_selector(".MdInputTxt01.mdInputTxt01Mail > input")
    addr.send_keys(CONFIG["mail"])
    passwd = driver.find_elements_by_css_selector(".MdInputTxt01")[1].find_element_by_css_selector("input")
    passwd.send_keys(CONFIG["password"])
    #passwd.send_keys(keys.ENTER)
    driver.find_element_by_css_selector(".MdBtn03Login").click()
    time.sleep(4)

    # 敬語スタンプ
    close_btn = driver.find_elements_by_css_selector(".FnCloseDialogBtn.mdBtn")[-1]
    close_btn.click()
    ''' 

    # ラブスタンプ
    time.sleep(3)
    close_btn = driver.find_elements_by_css_selector(".FnCloseDialogBtn.mdBtn")[1]
    #print(close_btn)
    close_btn.click()
    ''' 

    # 着せ替え用
    '''
    time.sleep(5)
    close_btn = driver.find_elements_by_css_selector(".FnCloseDialogBtn.mdBtn")[2]
    print(close_btn)
    close_btn.click()

    # 許可承認
    time.sleep(2)
    yes_btn = driver.find_element_by_css_selector(".button-type-a.yes")
    yes_btn.click()

  
    # クリエータースタジオ
    time.sleep(2)
    close_btn = driver.find_element_by_css_selector(".FnCloseDialogBtn.mdBtn")
    close_btn.click()
    '''
def check_sticker_status(driver, url):
    driver.get(url)

    if driver.current_url != url:
        print(driver.current_url,url)
        return False

    status_list=[]
    tr_list = driver.find_elements_by_css_selector("tr.mdCMN11Row")[1:]
    #print(len(tr_list))
    for tr in tr_list:
        name = tr.find_elements_by_css_selector("td")[1].get_attribute('innerHTML')
        sid = tr.find_elements_by_css_selector("td")[2].get_attribute('innerHTML')
        status = tr.find_elements_by_css_selector("td")[5].find_element_by_css_selector("span").get_attribute('innerHTML')
        status_list.append({"name" : name, "sid" : sid, "status" :status})
    return status_list

        

def crawl_site(driver):
    pass


def load_param(path):
    f = codecs.open(path,"r","utf-8")
    param = json.load(f)
    f.close()
    return param

def exec_line_apply(CONFIG):
    driver = create_driver()
    line_login(driver, CONFIG)


    # bVxrmBVLUSqOE1iG りさ
    # V3zWWv129tihG9ax 修平
    page = 1
    base_url = "https://creator.line.me/my/{}/sticker/?page={}"
    cur_sticker_list = check_sticker_status(driver, base_url.format(CONFIG["id"],page))
    sticker_list = []
    while(cur_sticker_list):
        sticker_list.extend(cur_sticker_list)
        page += 1
        cur_sticker_list = check_sticker_status(driver, base_url.format(CONFIG["id"], page))
        if page > 5:
            break

    print(sticker_list)

    for sticker in sticker_list:
        if sticker["status"] == "編集中":
            url = "https://creator.line.me/my/{}/sticker/{}".format(CONFIG["id"], sticker["sid"])
            driver.get(url)
            time.sleep(2)
            driver.find_element_by_css_selector(".mdBtnLabel").click()
            time.sleep(2)
            driver.find_element_by_css_selector(".mdInputCheck").click()
            time.sleep(2)
            driver.find_elements_by_css_selector(".mdBtn")[-1].click()
            
        
    driver.close()

    return 

def main():
    psr = argparse.ArgumentParser()
    psr.add_argument('-c', '--config', default='config.json')
    args = psr.parse_args()

    CONFIG = load_param(args.config)
    #print(CONFIG)

    exec_line_apply(CONFIG)






if __name__ == '__main__': main()
