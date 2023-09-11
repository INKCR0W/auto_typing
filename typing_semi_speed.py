# coding = utf-8

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from threading import Thread
import re
import time
import math

MAIN_URL = 'https://dazi.kukuw.com/'









speed = int(input("请输入设定的打字速度"))
input_time = int(input("请输入设定的打字时间"))

wanted_letter = speed * input_time

if input_time > 50 or input_time < 1:
    print("非法的打字时间（范围为1~50）")
    exit()


driver = webdriver.Chrome()
print("打开主页面，等待加载完成")
driver.get(MAIN_URL)

try:
    print("随机选择文章")
    driver.find_element("xpath", '//*[@id="suiji_a"]').click()
    print("文章: {}".format(driver.find_element("xpath", '//*[@id="select_i"]').text))

    print("设置打字时间")
    time_box = driver.find_element("xpath", '//*[@id="time"]')
    time_box.clear()
    time_box.send_keys(input_time)
    print("设置时间为{}分钟".format(input_time))

    print("预计输入{}个字母".format(wanted_letter))

    time.sleep(1)

    print("准备开始打字，等待加载完成")
    driver.find_element("xpath", '/html/body/div[2]/div[3]/div/div/form/ul[6]/li[2]/input').click()
except Exception as e:
    print("出现错误:", e)
    exit()

while True:
    try:
        if re.search('typing.html', driver.current_url):
            print("进入打字页面")
            break
        else:
            driver.find_element("xpath", '/html/body/div[2]/div[3]/div/div/form/ul[6]/li[2]/input').click()
            print("还未进入打字页面，重新尝试")
            time.sleep(1)
    except Exception as e:
        print("尝试进入打字页面时出现错误{}，\n不过可能不是致命影响，如果一直出现此提示，请检查代码".format(e))


line_count = 1
typed_letter = 0

while True:
    try:
        if typed_letter != wanted_letter:
            print("读取第{}行:".format(line_count))
            text = driver.find_element("xpath", '/html/body/div[2]/form/div[3]/div[{}]/div/span'.format(line_count)).text
            if len(text) > (wanted_letter - typed_letter):
                text = text[:(wanted_letter - typed_letter)]
            print(text)
            print("输入第{}行".format(line_count))
            driver.find_element("xpath", '/html/body/div[2]/form/div[3]/div[{}]/input[2]'.format(line_count)).send_keys(text)
            typed_letter += len(text)
            if typed_letter < wanted_letter:
                driver.find_element("xpath", '/html/body/div[2]/form/div[3]/div[{}]/input[2]'.format(line_count)).send_keys(' ')
            line_count = line_count + 1
        else:
            time.sleep(1)

        continue_button = driver.find_element("xpath", '//*[@id="box_button_a"]')
        print("打字结束，KPM: {}".format(driver.find_element("xpath", '/html/body/div[2]/div[5]/div/div[2]/strong[2]').text))
        continue_button.click()
        break

    except Exception as e:
        if not re.search('typing.html', driver.current_url):
            print("未知情况，可能是打字结束了，错误:", e)
            break
        else:
            print("打字继续")



user_input = input("输入任意字符退出")