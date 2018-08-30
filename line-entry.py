import os
import json
import codecs
import time
import argparse
from linestampbot.bot import LineStampBot
from linestampbot.webdriver import create_driver

def load_param(path):
    f = codecs.open(path,"r","utf-8")
    param = json.load(f)
    f.close()
    return param


def main():
    psr = argparse.ArgumentParser()
    psr.add_argument('-c', '--config', default='config.json')
    args = psr.parse_args()

    f = codecs.open("name_dict_man_opti.json", "r", "utf-8")
    name_table = json.load(f)
    f.close()

    f = codecs.open("m.txt","r", "utf-8")
    name = f.readline().strip()
    names =[]
    while(name):
        if name in names:
            continue
        names.append(name)
        name = f.readline().strip()
    f.close()

    config = load_param(args.config)
    bot = LineStampBot(config)
    
    #names = list(set(names))

    driver = create_driver()
    bot.line_login(driver)

    for name in names:  
        print(name)
        if not name in name_table:
            print("{} テーブルになし".format(name))
            continue
        if os.path.exists("D:/program/line-entry/zip/{}.zip".format(name)):
            retry_cnt = 3
            success = False
            for i in range(retry_cnt):
                ret = bot.register_stamp(driver, name, name_table)
                if ret is False:
                    print("{}回目失敗 再起動".format(i))
                    driver.close()
                    driver = create_driver()
                    bot.line_login(driver)

                else:
                    success = True
                    break
            if not success:
                print("{} 登録失敗".format(name))

        else:
            print("{} なし".format(name))

    driver.close()


if __name__ == '__main__': main()
