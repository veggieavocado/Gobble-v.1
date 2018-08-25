from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

import json, os
from django.utils.encoding import smart_text
from contents.models import WantedUrl, WantedContent, WantedData

from tests.url_endpoints import URL

from molecular.settings import PRODUCTION

class WantedContetnsAPITestCase(TestCase):
    '''
    Wanted Contents REST API testing module
    '''

    def setUp(self):
        print('Starting Sentence API test')
        self.client = APIClient()
        self.production = PRODUCTION
        # create sentence data
        self.wanted_contents = {
                                "title": "iOS 개발자",
                                "company": "원티드랩",
                                "location": "서울 강남구",
                                "url":"https://www.wanted.co.kr/wd/12970,",
                                "content": "‘원티드랩’은 전 세계 모든 기업과 직장인의 고민을 해결하기 위한 HR 스타트업입니다.",
                                }

        self.wanted_urls = {
                            "urls": "https://www.wanted.co.kr/wd/12970,\
                                    https://www.wanted.co.kr/wd/12966,\
                                    https://www.wanted.co.kr/wd/12810,\
                                    https://www.wanted.co.kr/wd/3807,\
                                    https://www.wanted.co.kr/wd/12794,\
                                    https://www.wanted.co.kr/wd/6053,\
                                    https://www.wanted.co.kr/wd/5057,\
                                    https://www.wanted.co.kr/wd/12076,\
                                    https://www.wanted.co.kr/wd/12878,",
                            }

        self.wanted_data = {
                            "data_name": "top_skill",
                            "data":"[{'name': 'JavaScript', 'y': 539}, {'name': 'AWS', 'y': 503},\
                                    {'name': 'API', 'y': 461}, {'name': 'iOS', 'y': 333},\
                                    {'name': 'C', 'y': 333}, {'name': 'Python', 'y': 305},\
                                    {'name': 'Java', 'y': 264}, {'name': 'Android', 'y': 263},\
                                    {'name': 'Web', 'y': 257}, {'name': 'React', 'y': 239},\
                                    {'name': 'Linux', 'y': 200}, {'name': 'UI', 'y': 190},\
                                    {'name': 'MySQL', 'y': 182}, {'name': 'DB', 'y': 175},\
                                    {'name': 'CSS', 'y': 169}, {'name': 'HTML', 'y': 168},\
                                    {'name': 'Git', 'y': 156}, {'name': 'SQL', 'y': 156},\
                                    {'name': 'MS', 'y': 142}, {'name': 'PHP', 'y': 140},\
                                    {'name': 'Node', 'y': 125}, {'name': 'R', 'y': 108},\
                                    {'name': 'Ruby', 'y': 105}]"
                            }

    def test_wanted_contents_api(self):
        # post
        # unauthorized case
        response = self.client.post(
            URL['wanted_job_contents'],
            self.wanted_contents,
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        if self.production == True:
            self.assertEqual(WantedContent.objects.using('contents').all().count(), 1, msg='user data not created properly')
        else:
            self.assertEqual(WantedContent.objects.all().count(), 1, msg='user data not created properly')

        # authorized case
        response = self.client.get(
            URL['wanted_job_contents'],
            format='json',
        )
        data = response.json()['results'][0]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data['title'], "iOS 개발자")
        self.assertEqual(data['company'], "원티드랩")
        self.assertEqual(data['url'], "https://www.wanted.co.kr/wd/12970,")

    def test_wanted_urls_api(self):
        # post
        # unauthorized case
        response = self.client.post(
            URL['wanted_url'],
            self.wanted_urls,
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        if self.production == True:
            self.assertEqual(WantedUrl.objects.using('contents').all().count(), 1, msg='wanted data not created properly')
        else:
            self.assertEqual(WantedUrl.objects.all().count(), 1, msg='wanted data not created properly')

        # authorized case
        response = self.client.get(
            URL['wanted_url'],
            format='json',
        )
        print(response)
        data = response.json()['results'][0]
        data_split = data['urls'].split(',')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data_split[0], "https://www.wanted.co.kr/wd/12970")

    def test_wanted_data_api(self):
        # post
        # unauthorized case
        response = self.client.post(
            URL['wanted_data'],
            self.wanted_data,
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        if self.production == True:
            self.assertEqual(WantedData.objects.using('contents').all().count(), 1, msg='wanted data not created properly')
        else:
            self.assertEqual(WantedData.objects.all().count(), 1, msg='wanted data not created properly')

        # authorized case
        response = self.client.get(
            URL['wanted_data'],
            format='json',
        )
        data = response.json()['results'][0]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data['data_name'], "top_skill")
