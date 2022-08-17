#!/usr/bin/env python3
import time
import pickle
import re
from selenium import webdriver
from bs4 import BeautifulSoup as BS


options = webdriver.ChromeOptions()
options.headless = True
driver = webdriver.Chrome(options=options)
driver.get("https://bid.aaajapan.com/aj")

for c in pickle.load(open("./session", "rb")):
    driver.add_cookie(c)

driver.refresh()

brand = driver.find_element("xpath", '/html/body/font/nobr/table/tbody/tr[2]/td/form/table/tbody/tr/td[2]/table/tbody/tr/td[1]/div/select/option[3]')
brand.click()

models = driver.find_elements("xpath", '//*[@id="poisk"]/table/tbody/tr/td[2]/table/tbody/tr/td[2]/div/select/option')
for i in models:
    if "LEAF" in i.text:
        model = i
model.click()

item = driver.find_element("xpath", '/html/body/font/nobr/table/tbody/tr[2]/td/form/table/tbody/tr/td[3]/input[1]')
item.click()


time.sleep(1)

html = driver.page_source

with open("index0.html", "w", encoding="utf-8") as file:
    file.write(html)

page_two = driver.find_element("xpath", '//*[@id="aj_out_poisk"]/div/table[1]/tbody/tr/td[2]/table/tbody/tr/td[2]/a')
page_two.click()

time.sleep(1)

html_two = driver.page_source

with open("index1.html", "w", encoding="utf-8") as file:
    file.write(html_two)

driver.close()


for i in range(2):
    with open(f"./index{i}.html", encoding="utf-8") as file:
        html_read = file.read()

    soup = BS(html_read, "lxml")

    pattern = r'aj_light|aj_dark'

    trs = soup.find("table", class_="t_main").find("tbody").find_all("tr", class_=re.compile(pattern=pattern))
    # print(len(trs))
    for tr in trs:
        tds = tr.find_all("td")
        if "AZE0" in tds[5].text:
            if "продан" in tds[10].text:
                continue
            print()
            print("-------------------------------------------------------------------------------------------------------------------------------------------------")
            print(tr.text)
            print("-------------------------------------------------------------------------------------------------------------------------------------------------")
            print()


