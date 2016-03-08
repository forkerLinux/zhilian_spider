import io
import time
from PIL import Image
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys


class Zhilian(object):

    account_info = {
        'username': 'hxjs5875',
        'password': 'hxjs123456',
    }

    def __init__(self):
        self.browser = webdriver.Firefox()
        # self.browser = webdriver.PhantomJS()


    def to_png(self, element):
        location = element.location
        size = element.size

        img = self.browser.get_screenshot_as_png()
        img = Image.open(io.BytesIO(img))

        left = location['x']
        top = location['y']
        right = location['x'] + size['width']
        bottom = location['y'] + size['height']
        img = img.crop((left, top, right, bottom)) # defines crop points

        ret_img = io.BytesIO()
        img.save(ret_img, format='png')
        ret_img.seek(0)

        return ret_img

    def load_login(self):
        url = 'http://rd2.zhaopin.com/portal/myrd/regnew.asp?za=2'
        self.browser.get(url)
        validcode_element = self.browser.find_element_by_id('checkimg')
        img = self.to_png(validcode_element)
        return img

    def login(self, validcode):
        self.browser.find_element_by_id('LoginName').send_keys(self.account_info['username'])
        self.browser.find_element_by_id('Password').send_keys(self.account_info['password'])
        self.browser.find_element_by_id('CheckCode').send_keys(validcode)
        self.browser.find_element_by_name('Submit').click()
        return

    def search_cv(self, **kwarg):
        """模拟用户点击搜索后输入参数点击搜索
            keyword: 关键词
            edu_min: 最低学历
            edu_max: 最高学历
        """
        self.browser.get('http://rdsearch.zhaopin.com/')
        self.browser.find_element_by_id('SF_1_1_1').clear()
        self.browser.find_element_by_id('SF_1_1_1').send_keys(kwarg['keyword'])


        elem = self.browser.find_element_by_id('SF_1_1_5_min')
        select = Select(elem)
        select.select_by_value(kwarg['edu_min'])

        elem = self.browser.find_element_by_id('SF_1_1_5_max')
        select = Select(elem)
        select.select_by_value(kwarg['edu_max'])

        self.browser.find_element_by_css_selector("#searchSubmit button").click()
        return self.get_page_info()


    def get_page_info(self):
        """得到搜索数据
        """

        table_element = self.browser.find_element_by_tag_name('table')
        # 1/134 当前页面和总页面
        page_info = self.browser.find_element_by_id('rd-resumelist-pageNum').text

        tr_list = []

        tr_elements = table_element.find_elements_by_tag_name('tr')
        tr_elements.pop(0)
        for index, tr_element in enumerate(tr_elements):
            if index % 2 == 0:
                td_elements = tr_element.find_elements_by_tag_name('td')
                td_list = []
                cv_id = td_elements[0].find_element_by_class_name('smpcheckbox').\
                    get_attribute('data-smpcvid')

                td_list.append(cv_id[:-2])
                for i in range(8):
                    if i != 1:
                        td_list.append(td_elements[i+1].text)
                tr_list.append(td_list)

        return (tr_list, page_info)


    def go_next(self):
        # 下一页
        self.browser.find_element_by_class_name('right-icon').click()
        return self.get_page_info()

    def go_prev(self):
        # 上一页
        self.browser.find_element_by_class_name('left-icon').click()
        return self.get_page_info()

    def get_cv_page(self, cv_id):
        # cv详情
        url = 'http://rd.zhaopin.com/resumepreview/resume/viewone/2/'\
            +cv_id+'_1_1'
        self.browser.get(url)
        page_source = self.browser.page_source
        # 操纵浏览器返回
        self.browser.back()

        soup = BeautifulSoup(page_source, 'lxml')
        soup.select('.resume-preview-right')[0].decompose()
        soup.select('.rd_button')[0].decompose()
        new_tag = soup.new_tag("a", href="/add_cv?cv_id="+cv_id)

        return str(soup)
