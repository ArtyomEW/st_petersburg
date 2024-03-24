from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from openpyxl import load_workbook
from selenium import webdriver
from bs4 import BeautifulSoup
from icecream import ic
import numpy
import time

'''Список для хранения ссылок компаний'''
links = numpy.array([])


def add_el_in_links(svg, driver):
    global links

    count_page = 0

    while count_page != 130:
        time.sleep(3)
        link = driver.find_elements(By.TAG_NAME, 'a')
        for i in link:
            href = i.get_attribute('href')
            if href is not None and 'firm' in href and href not in links:
                links = numpy.append(links, href)
        count_page += 1
        '''Кликаем по тегу для перехода на следующую страницу'''
        driver.execute_script("arguments[0].click();", svg)
    driver.quit()


def main(link: str):
    global links

    """Функция что бы браузер не закрывался"""
    chr_options = Options()
    chr_options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=chr_options)

    """Переходим на наш сайт"""
    driver.get(link)

    '''Находим наш тег для перехода на следующую страницу'''
    svg = driver.find_element(By.CSS_SELECTOR, "#root > div > div > div._1sf34doj > div._1u4plm2 > div:nth-child("
                                               "2) >"
                                               "div > div > div:nth-child(2) > div > div > div > div._1tdquig > "
                                               "div._z72pvu > div._3zzdxk > div > div > div > div._1x4k6z7 > "
                                               "div._5ocwns > div._n5hmn94")
    add_el_in_links(svg, driver)


if __name__ == '__main__':
    main('https://2gis.ru/spb/search/%D0%B8%D0%BD%D0%B6%D0%B5%D0%BD%D0%B5%D1%80%D0%BD%D0%B0%D1%8F%20%D1%81%D0%B0%D0'
         '%BD%D1%82%D0%B5%D1%85%D0%BD%D0%B8%D0%BA%D0%B0?m=30.313803%2C59.944294%2F11')
    # taking_email_phone_and_website('https://2gis.ru/spb/search/%D0%A1%D0%B8%D1%81%D1%82%D0%B5%D0%BC%D1%8B%20%D0%BE%D1'
    #                                '%82%D0%BE%D0%BF%D0%BB%D0%B5%D0%BD%D0%B8%D1%8F%20%2F%20%D0%B2%D0%BE%D0%B4%D0%BE%D1'
    #                                '%81%D0%BD%D0%B0%D0%B1%D0%B6%D0%B5%D0%BD%D0%B8%D1%8F%20%2F%20%D0%BA%D0%B0%D0%BD%D0'
    #                                '%B0%D0%BB%D0%B8%D0%B7%D0%B0%D1%86%D0%B8%D0%B8/rubricId/489/firm/70000001069094676'
    #                                '?m=30.314838%2C59.938138%2F15.96')
