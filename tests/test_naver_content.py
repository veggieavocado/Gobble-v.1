from django.test import TestCase
from django.core.urlresolvers import reverse

from rest_framework import status
from rest_framework.test import APIClient

from rest_framework_jwt import utils, views
from rest_framework_jwt.compat import get_user_model
from rest_framework_jwt.settings import api_settings, DEFAULTS

import json, os
from django.utils.encoding import smart_text
from contents.models import NaverData, NaverContent
from accounts.models import Profile
User = get_user_model()

from tests.url_endpoints import URL

class NaverContetnsAPITestCase(TestCase):
    '''
    Naver Finance Contents REST API testing module
    '''

    def setUp(self):
        print('Starting Sentence API test')
        self.client = APIClient(enforce_csrf_checks=True)
        self.username = 'lee'
        self.email = 'lee@gmail.com'
        self.password = '123123123'
        # create new user to send post requests
        self.user = {
            'username': self.username,
            'email': self.email,
            'password': self.password,
        }

        # 테스트용 user-data 생성
        self.userdata =  {
            'username': self.username,
            'password': self.password,
        }
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

        response = self.client.post(
            URL['user_create_url'],
            self.user,
            format='json'
        )
        self.assertEqual(User.objects.all().count(), 1, msg='user data not created properly')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.first().username, self.user['username'])
        self.assertEqual(User.objects.first().email, self.user['email'])

        response = self.client.post(
            URL['get_jwt_token'],
            json.dumps(self.userdata),
            content_type='application/json'
        )

        self.token = response.data['token']
        response_content = json.loads(smart_text(response.content))
        decoded_payload = utils.jwt_decode_handler(response_content['token'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(decoded_payload['username'], self.username)


    def test_naver_contents_api(self):
        # post
        # unauthorized case
        response = self.client.post(
            URL['naver_contents'],
            self.naver_contents,
            format='json',
        )
        self.assertEqual(NaverContent.objects.all().count(), 0, msg='user data not created properly')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        # authorized case
        response = self.client.post(
            URL['naver_contents'],
            self.naver_contents,
            HTTP_AUTHORIZATION='JWT ' + self.token,
            format='json',
        )
        print(response)
        self.assertEqual(NaverContent.objects.all().count(), 1, msg='user data not created properly')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # authorized case
        response = self.client.get(
            URL['naver_contents'],
            HTTP_AUTHORIZATION='JWT ' + self.token,
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
        self.assertEqual(NaverData.objects.all().count(), 0, msg='user data not created properly')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        # authorized case
        response = self.client.post(
            URL['naver_data'],
            self.naver_data,
            HTTP_AUTHORIZATION='JWT ' + self.token,
            format='json',
        )
        self.assertEqual(NaverData.objects.all().count(), 1, msg='user data not created properly')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # authorized case
        response = self.client.get(
            URL['naver_data'],
            HTTP_AUTHORIZATION='JWT ' + self.token,
            format='json',
        )
        data = response.json()['results'][0]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data['data_name'], "R")
