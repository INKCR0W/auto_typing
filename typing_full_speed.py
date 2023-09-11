# coding = utf-8

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from threading import Thread
import re
import time

MAIN_URL = 'https://dazi.kukuw.com/'












driver = webdriver.Chrome()
print("打开主页面，等待加载完成")
driver.get(MAIN_URL)

print("随机选择文章")
driver.find_element("xpath", '//*[@id="suiji_a"]').click()

print("文章: {}".format(driver.find_element("xpath", '//*[@id="select_i"]').text))
time.sleep(1)

print("准备开始打字，等待加载完成")
driver.find_element("xpath", '/html/body/div[2]/div[3]/div/div/form/ul[6]/li[2]/input').click()

while True:
    try:
        if re.search('typing.html', driver.current_url):
            print("进入打字页面")
            break
        else:
            driver.find_element("xpath", '/html/body/div[2]/div[3]/div/div/form/ul[6]/li[2]/input').click()
            print("还未进入打字页面，重新尝试")
            time.sleep(1)
    except:
        print("尝试进入打字页面时出现错误，不过可能不是致命影响，如果一直出现此提示，请检查代码")


line_count = 1
finded_text = False
finded_button = False

while True:
    try:
        finded_text = False
        finded_button = False
        print("读取第{}行:".format(line_count))
        text = driver.find_element("xpath", '/html/body/div[2]/form/div[3]/div[{}]/div/span'.format(line_count)).text
        finded_text = True
        print(text)
        print("输入第{}行".format(line_count))
        driver.find_element("xpath", '/html/body/div[2]/form/div[3]/div[{}]/input[2]'.format(line_count)).send_keys(text + ' ')
        line_count = line_count + 1

        continue_button = driver.find_element("xpath", '//*[@id="box_button_a"]')
        print("打字结束，KPM: {}".format(driver.find_element("xpath", '/html/body/div[2]/div[5]/div/div[2]/strong[2]').text))
        continue_button.click()
        break

    except:
        if not re.search('typing.html', driver.current_url):
            print("未知情况，可能是打字结束了")
            break
        else:
            print("打字继续")




user_input = input("输入任意字符退出")