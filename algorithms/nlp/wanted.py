from konlpy.tag import Okt, Hannanum
from nltk import pos_tag, FreqDist
from nltk.corpus import stopwords
from collections import Counter
from time import time
import json
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
)

from contents.models import (
    WantedContent,
    WantedUrl,
    WantedData,
)

class WantedProcessor(object):

    def __init__(self):
        self.stop_words = set(stopwords.words('english'))
        self.stop_words.add(',')
        self.stop_words.add('.')
        self.wanted_contents_url = 'http://45.76.213.33:3000/api/v1/contents/job_contents/?page={}'
        print("Wanted Processor ready!")

    # 순수 함수
    # Text에서 영어만 추출하는 함수이다. Wanted 채용 공고란 에서 기술 리스트는 대부분 영어로 되어 있기 때문이다.
    def alpha_list(self, sentence):
        pos = twitter.pos(sentence, norm=True, stem=True)
        pos_alpha = [p[0].lower() for p in pos if p[1] == 'Alpha']
        return pos_alpha

    # request wanted api
    # 수집한 채용 데이터를 저장한 api에 요청으로 보내서 데이터를 저장하는 함수
    def wanted_request(self):
        start_time = time()
        i = 1
        tech_list = []
        company_dict = {}
        url_dict = {}
        r = requests.get(self.wanted_contents_url.format(1))
        while r.json()['next'] is not None:
            r = requests.get(self.wanted_contents_url.format(i))
            content_data = r.json()['results']
            for j in range(len(content_data)):
                content = content_data[j]['content']
                company = content_data[j]['company']
                content = content_data[j]['content']
                url = content_data[j]['url']
                if company in url_dict.keys():
                    url_dict[company].append(url)
                else:
                    url_dict[company] = [url]
                company_dict[company] = list(set(self.alpha_list(content)))
                temp_list = self.alpha_list(content)
                tech_list = tech_list + temp_list
            i += 1
        comapny_dict = company_dict
        tech_list = tech_list
        url_dict = url_dict
        end_time = time()
        print(end_time - start_time)
        return company_dict, tech_list, url_dict

    # 데이터 프로세싱 시작 전에 모델에서 필요한 데이터 모두 가져오기
    def wanted_model(self):
        # 관련 컨텐츠 모델을 가져온다
        wanted_content_model = WantedContent.objects.using('contents').all()
        # 채워넣을 빈 데이터를 만든다
        title_list = [] # 백엔드, 프론트엔드, 서버 등등 개발자의 총 공고수를 계산하기 위해 필요
        tech_list = [] # 회사들이 사용하는 모든 기술의 집합
        company_dict = {} # 각 회사별로 어떤 기술을 사용하는지 모음
        url_dict = {} # 회사별 공고 url 모음
        # 루프를 돌려 필요한 데이터를 위에서 만든 빈 데이터 안에 채워넣어 준다
        for i in range(len(wanted_content_model)):
            title = wanted_content_model[i].title
            content = wanted_content_model[i].content
            company = wanted_content_model[i].company
            url = wanted_content_model[i].url
            title_list.append(title)
            if company in url_dict.keys():
                url_dict[company][title] = url
            else:
                url_dict[company] = dict()
                url_dict[company][title] = url
            company_dict[company] = list(set(self.alpha_list(content)))
            temp_list = self.alpha_list(content)
            tech_list = tech_list + temp_list
        company_dict = company_dict
        tech_list = tech_list
        url_dict = url_dict
        return title_list, company_dict, tech_list, url_dict

    def check_if_skill_in_title(self, title, skill_list):
        skill_exists = 0
        for skill in skill_list:
            if skill in title:
                skill_exists = 1
        return skill_exists

    def create_skill_category_count(self, title_list):
        skill_count = {
            'Frontend': 0,
            'Backend': 0,
            'iOS': 0,
            'Android': 0,
            'Server': 0,
            'Devops': 0,
            'Data Scientist': 0,
            'Blockchain': 0
        }

        for title in title_list:
            frontend = self.check_if_skill_in_title(title, FRONTEND_NAMES)
            backend = self.check_if_skill_in_title(title, BACKEND_NAMES)
            ios = self.check_if_skill_in_title(title, IOS_NAMES)
            android = self.check_if_skill_in_title(title, ANDROID_NAMES)
            server = self.check_if_skill_in_title(title, SERVER_NAMES)
            devops = self.check_if_skill_in_title(title, DEVOPS_NAMES)
            data = self.check_if_skill_in_title(title, DATA_NAMES)
            blockchain = self.check_if_skill_in_title(title, BLOCKCHAIN_NAMES)

            if frontend == 1:
                skill_count['Frontend'] += 1
            if backend == 1:
                skill_count['Backend'] += 1
            if ios == 1:
                skill_count['iOS'] += 1
            if android == 1:
                skill_count['Android'] += 1
            if server == 1:
                skill_count['Server'] += 1
            if devops == 1:
                skill_count['Devops'] += 1
            if data == 1:
                skill_count['Data Scientist'] += 1
            if blockchain == 1:
                skill_count['Blockchain'] += 1

        return skill_count

    # 예외 처리 함수 : 중복되지만 key 값이 다른 함수 합치기
    def exception_process(self, data, parent_key, child_key, func):
        if parent_key and child_key in data.keys():
            if func == 'sum':
                data[parent_key] = data[parent_key] + data[child_key]
                del data[child_key]
            elif func == 'sub':
                data[parent_key] = data[parent_key] - data[child_key]
                del data[child_key]
        else:
            pass
        return data

    # Wanted Data 전처리
    def refine_data(self, tech_list):
        filtered_sentence = [w for w in tech_list if not w.lower() in self.stop_words]
        total_dict = {}
        count_tech = Counter(filtered_sentence)

        # 빈도수가 10개 이하인 값 버리기
        for key, value in count_tech.items():
            if value <= 10:
                continue
            total_dict[key] = value

        # 중복되지만 key 값이 다른 데이터 합치기
        for exception in EXCEPTION_LIST:
            total_dict = self.exception_process(total_dict, exception[0], exception[1], 'sum')
        total_dict = self.exception_process(total_dict, 'web', 'amazon', 'sub')

        sorted_x = sorted(total_dict.items(), key=operator.itemgetter(1), reverse=True)
        # data type is like [('aws', 514), ('api', 470),  ('web', 350), ('ios', 349),  ('c', 344), ('js', 328), ('python', 324),]
        # extract top 200
        sorted_data = sorted_x[0:200]
        js1 = js2 = amazon = web = rest = react = node = angular = vue = front = back = 0
        refine_skill = []
        exception_dict = {}
        for d in sorted_data:
            temp_dict = {}
            if d[0] in WANTED_PASS_LIST:
                continue
            temp_tuple = (d[0], d[1])
            refine_skill.append(temp_tuple)
        final_sorted_list = sorted(refine_skill, key=lambda tup: tup[1], reverse=True)
        return final_sorted_list

    # 많이 사용되는 기술 list와 기술별 사용회사 리스트를 뽑는 것을 수행하는 함수
    def create_topskill_list(self, final_sorted_list, tech_list):
        top_skill = []
        for d in final_sorted_list:
            chart_dict = {}
            if d[0] in CHANGE_NAME_DICT.keys():
                chart_dict['name'] = CHANGE_NAME_DICT[d[0]]
            elif d[0] in CAPITAL_NAMES:
                chart_dict['name'] = d[0].upper()
            else:
                chart_dict['name'] = d[0].title()
            chart_dict['y'] = d[1]
            top_skill.append(chart_dict)
        return top_skill

    def create_wantedjob_list(self, final_sorted_list, company_dict):
        wanted_job = {}
        tech_compare_list = []
        for d in final_sorted_list:
            if d[0] in WANTED_PASS_LIST:
                continue
            wanted_job[d[0]] = [d[1],[]]
            tech_compare_list.append(d[0])

        # make job_list
        for k in company_dict.keys():
            for tech in tech_compare_list:
                if tech in company_dict[k]:
                    wanted_job[tech][1].append(k)
        result_dict = {}

        total_list = list(CHANGE_NAME_DICT.keys()) + CAPITAL_NAMES
        # pop 이되면 데이터가 순서상 마지막으로 추가 되어서 문제가 발생하여
        # 반복문을 두개로 쪼개서 실행
        for key, v in wanted_job.items():
            if key not in total_list:
                wanted_job[key.title()] = wanted_job.pop(key)
        for key, v in wanted_job.items():
            if key in CHANGE_NAME_DICT.keys():
                wanted_job[CHANGE_NAME_DICT[key]] = wanted_job.pop(key)
            elif key in CAPITAL_NAMES:
                wanted_job[key.upper()] = wanted_job.pop(key)
        # pop으로 dict의 key 값을 변환해주어서 다시 순서를 sort해줘야함
        sorted_tuple = sorted(wanted_job.items(), key=operator.itemgetter(1), reverse=True)
        # sort 된값은 tuple로 저장되므로 다시 dict 형태로 바꾸어야 한다.
        for data in sorted_tuple:
            result_dict[data[0]] = data[1]
        return result_dict

    def save_data_to_db(self, name, data):
        str_data = json.dumps(data)
        db_data = WantedData(data_name=name, data=str_data)
        db_data.save()
        print('{} saved'.format(name))
