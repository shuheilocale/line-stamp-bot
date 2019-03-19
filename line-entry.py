import os
import json
import codecs
from datetime import datetime as dt
import calendar
import time
import argparse
import shutil
import glob
import inspect
import random

from selenium import webdriver
from selenium.webdriver.common.keys import Keys as keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver import FirefoxProfile
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

def location(depth=0):
  frame = inspect.currentframe().f_back
  return os.path.basename(frame.f_code.co_filename), frame.f_code.co_name, frame.f_lineno


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

def register_stamp(driver, name, name_table, CONFIG):

    # 新規登録
    try:
        new_stamp_a = driver.find_elements_by_css_selector(".mdBtn")[0]
        new_stamp_a.click()
    except:
        print("新規登録エラー", location())
        return False

    # スタンプ
    try:
        new_stamp_a = driver.find_elements_by_css_selector(".mdBtn")[1]
        new_stamp_a.click()
    except:
        print("新規登録エラー", location())
        return False
 
    # 表示情報登録
    if not name in name_table:
        return False

    ret = register_disp_info(driver, name, name_table[name], CONFIG)
    if ret is False:
        print("表示情報登録失敗")
        return False

    #time.sleep(100)


    # スタンプ登録とリクエスト
    driver.find_elements_by_css_selector(".mdCMN06Item")[1].click()
    ret = register_image(driver, name, CONFIG)
    if ret is False:
        print("スタンプ登録失敗")
        return False
    
    return True


# 表示情報登録
def register_disp_info(driver, name, romaji, CONFIG):

    time.sleep(3)
    try:
        # 日本語を追加
        selects = driver.find_elements_by_css_selector("select")
        lang_select_element = Select(selects[0])
        lang_select_element.select_by_index(1)
        btn = driver.find_elements_by_css_selector(".mdBtn")[1]
        btn.click()

        time.sleep(2)
        actions = ActionChains(driver)
        actions.send_keys(keys.TAB)

        items = driver.find_elements_by_css_selector(".ng-isolate-scope")
        dot = ""
        for i in range(random.randint(0, 3)):
            dot += "."

        items[0].send_keys(CONFIG["info"]["en-title"].format(romaji)+dot)
        items[0].click()
        actions.perform()

        items[1].send_keys(CONFIG["info"]["en-description"].format(romaji))

        items[2].send_keys(CONFIG["info"]["jp-title"].format(name))
        items[2].click()
        actions.perform()


        items[3].send_keys(CONFIG["info"]["jp-description"].format(name))
        items[4].send_keys(CONFIG["info"]["author"])

        time.sleep(2)
        text_select_element = Select(selects[1])
        text_select_element.select_by_index(6) # 1 かわいい 6シュール 7おもしろ
        chara_select_element = Select(selects[2])
        chara_select_element.select_by_index(12)


        # 販売エリア
        radio = driver.find_elements_by_css_selector(".mdInputRadio > input")[4]
        radio.click()

        time.sleep(1)
        driver.find_elements_by_css_selector(".MdCMN28AreaListItem.ng-scope")[0].click()

        # インドネシアだけ外す。
        time.sleep(2)
        ipt = driver.find_elements_by_css_selector("label.MdCMN28AreaListCountry.ng-scope > input")[3]
        ipt.click()
    except:
        raise

    # 保存
    try:
        time.sleep(3)
        WAIT_SECOND = 30
        WebDriverWait(driver, WAIT_SECOND).until(EC.visibility_of_element_located((By.CLASS_NAME, 'mdBtn')))

        driver.find_elements_by_css_selector(".mdBtnLabel")[1].click()
        time.sleep(3)
        btns = driver.find_elements_by_css_selector(".mdBtn")
        if len(btns) < 11:
            print(len(btns))
            return False
        
        # 説明文などでエラーが出て、保存を押せなかった場合の対応
        if btns[-1].tag_name.lower() != "a":
            print(btns[-1].tag_name)
            return False

        btns[-1].click()
        time.sleep(5)
        return True
    except:
        raise


# スタンプ登録
def register_image(driver, name, CONFIG):
    time.sleep(3)

    # エラーチェック
    """
    if len(driver.find_elements_by_css_selector(".mdCMN23Error")) > 0:
        clss_list = driver.find_elements_by_css_selector(".mdCMN23Error")
        for c in clss_list:
            cls = c.get_attribute("class")
            if cls.find("ng-hide") < 0:
                return False
    """

    # 編集ボタン
    driver.find_elements_by_css_selector("a.mdBtn")[3].click()

    time.sleep(5)
    select = driver.find_element_by_css_selector("select")
    image_num_select = Select(select)
    image_num_select.select_by_index(4)
    time.sleep(5)

    # スタンプ個数変更
    driver.find_elements_by_css_selector("a.mdBtn")[17].click()
    time.sleep(10)


    # 画像登録
    driver.find_element_by_css_selector('input[type="file"]').send_keys(os.path.join(CONFIG["zip-dir"], name + ".zip"))
    time.sleep(20)

    driver.find_elements_by_css_selector("a.mdBtn")[45].click()
    time.sleep(3)

    return True    ## 申請？
    driver.find_element_by_css_selector(".mdBtnLabel").click()
    time.sleep(1)
    regist_btn = find_element_by_css_selector_With_wait(driver, ".mdInputCheck.ng-pristine.ng-invalid.ng-invalid-required")
    if regist_btn is not None:
        regist_btn.click()
    else:
        return False
    time.sleep(1)


    btn = driver.find_elements_by_css_selector("span.MdBtn01.mdBtn01Cr01")[5]
    if btn is not None:
        btn.click()
    else:
        return False
    time.sleep(5)


def load_param(path):
    f = codecs.open(path,"r","utf-8")
    param = json.load(f)
    f.close()
    return param

def exec_line_entry(name_table, CONFIG, reverse):
    driver = create_driver()
    line_login(driver, CONFIG)
    

    fail_names = []

    zip_files = glob.glob(os.path.join(CONFIG["zip-dir"],"*.zip"))
    if reverse:
        zip_files.reverse()

    print(len(zip_files))

    for target_zip in zip_files:
        name = os.path.splitext(os.path.basename(target_zip))[0]
        print(name)

        if name in name_table:
        #if True:
            retry_cnt = 3
            for i in range(retry_cnt):
                ret = register_stamp(driver, name, name_table, CONFIG)
                if ret is False:
                    print("{} 登録失敗".format(name))
                    with open("fail-names.txt", "a") as f:
                        f.write(name)
                    fail_names.append(name)
                else:
                    done = os.path.join(CONFIG["zip-dir"], "done")
                    os.makedirs(done, exist_ok=True)
                    shutil.move(target_zip, done)
                    break
        else:
            print("{}：zipファイルなし".format(name))

    driver.close()

    return fail_names

def main():
    psr = argparse.ArgumentParser()
    psr.add_argument('-c', '--config', default='config.json')
    psr.add_argument('--reverse', action='store_true')
    args = psr.parse_args()

    CONFIG = load_param(args.config)
    #print(CONFIG)

    """
    f = codecs.open(CONFIG["name-table"], "r")
    name_table = json.loads(f.read())
    f.close()

    f = open(CONFIG["name-list"],"r")
    name = f.readline().strip()

    while(name):
        if name in names:
            continue
        names.append(name)
        name = f.readline().strip()
    f.close()

    """
    import csv

    f = open(CONFIG['last-name-list'], 'r', encoding="utf-8")
    reader = csv.reader(f)

    name_table = {}
    for row in reader:
        name_table[row[0]] = row[2]
    f.close()

    fail_names = exec_line_entry(name_table, CONFIG, args.reverse)

    return


    #fail_names = exec_line_entry(names, name_table, CONFIG)

    #print(fail_names)





if __name__ == '__main__': main()

