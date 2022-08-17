#!/usr/bin/env python3
import time
import pickle
from selenium import webdriver
from bs4 import BeautifulSoup as BS


options = webdriver.ChromeOptions()
# options.headless = True
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


with open("index.html", "w", encoding="utf-8") as file:
    file.write(html)


driver.close()


with open("./index.html", encoding="utf-8") as file:
    html_read = file.read()

soup = BS(html_read, "lxml")

trs_light = soup.find("table", class_="t_main").find("tbody").find_all("tr", class_="aj_light")
trs_dark = soup.find("table", class_="t_main").find("tbody").find_all("tr", class_="aj_dark")
print(len(trs_light), len(trs_dark))
