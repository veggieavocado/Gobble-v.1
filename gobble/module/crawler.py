# -*- coding: utf-8 -*-
"""
Created on Sun Aug 19 03:15:30 2018

@author: LeeMH
"""
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import requests

from utils.processor_checker import timeit

class Crawler(object):
    '''
    네이버 증권 실시간 속보 크롤러
    '''
    def __init__(self):
        # self.today = datetime.today() - timedelta(days=2)
        self.today = datetime.today()
        self.rt_today = self.today.strftime('%Y%m%d')
        self.main_today = self.today.strftime('%Y-%m-%d')
        self.fin_nhn = 'https://finance.naver.com{}'
        self.main_news = 'https://finance.naver.com/news/mainnews.nhn?date={}&page={}'
        self.real_time_list = 'https://finance.naver.com/news/news_list.nhn?mode=LSS2D&section_id=101&section_id2=258&date={}&page={}'
        self.user_agent = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36'}
        print("NAVER CRAWLER READY!", self.today, self.main_today)

    def request_get(self, url, user_agent):
        req = requests.get(url, headers= user_agent, auth=('user', 'pass'))
        return req

    def html_parser(self, req):
        soup = BeautifulSoup(req.text, 'html.parser')
        return soup
    # find & findall
    def soup_find(self, soup, tags, class_dict=None, func=None):
        if func == 'all':
            source = soup.findAll(tags, class_dict)
        elif func == None:
            source = soup.find(tags, class_dict)
        return source

    def find_navernews_url(self, soup, url_data):
        sub_url_dd = self.soup_find(soup, 'dd', {'class':'articleSubject'}, func='all')
        sub_url_dt = self.soup_find(soup, 'dt', {'class':'articleSubject'}, func='all')
        url_data += sub_url_dd
        url_data += sub_url_dt
        return url_data
