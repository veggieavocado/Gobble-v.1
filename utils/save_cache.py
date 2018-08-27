import redis, json

import os, sys, glob, re
from django.core.wsgi import get_wsgi_application
from datetime import datetime

start_path = os.getcwd()
proj_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "molecular.settings")
sys.path.append(proj_path)
os.chdir(proj_path)
application = get_wsgi_application()


from contents.models import (
    KreditJobContent,
    GoogleTrendsContent
)

from molecular.settings import IP_ADDRESS

### google trends 와 kredit job 데이터 cache로 송신
class SendCache(object):

    def save_data_to_cache(self, redis_client, key, value):
        redis_client.delete(key)
        redis_client.set(key, json.dumps(value))

    def convert_obj_json(self, tools):
        # 관련 컨텐츠 모델을 가져온다
        json_list = []
        if tools == "kredit":
            kredit_models = KreditJobContent.objects.using('contents').all()
            for obj in kredit_models:
                d = {'company': obj.company, 'industry': obj.industry, 'location': obj.location,\
                    'starting_income': obj.starting_income, 'average_income': obj.average_income}
                json_list.append(d)
        elif tools == "googleKR":
            google_models = GoogleTrendsContent.objects.using('contents').filter(geo="KR")
            for obj in google_models:
                d = {'keyword': obj.keyword, 'starting_date': obj.starting_date,\
                    'end_date': obj.end_date,'data': obj.data, 'geo':obj.geo}
                json_list.append(d)
        elif tools == "googleUS":
            google_models = GoogleTrendsContent.objects.using('contents').filter(geo="US")
            for obj in google_models:
                d = {'keyword': obj.keyword, 'starting_date': obj.starting_date,\
                    'end_date': obj.end_date,'data': obj.data, 'geo':obj.geo}
                json_list.append(d)
        else:
            print("기능이 없습니다.")
            print("kredit, googleKR, googleUS 중에서 고르시오")
        return json_list

    def make_data_for_website(self, tools):
        # 캐싱할 데이터 정의내리는 곳/저장까지
        redis_client = redis.Redis(host=IP_ADDRESS,
                                   port=6379,
                                   password='molecularredispassword')

        if tools == "kredit":
            json_data = self.convert_obj_json(tools)
            self.save_data_to_cache(redis_client, 'KREDIT_JOB_DATA', json_data)
        elif tools == "googleKR":
            json_data = self.convert_obj_json(tools)
            self.save_data_to_cache(redis_client, 'GOOGLE_TRENDS_KR_DATA', json_data)
        elif tools == "googleUS":
            json_data = self.convert_obj_json(tools)
            self.save_data_to_cache(redis_client, 'GOOGLE_TRENDS_US_DATA', json_data)
