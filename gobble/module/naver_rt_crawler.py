# -*- coding: utf-8 -*-
"""
Created on Fri Aug 17 05:15:30 2018

@author: LeeMH
"""
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import requests
import re

from utils.processor_checker import timeit
from gobble.module.crawler import Crawler


class NaverRealtimeCrawler(Crawler):
    '''
    네이버 증권 실시간 속보 크롤러
    '''
    def __init__(self):
        super().__init__()

    # func (기능): all (오늘 날짜의 모든 뉴스를 크롤링), new (1page만 크롤링)
    @timeit
    def create_url_list(self, func):
        req = self.request_get(self.real_time_list.format(self.rt_today, 1), self.user_agent)
        print(self.real_time_list.format(self.rt_today, 1))
        soup = self.html_parser(req)
        url_list = []
        if func == 'new':
            url_data = self.find_navernews_url(soup, url_list)

        elif func == 'all':
            pgRR = self.soup_find(soup, 'td', {'class':'pgRR'})
            last_page = self.soup_find(pgRR, 'a')['href'][-3:]
            last_page = re.findall("\d+", last_page)[0]

            sub_list = []
            for i in range(1,int(last_page)+1):
                req = self.request_get(self.real_time_list.format(self.rt_today, i), self.user_agent)
                sub_soup = self.html_parser(req)
                url_list += self.find_navernews_url(sub_soup, sub_list)
            url_data = url_list
        else:
            print("Choose between 'all' and 'new'")
        url_data = list(set(url_data))
        print(len(url_data))
        real_time_url = [self.soup_find(sub, 'a')['href'].replace('§', '&sect') for sub in url_data]
        return real_time_url

    @timeit
    def get_data(self, url_list, checklist):
        url_list = url_list
        data_list = []
        for url in url_list:
            self.req = self.request_get(self.fin_nhn.format(url), self.user_agent)
            soup = self.html_parser(self.req)
            url = self.fin_nhn.format(url)
            title = self.soup_find(soup, 'h3').text.replace('\n','').replace('\t','').strip()
            if url in checklist:
                print('Already up-to-date.')
                continue
            upload_time = self.soup_find(soup, 'span', {'class':'article_date'}).text
            media = self.soup_find(soup, 'span', {'class':'press'}).img['title']
            data_dict = {'title':title, 'media':media, 'url':url, 'data_type':'R', 'upload_time': upload_time}
            data_list.append(data_dict)
        print(len(data_list))
        return data_list
