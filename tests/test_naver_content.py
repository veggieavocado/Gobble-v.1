from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

import json, os
from django.utils.encoding import smart_text
from contents.models import NaverData, NaverContent

from tests.url_endpoints import URL

class NaverContetnsAPITestCase(TestCase):
    '''
    Naver Finance Contents REST API testing module
    '''

    def setUp(self):
        print('Starting Sentence API test')
        self.client = APIClient()
        # create sentence data
        self.naver_contents = {
                                "title": "[공시+]에이티젠, NK뷰키트 매출 83%증가… 상반기매출 전년比 약 40%↑",
                                "media": "[아시아경제 문채석 기자]",
                                "upload_time": "2018-08-15 12:06",
                                "url":"https://finance.naver.com/news/news_read.nhn?article_id=0004295863&office_id=277&mode=LSS2D&type=0&section_id=101&section_id2=258&section_id3=&date=20180815&page=1",
                                "content": "정밀 면역검사용 의료기기 NK뷰키트를 개발한 에이티젠은 지난 상반기 NK뷰키트 매출이 83% 증가했다고 14일 공시했다.",
                                "type": "R"
                                }

        self.naver_data = {
                            "data_name": "R",
                            "data":"[{'name': '삼성전자', 'y': 10}, {'name': '삼성바이오로직스', 'y': 8},\
                                    {'name': 'NHN', 'y': 4}, {'name': '셀트리온', 'y': 3}]"
                            }

    def test_naver_contents_api(self):
        # post
        response = self.client.post(
            URL['naver_contents'],
            self.naver_contents,
            format='json',
        )
        self.assertEqual(NaverContent.objects.all().count(), 1, msg='user data not created properly')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # authorized case
        response = self.client.get(
            URL['naver_contents'],
            format='json',
        )
        data = response.json()['results'][0]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data['title'], "[공시+]에이티젠, NK뷰키트 매출 83%증가… 상반기매출 전년比 약 40%↑")
        self.assertEqual(data['media'], "[아시아경제 문채석 기자]")
        self.assertEqual(data['url'], "https://finance.naver.com/news/news_read.nhn?article_id=0004295863&office_id=277&mode=LSS2D&type=0&section_id=101&section_id2=258&section_id3=&date=20180815&page=1")

    def test_naver_data_api(self):
        # post
        # unauthorized case
        response = self.client.post(
            URL['naver_data'],
            self.naver_data,
            format='json',
        )
        self.assertEqual(NaverData.objects.all().count(), 1, msg='user data not created properly')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # authorized case
        response = self.client.get(
            URL['naver_data'],
            format='json',
        )
        data = response.json()['results'][0]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data['data_name'], "R")
