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
    
    config = load_param(args.config)
    bot = LineStampBot(config)

    driver = create_driver()
    bot.release(driver, f=1, t=50)


if __name__ == '__main__':
    main()
