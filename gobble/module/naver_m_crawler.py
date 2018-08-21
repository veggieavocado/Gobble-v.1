# -*- coding: utf-8 -*-
"""
Created on Fri Aug 19 05:15:30 2018

@author: LeeMH
"""

from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import requests
import re

from utils.processor_checker import timeit
from gobble.module.crawler import Crawler

# TODAY = datetime.today().strftime("%Y-%m-%d")
# TODAY = datetime.today() - timedelta(days=2)
# TODAY = TODAY.strftime("%Y-%m-%d")


class NaverMajorCrawler(Crawler):
    '''
    네이버 증권 실시간 속보 크롤러
    '''
    def __init__(self):
        super().__init__()

    # func (기능): all (오늘 날짜의 모든 뉴스를 크롤링), new (1page만 크롤링)
    @timeit
    def create_url_list(self, func):
        req = self.request_get(self.main_news.format(self.main_today, 1), self.user_agent)
        print(self.main_news.format(self.main_today, 1))
        print(req)
        soup = self.html_parser(req)
        url_list = []
        try:
            pgRR = self.soup_find(soup, 'td', {'class':'pgRR'})
            last_page = self.soup_find(pgRR, 'a')['href'][-3:]
            last_page = re.findall("\d+", last_page)[0]
        except AttributeError:
            func = 'new'

        if func == 'new':
            url_data = self.find_navernews_url(soup, url_list)

        elif func == 'all':
            sub_list = []
            for i in range(1,int(last_page)+1):
                req = self.request_get(self.main_news.format(self.main_today, i), self.user_agent)
                sub_soup = self.html_parser(req)
                url_list += self.find_navernews_url(sub_soup, sub_list)
            url_data = url_list
        else:
            print("Choose between 'all' and 'new'")
        url_data = list(set(url_data))
        print(len(url_data))
        major_new_url = [self.soup_find(sub, 'a')['href'].replace('§', '&sect') for sub in url_data]
        return major_new_url

    @timeit
    def get_data(self, url_list, checklist):
        url_list = url_list
        data_list = []
        for url in url_list:
            req = self.request_get(self.fin_nhn.format(url), self.user_agent)
            soup = self.html_parser(req)
            url = self.fin_nhn.format(url)
            title = self.soup_find(soup, 'h3').text.replace('\n','').replace('\t','').strip()
            if url in checklist:
                print('Already up-to-date.')
                continue
            upload_time = self.soup_find(soup, 'span', {'class':'article_date'}).text
            contents = self.soup_find(soup, 'div', {'class':'articleCont'}).text.replace('\n','').replace('\t','').strip()
            media = self.soup_find(soup, 'span', {'class':'press'}).img['title']
            data_dict = {'title':title, 'media':media, 'url':url, 'data_type':'M', 'upload_time': upload_time, 'contents':contents}
            data_list.append(data_dict)
        print(len(data_list))
        return data_list
