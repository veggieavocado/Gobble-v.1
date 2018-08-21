from django.test import TestCase
from django.core.urlresolvers import reverse

from rest_framework import status
from rest_framework.test import APIClient

from rest_framework_jwt import utils, views
from rest_framework_jwt.compat import get_user_model
from rest_framework_jwt.settings import api_settings, DEFAULTS

import json, os
from django.utils.encoding import smart_text
from contents.models import WantedUrl, WantedContent, WantedData
from accounts.models import Profile
User = get_user_model()

from tests.url_endpoints import URL

class WantedContetnsAPITestCase(TestCase):
    '''
    Wanted Contents REST API testing module
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


    def test_wanted_contents_api(self):
        # post
        # unauthorized case
        response = self.client.post(
            URL['job_contents'],
            self.wanted_contents,
            format='json',
        )
        self.assertEqual(WantedContent.objects.all().count(), 0, msg='user data not created properly')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        # authorized case
        response = self.client.post(
            URL['job_contents'],
            self.wanted_contents,
            HTTP_AUTHORIZATION='JWT ' + self.token,
            format='json',
        )
        self.assertEqual(WantedContent.objects.all().count(), 1, msg='user data not created properly')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # authorized case
        response = self.client.get(
            URL['job_contents'],
            HTTP_AUTHORIZATION='JWT ' + self.token,
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
        self.assertEqual(WantedUrl.objects.all().count(), 0, msg='user data not created properly')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        # authorized case
        response = self.client.post(
            URL['wanted_url'],
            self.wanted_urls,
            HTTP_AUTHORIZATION='JWT ' + self.token,
            format='json',
        )
        self.assertEqual(WantedUrl.objects.all().count(), 1, msg='user data not created properly')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # authorized case
        response = self.client.get(
            URL['wanted_url'],
            HTTP_AUTHORIZATION='JWT ' + self.token,
            format='json',
        )
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
        self.assertEqual(WantedData.objects.all().count(), 0, msg='user data not created properly')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        # authorized case
        response = self.client.post(
            URL['wanted_data'],
            self.wanted_data,
            HTTP_AUTHORIZATION='JWT ' + self.token,
            format='json',
        )
        self.assertEqual(WantedData.objects.all().count(), 1, msg='user data not created properly')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # authorized case
        response = self.client.get(
            URL['wanted_data'],
            HTTP_AUTHORIZATION='JWT ' + self.token,
            format='json',
        )
        data = response.json()['results'][0]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data['data_name'], "top_skill")
