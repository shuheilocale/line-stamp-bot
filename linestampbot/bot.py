import os
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys as keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver import FirefoxProfile

class LineStampBot():

    def __init__(self, config):
        self.config = config

    def line_login(self, driver):
        
        url = "https://creator.line.me/ja/"
        driver.get(url)

        # ラインアワード用
        #close_btn = driver.find_element_by_css_selector(".mdAwardPop2017BtnClose")
        #close_btn.click()

        # ログイン
        if False : #マニュアル
            time.sleep(10)
        else:
            time.sleep(2)
            login_btn = driver.find_element_by_css_selector(".mdGHD02Manager > a")
            login_btn.click()
            addr = driver.find_element_by_css_selector(".MdInputTxt01.mdInputTxt01Mail > input")
            addr.send_keys(self.config["mail"])
            passwd = driver.find_elements_by_css_selector(".MdInputTxt01")[1].find_element_by_css_selector("input")
            passwd.send_keys(self.config["password"])
            passwd.send_keys(keys.ENTER)

        # 着せ替え用
        time.sleep(2)
        close_btns = driver.find_elements_by_css_selector(".FnCloseDialogBtn.mdBtn")
        for b in close_btns:
            if b.text.find("閉じる") != -1:
                b.click()
                break
        
        # 人気キャラクター
        time.sleep(2)
        close_btns = driver.find_elements_by_css_selector(".FnCloseDialogBtn.mdBtn")
        for b in close_btns:
            if b.text.find("閉じる") != -1:
                b.click()
                break
        
        # クリエータースタジオ
        time.sleep(2)
        close_btns = driver.find_elements_by_css_selector(".FnCloseDialogBtn.mdBtn")
        for b in close_btns:
            if b.text.find("閉じる") != -1:
                b.click()
                break
    

    def register_stamp(self, driver, name, name_table):

        while True:
            # 新規登録
            new_stamp_a = driver.find_elements_by_css_selector(".mdBtn")[0]
            new_stamp_a.click()

            # スタンプ
            new_stamp_a = driver.find_elements_by_css_selector(".mdBtn")[1]
            new_stamp_a.click()
        
            # 表示情報登録
            if not name in name_table:
                return False
        
            success = self.register_disp_info(driver, name, name_table[name])
            if success:
                print("break")
                break
            else:
                 return False
            time.sleep(3)

        # スタンプ登録とリクエスト
        #time.sleep(3)
        #image_url = driver.current_url + "#/image"
        #driver.get(image_url)
        driver.find_elements_by_css_selector(".mdCMN06Item")[1].click()
        ret = self.register_image(driver, name)
        if ret is False:    
            return False
        
        return True


    # 表示情報登録
    def register_disp_info(self, driver, name, name_info):
        time.sleep(3)
        
        # 日本語を追加
        selects = driver.find_elements_by_css_selector("select")
        lang_select_element = Select(selects[0])
        lang_select_element.select_by_index(1)
        btn = driver.find_elements_by_css_selector(".mdBtn")[1]
        btn.click()

        time.sleep(2)
        actions = ActionChains(driver)
        actions.send_keys(keys.TAB)

        time.sleep(1)
        items = driver.find_elements_by_css_selector(".ng-isolate-scope")
        items[0].send_keys(self.config["info"]["en-title"].format(name_info["r"]))
        items[0].click()
        actions.perform()

        time.sleep(1)
        items[1].send_keys(self.config["info"]["en-description"].format(name_info["r"]))

        time.sleep(1)
        items[2].send_keys(self.config["info"]["jp-title"].format(name))
        items[2].click()
        actions.perform()

        kanji =""
        for k in name_info["k"]:
            if( len(kanji) > 50):
                break
            else:
                kanji += k
                kanji += "/"

        items[3].send_keys(self.config["info"]["jp-description"].format(name, kanji))
        items[4].send_keys("shey")

        time.sleep(2)
        text_select_element = Select(selects[1])
        text_select_element.select_by_index(7)
        chara_select_element = Select(selects[2])
        chara_select_element.select_by_index(12)

        # 販売エリア
        radio = driver.find_elements_by_css_selector(".mdInputRadio > input")[4]
        radio.click()

        time.sleep(1)
        driver.find_elements_by_css_selector(".MdCMN28AreaListItem.ng-scope")[0].click()

        # インドネシアだけ外す。
        time.sleep(2)
        driver.find_elements_by_css_selector("label.MdCMN28AreaListCountry.ng-scope > input")[3].click()
        #driver.find_elements_by_css_selector("label.MdCMN28AreaListCountry.ng-scope > input")[1].click()
        #driver.find_elements_by_css_selector("label.MdCMN28AreaListCountry.ng-scope > input")[2].click()
        #driver.find_elements_by_css_selector("label.MdCMN28AreaListCountry.ng-scope > input")[4].click()
        #driver.find_elements_by_css_selector("label.MdCMN28AreaListCountry.ng-scope > input")[5].click()

        # クリスマス
        #driver.find_elements_by_css_selector(".mdInputLabel")[7].click()
        #time.sleep(1)

        # 保存
        time.sleep(2)
        driver.find_elements_by_css_selector(".mdBtnLabel")[-1].click()
        time.sleep(3)
        len_btn = len(driver.find_elements_by_css_selector(".mdBtn"))
        print(len_btn)

        found = False
        btns = driver.find_elements_by_css_selector(".mdBtn")
        for b in btns:
            if b.text.find("OK") != -1:
                found = True
                b.click()
                break

        if not found:   
            print("OK not found")
            return False
        

        time.sleep(5)
        return True

    # スタンプ登録
    def register_image(self, driver, name):
        time.sleep(3)

        # エラーチェック
        is_limit = False
        if len(driver.find_elements_by_css_selector(".mdCMN23Error")) > 0:
            clss_list = driver.find_elements_by_css_selector(".mdCMN23Error")
            for c in clss_list:
                cls = c.get_attribute("class")
                if cls.find("ng-hide") < 0:       
                    is_limit = True

        # 編集ボタン
        print("編集ボタン")
        driver.find_elements_by_css_selector("a.mdBtn")[3].click()

        # スタンプ個数変更
        time.sleep(2)
        select = driver.find_element_by_css_selector("select")
        image_num_select = Select(select)
        image_num_select.select_by_index(4)
        time.sleep(2)


        driver.find_elements_by_css_selector("a.mdBtn")[17].click()

        time.sleep(3)

        # 画像登録
        zipfmt = os.path.join(self.config["zipdir"],"{}.zip")
        driver.find_element_by_css_selector('input[type="file"]').send_keys(zipfmt.format(name))
        time.sleep(10)

        # 戻る
        driver.find_element_by_css_selector(".MdBtn01.mdBtn01Cr02").click()
        time.sleep(3)

        # 申請
        if not is_limit:
            driver.find_element_by_css_selector(".mdBtnLabel").click()
            time.sleep(2)
            driver.find_element_by_css_selector(".mdInputCheck.ng-pristine.ng-invalid.ng-invalid-required").click()
            time.sleep(2)
            driver.find_elements_by_css_selector("span.MdBtn01.mdBtn01Cr01")[5].click()
            time.sleep(3)

    def check_sticker_status(self, driver, url):
        driver.get(url)

        if driver.current_url != url:
            print(driver.current_url, url)
            return False

        status_list = []
        tr_list = driver.find_elements_by_css_selector("tr.mdCMN11Row")[1:]
        for tr in tr_list:
            name = tr.find_elements_by_css_selector("td")[1].get_attribute('innerHTML')
            sid = tr.find_elements_by_css_selector("td")[2].get_attribute('innerHTML')
            status = tr.find_elements_by_css_selector("td")[5].find_element_by_css_selector("span").get_attribute('innerHTML')
            status_list.append({"name": name, "sid": sid, "status": status})
        return status_list

    def apply(self, driver):

        page = 21
        base_url = "https://creator.line.me/my/{}/sticker/?page={}"
        cur_sticker_list = self.check_sticker_status(driver, base_url.format(self.config["userid"], page))
        sticker_list = []
        while(cur_sticker_list):
            sticker_list.extend(cur_sticker_list)
            page += 1
            cur_sticker_list = self.check_sticker_status(driver, base_url.format(self.config["userid"], page))
            if page > 21:
                break

        url_list = []
        for sticker in sticker_list:
            if sticker["status"] == "編集中":
                url = "https://creator.line.me/my/{}/sticker/{}".format(self.config["userid"],sticker["sid"])
                url_list.append(url)

        for url in url_list:
            self.apply_main(driver, url)


    def apply_main(self, driver, url):
        driver.get(url)
        time.sleep(3)
        driver.find_elements_by_css_selector(".mdBtnLabel")[0].click()
        time.sleep(1)
        driver.find_elements_by_css_selector("input[type='checkbox']")[-1].click()
        time.sleep(1)
        driver.find_elements_by_css_selector("a.mdBtn")[-1].click()
        time.sleep(3)

    def release(self, driver, f=1, t=100):

        page = f
        base_url = "https://creator.line.me/my/{}/sticker/?page={}"
        cur_sticker_list = self.check_sticker_status(driver, base_url.format(page))
        sticker_list = []
        while(cur_sticker_list):
            sticker_list.extend(cur_sticker_list)
            page += 1
            cur_sticker_list = self.check_sticker_status(driver, base_url.format(page))
            if page > t:
                break

        # print(sticker_list)

        for sticker in sticker_list:
            if sticker["status"] == "承認":
                url = "https://creator.line.me/my/{}/sticker/{}".format(self.config["userid"],sticker["sid"])
                driver.get(url)
                time.sleep(2)
                driver.find_elements_by_css_selector(".mdBtnLabel")[0].click()
                time.sleep(2)
                driver.find_elements_by_css_selector(".mdBtn")[-1].click()
            elif sticker["status"] == "編集中":
                print("編集中:" + sticker["name"] + ", " + sticker["sid"])
            elif sticker["status"] == "審査中":
                print("審査中:" + sticker["name"] + ", " + sticker["sid"])  

        return
