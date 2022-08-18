#!/usr/bin/env python3
import time
import pickle
import re
from selenium import webdriver
from bs4 import BeautifulSoup as BS



def get_index():
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument('--log-level=3')
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
    try:
        page_two = driver.find_element("xpath", '//*[@id="aj_out_poisk"]/div/table[1]/tbody/tr/td[2]/table/tbody/tr/td[2]/a')
        page_two.click()
        time.sleep(1)
        html_two = driver.page_source
        with open("index1.html", "w", encoding="utf-8") as file:
            file.write(html_two)
        number_of_pages = 2
    except:
        number_of_pages = 1
    driver.close()
    return number_of_pages


def get_car():
    data = []
    cnt = get_index()
    for i in range(cnt):
        with open(f"./index{i}.html", encoding="utf-8") as file:
            html_read = file.read()
        soup = BS(html_read, "lxml")
        pattern = r'aj_light|aj_dark'
        trs = soup.find("table", class_="t_main").find("tbody").find_all("tr", class_=re.compile(pattern=pattern))
        for tr in trs:
            tds = tr.find_all("td")
            if "AZE0" in tds[5].text:
                if "продан" in tds[10].text:
                    continue
                data.append(tr.text.strip())
    return data


def main():
    for i in get_car():
        print(i)
    print(len(get_car()))


if __name__ == "__main__":
    main()
