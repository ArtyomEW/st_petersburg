from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from openpyxl import load_workbook
from selenium import webdriver
from bs4 import BeautifulSoup
import numpy
import time



class Gis2:
    links = numpy.array([])
    page = 0

    @staticmethod
    def bs4(driver):
        """Функция, которая определяет,
        дошёл ли скрипт до последней страницы"""
        bs = BeautifulSoup(driver.page_source, 'html.parser')
        _7q94tr = bs.findAll('div', class_='_7q94tr')
        if not _7q94tr:
            return False
        return True

    @staticmethod
    def site_does_not_close():
        chr_options = Options()
        chr_options.add_experimental_option("detach", True)
        driver = webdriver.Chrome(options=chr_options)
        return driver

    @classmethod
    def taking_email_phone_and_website(cls, link):
        fn = '2gis.xlsx'
        wb = load_workbook(fn)
        ws = wb['Лист1']
        driver = cls.site_does_not_close()
        driver.get(link)
        time.sleep(3)
        bs = BeautifulSoup(driver.page_source, 'html.parser')
        mail_and_site = bs.findAll('div', class_='_49kxlr')
        name_company = bs.findAll('h1', class_='_cwjbox')
        lst = []
        for i in name_company:
            lst.append(i.text[:-1])
        for i in mail_and_site:
            if i.find('a', class_='_1rehek') is not None:
                if 'ru' in i.text or 'com' in i.text:
                    lst.append(i.text)
            if i.find('a', class_='_2lcm958') is not None:
                if 'ru' in i.text or 'com' in i.text:
                    lst.append(i.text)
        link = driver.find_elements(By.TAG_NAME, 'a')
        for teg in link:
            phone = teg.get_attribute('href')
            if phone is not None and 'tel:' in phone:
                lst.append(phone)
        ws.append(lst)
        wb.save(fn)
        driver.quit()

    @classmethod
    def find_firm_link_if_all_page_True(cls, driver, svg):
        while True:
            time.sleep(3)
            link = driver.find_elements(By.TAG_NAME, 'a')
            for l in link:
                href = l.get_attribute('href')
                if href is not None and 'firm' in href and href not in cls.links:
                    cls.links = numpy.append(cls.links, href)
            cls.page += 1
            # Кликаем по тегу для перехода на следующую страницу
            driver.execute_script("arguments[0].click();", svg)
            if cls.bs4(driver):
                driver.quit()
                for i in cls.links:
                    cls.taking_email_phone_and_website(i)
                return "ВСЕ СТРАНИЦЫ УСПЕШНО СПАРСИЛИСЬ"

    @classmethod
    def add_el_in_links(cls, svg, driver, count_page, all_page=False):
        try:
            if not all_page:
                while cls.page < int(count_page):
                    time.sleep(3)
                    link = driver.find_elements(By.TAG_NAME, 'a')
                    for l in link:
                        href = l.get_attribute('href')
                        if href is not None and 'firm' in href and href not in cls.links:
                            cls.links = numpy.append(cls.links, href)
                    cls.page += 1
                    #Кликаем по тегу для перехода на следующую страницу
                    driver.execute_script("arguments[0].click();", svg)
                    if cls.bs4(driver):
                        driver.quit()
                        for i in cls.links:
                            cls.taking_email_phone_and_website(i)
                        return "ВСЕ СТРАНИЦЫ УСПЕШНО СПАРСИЛИСЬ"
            else:
                cls.find_firm_link_if_all_page_True(driver, svg)
            driver.quit()
            for i in cls.links:
                cls.taking_email_phone_and_website(i)
        except Exception:
            print('Попробуйте снова!')


    @classmethod
    def main(cls):
        all_page = False
        link: str = input('Ссылка для сбора информации-> ')
        count_page = input('Число желаемых страниц для парсинга-> ')
        if count_page == '':
            print('Сейчас будет парсинг всех страниц сайта')
            count_page = 0
            all_page = True
        #Функция, что бы браузер не закрывался
        driver = cls.site_does_not_close()
        #Переходим на наш сайт
        driver.get(link)
        time.sleep(2)
        #Находим наш тег для перехода на следующую страницу
        svg = driver.find_element(By.CSS_SELECTOR, '#root > div > div > div._1sf34doj > div._1u4plm2 > '
                                                   'div:nth-child(3) > div > div > div:nth-child(2) > div > div > div > div._1tdquig > '
                                                   'div._z72pvu > div._3zzdxk > div > div > div > div._1x4k6z7 > div._5ocwns > div._n5hmn94')

        cls.add_el_in_links(svg, driver, count_page, all_page)

if __name__ == '__main__':
    gis = Gis2()
    gis.main()
