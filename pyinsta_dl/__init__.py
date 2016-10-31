# -*- coding: utf-8 -*-
import urllib2, time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


class PyInsta_DL(object):

    DesiredCapabilities.PHANTOMJS[
        'phantomjs.page.customHeaders.User-Agent'] = \
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'
    driver = webdriver.PhantomJS(executable_path='/usr/local/share/phantomjs-2.1.1-linux-x86_64/bin/phantomjs',
                                 service_args=['--ignore-ssl-errors=true'])

    def get(self, url):
        self.url = url
        soup = BeautifulSoup(urllib2.urlopen(self.url).read() , "html.parser")
        for meta in soup.findAll('meta'):
            if meta.get("property") == "og:image" and meta.get("content") != '':
                return meta.get("content")
            elif meta.get("property") == "og:video" and meta.get("content") != '':
                return meta.get("content")
        return None

    def get_all(self, url_profile):

        self.url = url_profile
        self.driver.get('https://www.instagram.com/natanocr/')
        time.sleep(5)
        for i in range(self.count_scrolls()):
            self.scroll()
        return self.get_all_urls()

    def count_scrolls(self):
        _default_number = 12
        publicatios = self.driver.find_element_by_class_name('_bkw5z')
        number = int(publicatios.text.replace('.', ''))
        if number <= 12:
            return 1
        else:
            more = self.driver.find_element_by_class_name(' _1ooyk')
            more.click()
            return (number / _default_number) + 1

    def scroll(self):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)

    def get_all_urls(self):
        images = self.driver.find_elements_by_class_name('_icyx7')
        links = []
        for i in images:
            if i != None:
                links.append(i.get_attribute('src'))
        return links


DEFAULT_DOWNLOAD = PyInsta_DL()


def get(url):
    return DEFAULT_DOWNLOAD.get(url)


def get_all(url_profile):
    return DEFAULT_DOWNLOAD.get_all(url_profile)

