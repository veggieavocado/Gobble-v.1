from konlpy.tag import Okt, Hannanum
from nltk import pos_tag, FreqDist
from nltk.corpus import stopwords
from collections import Counter
from time import time
import redis, json
twitter = Okt()
hannanum = Hannanum()

import requests
import operator

# 외부에서 예외 처리 변수를 불러오기
from .exceptions_data import (
    CAPITAL_NAMES,
    CHANGE_NAME_DICT,
    EXCEPTION_LIST,
    WANTED_PASS_LIST,

    FRONTEND_NAMES,
    BACKEND_NAMES,
    IOS_NAMES,
    ANDROID_NAMES,
    SERVER_NAMES,
    DEVOPS_NAMES,
    DATA_NAMES,
    BLOCKCHAIN_NAMES,

    FRONTEND_SKILLS,
    BACKEND_SKILLS,
    SERVER_SKILLS,
    DEVOPS_SKILLS,
    DATA_SKILLS,
)

from contents.models import (
    WantedContent,
    WantedUrl,
    WantedData,
)

from molecular.settings import IP_ADDRESS

class WantedProcessor(object):

    def __init__(self):
        self.stop_words = set(stopwords.words('english'))
        self.stop_words.add(',')
        self.stop_words.add('.')
        self.wanted_contents_url = 'http://45.76.213.33:3000/api/v1/contents/job_contents/?page={}'
        print("Wanted Processor ready!")

    def save_data_to_db(self, name, data):
        str_data = json.dumps(data)
        db_data = WantedData(data_name=name, data=str_data)
        db_data.save(using='contents')
        print('{} saved'.format(name))

    def save_data_to_cache(self, redis_client, key, value):
        redis_client.delete(key)
        redis_client.set(key, json.dumps(value))

    # 순수 함수
    # Text에서 영어만 추출하는 함수이다. Wanted 채용 공고란 에서 기술 리스트는 대부분 영어로 되어 있기 때문이다.
    def alpha_list(self, sentence):
        pos = twitter.pos(sentence, norm=True, stem=True)
        pos_alpha = [p[0].lower() for p in pos if p[1] == 'Alpha']
        return pos_alpha

    # # request wanted api
    # # 수집한 채용 데이터를 저장한 api에 요청으로 보내서 데이터를 저장하는 함수
    # def wanted_request(self):
    #     start_time = time()
    #     i = 1
    #     tech_list = []
    #     company_dict = {}
    #     url_dict = {}
    #     r = requests.get(self.wanted_contents_url.format(1))
    #     while r.json()['next'] is not None:
    #         r = requests.get(self.wanted_contents_url.format(i))
    #         content_data = r.json()['results']
    #         for j in range(len(content_data)):
    #             content = content_data[j]['content']
    #             company = content_data[j]['company']
    #             content = content_data[j]['content']
    #             url = content_data[j]['url']
    #             if company in url_dict.keys():
    #                 url_dict[company].append(url)
    #             else:
    #                 url_dict[company] = [url]
    #             company_dict[company] = list(set(self.alpha_list(content)))
    #             temp_list = self.alpha_list(content)
    #             tech_list = tech_list + temp_list
    #         i += 1
    #     comapny_dict = company_dict
    #     tech_list = tech_list
    #     url_dict = url_dict
    #     end_time = time()
    #     print(end_time - start_time)
    #     return company_dict, tech_list, url_dict

    ##### BASE PROCESSING: 다른 작업 전에 전처리 #####
    def get_wanted_model_data(self):
        # 관련 컨텐츠 모델을 가져온다
        wanted_content_model = WantedContent.objects.using('contents').all()
        return wanted_content_model

    ##################
    ##### DATA 1 #####
    ##################
    def create_hire_title_list(self, wanted_content_data):
        # 백엔드, 프론트엔드, 서버 등등 개발자의 총 공고수를 계산하기 위해 필요
        # wanted_content_data --> WantedContent.objects.all()해서 가져온 데이터
        hire_title_list = []
        # 루프를 돌려 필요한 데이터를 위에서 만든 빈 데이터 안에 채워넣어 준다
        for i in range(len(wanted_content_data)):
            title = wanted_content_data[i].title
            hire_title_list.append(title)
        return hire_title_list

    ##################
    ##### DATA 2 #####
    ##################
    def create_tech_list(self, wanted_content_data):
        # 회사들이 사용하는 모든 기술의 집합
        tech_list = []
        for i in range(len(wanted_content_data)):
            content = wanted_content_data[i].content
            temp_list = self.alpha_list(content) # 우선은 그냥 알파 리스트를 만들어서 모두 합친다
            # 위와 같이 하면 하나의 채용 공고에서 같은 기술이 여러번 언급될 수 있다는 문제점이 있다
            tech_list = tech_list + temp_list
        return tech_list

    ##################
    ##### DATA 3 #####
    ##################
    def create_company_tech_dict(self, wanted_content_data):
        # 각 회사별로 어떤 기술을 사용하는지 모음
        company_tech_dict = {}
        for i in range(len(wanted_content_data)):
            content = wanted_content_data[i].content
            company = wanted_content_data[i].company
            company_tech_dict[company] = list(set(self.alpha_list(content)))
        return company_tech_dict

    ##################
    ##### DATA 4 #####
    ##################
    def create_company_hire_url_dict(self, wanted_content_data):
        # 회사별 공고 url 모음
        company_hire_url_dict = {}
        for i in range(len(wanted_content_data)):
            title = wanted_content_data[i].title
            company = wanted_content_data[i].company
            url = wanted_content_data[i].url
            if company in company_hire_url_dict.keys():
                company_hire_url_dict[company][title] = url
            else:
                company_hire_url_dict[company] = dict()
                company_hire_url_dict[company][title] = url
        return company_hire_url_dict

    def check_if_skill_in_title(self, title, skill_list):
        skill_exists = 0
        for skill in skill_list:
            if skill in title:
                skill_exists = 1
        return skill_exists

    ##################
    ##### DATA 5 #####
    ##################
    def create_skill_category_count(self, hire_title_list):
        skill_category_count = {
            'Frontend': 0,
            'Backend': 0,
            'iOS': 0,
            'Android': 0,
            'Server': 0,
            'Devops': 0,
            'Data Scientist': 0,
            'Blockchain': 0
        }

        for title in hire_title_list:
            frontend = self.check_if_skill_in_title(title, FRONTEND_NAMES)
            backend = self.check_if_skill_in_title(title, BACKEND_NAMES)
            ios = self.check_if_skill_in_title(title, IOS_NAMES)
            android = self.check_if_skill_in_title(title, ANDROID_NAMES)
            server = self.check_if_skill_in_title(title, SERVER_NAMES)
            devops = self.check_if_skill_in_title(title, DEVOPS_NAMES)
            data = self.check_if_skill_in_title(title, DATA_NAMES)
            blockchain = self.check_if_skill_in_title(title, BLOCKCHAIN_NAMES)

            if frontend == 1:
                skill_category_count['Frontend'] += 1
            if backend == 1:
                skill_category_count['Backend'] += 1
            if ios == 1:
                skill_category_count['iOS'] += 1
            if android == 1:
                skill_category_count['Android'] += 1
            if server == 1:
                skill_category_count['Server'] += 1
            if devops == 1:
                skill_category_count['Devops'] += 1
            if data == 1:
                skill_category_count['Data Scientist'] += 1
            if blockchain == 1:
                skill_category_count['Blockchain'] += 1

        return skill_category_count

    # 예외 처리 함수 : 중복되지만 key 값이 다른 함수 합치기
    def exception_process(self, data, parent_key, child_key, func):
        if (parent_key in data.keys()) and (child_key in data.keys()):
            if func == 'sum':
                data[parent_key] = data[parent_key] + data[child_key]
                del data[child_key]
            elif func == 'sub':
                data[parent_key] = data[parent_key] - data[child_key]
                del data[child_key]
        else:
            pass
        return data

    ##################
    ##### DATA 6 #####
    ##################
    def create_sorted_skill_hire_count_list(self, tech_list):
        # stop word들을 모두 제거한다
        total_dict = {}
        filtered_sentence = [w for w in tech_list if not w.lower() in self.stop_words]
        count_tech = Counter(filtered_sentence) # 기술별 언급 빈도수를 카운터로 계산하다

        # 빈도수가 10개 이하인 값 버리기 --> 무의미하다고 판단
        for key, value in count_tech.items():
            if value <= 10:
                continue
            total_dict[key] = value

        # 중복되지만 key 값이 다른 데이터 합치기
        for exception in EXCEPTION_LIST:
            total_dict = self.exception_process(total_dict, exception[0], exception[1], 'sum')
        total_dict = self.exception_process(total_dict, 'web', 'amazon', 'sub')

        sorted_skill_hire_count_list = sorted(total_dict.items(), key=operator.itemgetter(1), reverse=True)
        # data type is like [('aws', 514), ('api', 470),  ('web', 350), ('ios', 349),  ('c', 344), ('js', 328), ('python', 324),]
        return sorted_skill_hire_count_list

    ##################
    ##### DATA 7 #####
    ##################
    def create_clean_sorted_top_200_skill_hire_count_list(self, tech_list):
        sorted_skill_hire_count_list = self.create_sorted_skill_hire_count_list(tech_list)

        # extract top 200
        sorted_data = sorted_skill_hire_count_list[0:200]

        clean_sorted_top_200_skill_hire_count_list = []

        for d in sorted_data:
            if d[0] in WANTED_PASS_LIST:
                continue
            temp_tuple = (d[0], d[1])
            clean_sorted_top_200_skill_hire_count_list.append(temp_tuple) # TOP 200 기술을 들고와서 예외처리하면 이전에 소팅된 것을 다시 소팅해줘야 한다
        clean_sorted_top_200_skill_hire_count_list = sorted(clean_sorted_top_200_skill_hire_count_list, key=lambda tup: tup[1], reverse=True)
        return clean_sorted_top_200_skill_hire_count_list

    ##################
    ##### DATA 8 #####
    ##################
    def create_topskill_highcharts_list(self, clean_sorted_top_200_skill_hire_count_list):
        # 많이 사용되는 기술 list와 기술별 사용회사 리스트를 뽑는 것을 수행하는 함수
        # 하이차트 들어가는 데이터 형식대로 포맷팅하는 함수
        # 형식: [ {'name': 'Javascript', 'y': 1, 'sliced': 'true', 'selected': 'true' }, {'name': 'AWS', 'y': 1}, ... ]
        topskill_highcharts_list = []
        first_item = 1
        for d in clean_sorted_top_200_skill_hire_count_list:
            chart_dict = {}
            # 먼저 예외처리를 한다 --> 이름을 수정해야할 수도 있기 때문에
            if d[0] in CHANGE_NAME_DICT.keys():
                chart_dict['name'] = CHANGE_NAME_DICT[d[0]]
            elif d[0] in CAPITAL_NAMES:
                chart_dict['name'] = d[0].upper()
            else:
                chart_dict['name'] = d[0].title()
            chart_dict['y'] = d[1]
            chart_dict['states'] = {
                'select': { 'color': '#FF385A' },
                'hover': { 'color': '#d1d1d1' }
            }
            if first_item == 1: # 첫 번째 데이터값이면 selected, sliced를 true로 설정한다
                chart_dict['sliced'] = 1
                chart_dict['selected'] = 1 # 1로 해도 true와 같다
            topskill_highcharts_list.append(chart_dict)
            first_item = 0
        return topskill_highcharts_list

    ##################
    ##### DATA 9 #####
    ##################
    def create_full_wantedjob_list(self, clean_sorted_top_200_skill_hire_count_list, company_tech_dict):
        wanted_job = {}
        tech_compare_list = []
        for d in clean_sorted_top_200_skill_hire_count_list:
            if d[0] in WANTED_PASS_LIST:
                # 불필요한 데이터는 먼저 걸러낸다
                continue
            wanted_job[d[0]] = [d[1],[]] # 두 번째 리스트값에는 회사 이름을 넣을 것이다
            tech_compare_list.append(d[0])

        # make job_list
        for k in company_tech_dict.keys():
            for tech in tech_compare_list:
                if tech in company_tech_dict[k]:
                    wanted_job[tech][1].append(k)

        total_list = list(CHANGE_NAME_DICT.keys()) + CAPITAL_NAMES
        # pop 이되면 데이터가 순서상 마지막으로 추가 되어서 문제가 발생하여
        # 반복문을 두개로 쪼개서 실행
        for key, v in wanted_job.items():
            if key not in total_list:
                # 예외처리를 따로 할 필요가 없으면, 첫 단어만 대문자로 바꿔서 저장한다
                wanted_job[key.title()] = wanted_job.pop(key)
        for key, v in wanted_job.items():
            if key in CHANGE_NAME_DICT.keys():
                wanted_job[CHANGE_NAME_DICT[key]] = wanted_job.pop(key)
            elif key in CAPITAL_NAMES:
                wanted_job[key.upper()] = wanted_job.pop(key)
        # pop으로 dict의 key 값을 변환해주어서 다시 순서를 sort해줘야함
        sorted_tuple = sorted(wanted_job.items(), key=operator.itemgetter(1), reverse=True)

        # 최종 결과물을 담을 딕셔너리를 만든다
        full_wantedjob_list = {}

        # sort 된값은 tuple로 저장되므로 다시 dict 형태로 바꾸어야 한다.
        for data in sorted_tuple:
            full_wantedjob_list[data[0]] = data[1]
        return full_wantedjob_list

    ###################
    ##### DATA 10 #####
    ###################
    def create_wantedjob_table_list(self, clean_sorted_top_200_skill_hire_count_list, company_tech_dict):
        # 원티드 데이터 페이지 테이블 부분에 들어가는 데이터이다
        # 리턴되어야 하는 형식: [name, hire_count, [comp1, comp2, comp3, comp4]] --> comp는 무조건 4개
        wanted_job = {}
        tech_compare_list = []
        for d in clean_sorted_top_200_skill_hire_count_list:
            if d[0] in WANTED_PASS_LIST:
                # 불필요한 데이터는 먼저 걸러낸다
                continue
            wanted_job[d[0]] = [d[1],[]] # 두 번째 리스트값에는 회사 이름을 넣을 것이다
            tech_compare_list.append(d[0])

        # make job_list
        for k in company_tech_dict.keys():
            for tech in tech_compare_list:
                if tech in company_tech_dict[k]:
                    wanted_job[tech][1].append(k)

        total_list = list(CHANGE_NAME_DICT.keys()) + CAPITAL_NAMES
        # pop 이되면 데이터가 순서상 마지막으로 추가 되어서 문제가 발생하여
        # 반복문을 두개로 쪼개서 실행
        for key, v in wanted_job.items():
            if key not in total_list:
                # 예외처리를 따로 할 필요가 없으면, 첫 단어만 대문자로 바꿔서 저장한다
                wanted_job[key.title()] = wanted_job.pop(key)
        for key, v in wanted_job.items():
            if key in CHANGE_NAME_DICT.keys():
                wanted_job[CHANGE_NAME_DICT[key]] = wanted_job.pop(key)
            elif key in CAPITAL_NAMES:
                wanted_job[key.upper()] = wanted_job.pop(key)
        # pop으로 dict의 key 값을 변환해주어서 다시 순서를 sort해줘야함
        sorted_tuple = sorted(wanted_job.items(), key=operator.itemgetter(1), reverse=True)

        # 최종 결과물을 담을 리스트를 만든다
        wantedjob_table_list = []

        # sort 된값은 tuple로 저장된다. 리스트 형식으로 변형한다
        for data in sorted_tuple:
            wantedjob_table_list.append([data[0], data[1][0], data[1][1]])
        return wantedjob_table_list

    def make_data_for_website(self, wantedjob_list):
        # 캐싱할 데이터 정의내리는 곳/저장까지
        ### 메인 색상: 초록(#00C73C), 파랑(#0183DA), 빨강(#FF385A), 주황(#FF6813), 회색(#D1D1D1), 아주연한회색(#EFEFEF)
        redis_client = redis.Redis(host=IP_ADDRESS,
                                   port=6379,
                                   password='molecularredispassword')

        wanted_content_data = self.get_wanted_model_data()
        wanted_content_data = self.get_wanted_model_data()
        company_tech_dict = self.create_company_tech_dict(wanted_content_data)
        tech_list = self.create_tech_list(wanted_content_data)
        clean_sorted_top_200_skill_hire_count_list = self.create_clean_sorted_top_200_skill_hire_count_list(tech_list)
        # 원티드 데이터 페이지 메인 랭크 테이블 데이터: 상위 5개 기술 기술명, 점유율, 공고수, 관련스타트업 4개
        wantedjob_table_list = self.create_wantedjob_table_list(clean_sorted_top_200_skill_hire_count_list, company_tech_dict)
        self.save_data_to_cache(redis_client, 'WANTED_SKILL_RANK_TABLE_DATA', wantedjob_table_list)

    # def cache_wanted_page_data(self, skill_count):
    #     redis_client = redis.Redis(host=IP_ADDRESS,
    #                                port=6379,
    #                                password='molecularredispassword')
    #
    #
    #
    #     self.save_data_to_cache(redis_client, 'WANTED_TOP_5_SKILL:COUNT:COMPS_LIST', main_wantedjob_table_list)
    #
    #     # 원티드 기술점유율 도넛 하이차트 데이터: { 'name', 'y', 'showInLegend', 'states': {{'select': 'color'}, {'hover': 'color'}} }
    #     # select - color: #FF385A, hover - color: #D1D1D1
    #     # 100개 기술 모두의 정보가 들어가야하지만, 상위 6개만 showInLegend: true, 나머지는 false
    #     self.save_data_to_cache(redis_client, 'WANTED_TOP_6_FOCUSED_SKILL:COUNT_CHART_DATA', )
    #
    #     # 원티드 직군별 공고수 바차트 데이터:
    #     # 데이터 형식: [{'y', 'color'}, ... ] --> 공고수 최대값인 데이터는 색상 다르게, 나머지는 모두 회색
    #     self.save_data_to_cache(redis_client, 'WANTED_HIRE:COUNT_CHART_DATA', skill_count)
    #
    #     # 원티드 직군에서 사용 기술 공고수 바차트 데이터:
    #     # 데이터 형식: [{'name', 'data': [{'y', 'color'}, ... ]}, ... ]
    #     self.save_data_to_cache(redis_client, 'WANTED_HIRE_SKILLS_COUNT_CHART_DATA', )
    #
    #     self.save_data_to_cache(redis_client, 'WANTED_TOTAL_SKILL_COUNT_COMPS_LIST', wantedjob_list)
    #
    #     self.save_data_to_cache(redis_client, 'WANTED_HIRE_URL_DATA', url_dict)
