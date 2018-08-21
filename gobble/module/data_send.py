import os, sys, glob
from django.core.wsgi import get_wsgi_application
from datetime import datetime

start_path = os.getcwd()
proj_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "molecular.settings")
sys.path.append(proj_path)
os.chdir(proj_path)

application = get_wsgi_application()
from molecular.settings import PRODUCTION
from gobble.module.naver_m_crawler import NaverMajorCrawler
from gobble.module.naver_rt_crawler import NaverRealtimeCrawler

from contents.models import NaverContent

TODAY = datetime.today().strftime("%Y-%m-%d")

def make_checklist(new_type, date, value):
    if PRODUCTION == True:
        all_url = NaverContent.objects.using('contents').filter(data_type=new_type).filter(upload_time__contains=TODAY).values_list(value)
        checklist = [a[0] for a in all_url]
    elif PRODUCTION == False:
        all_url = NaverContent.objects.filter(data_type=new_type).filter(upload_time__contains=TODAY).values_list(value)
        checklist = [a[0] for a in all_url]
    checklist = list(set(checklist))
    return checklist

# func (기능): all (오늘 날짜의 모든 뉴스를 크롤링), new (1page만 크롤링)
# data_type (데이터 종류) : major(주요뉴스), rt(실시간 속보)
def NaverDataSend(func, new_type):
    if new_type == "major":
        nnc = NaverMajorCrawler()
        checklist = make_checklist('M', TODAY, 'url')
    elif new_type == "rt":
        nnc = NaverRealtimeCrawler()
        checklist = make_checklist('R', TODAY, 'url')
    else:
        print("major와 rt 중에 선택하시오.")

    if func == 'new':
        nnc_url = nnc.create_url_list(func='new')
    elif func == 'all':
        nnc_url = nnc.create_url_list(func='all')
    else:
        print("major와 rt 중에 선택하시오.")

    nnc_data = nnc.get_data(nnc_url, checklist)
    if len(nnc_data) == 0:
        print('Already up-to-date.')
    else:
        for nnc_part in nnc_data:
            title = nnc_part['title']
            url = nnc_part['url']
            upload_time = nnc_part['upload_time']
            media = nnc_part['media']
            data_type = nnc_part['data_type']
            if new_type == "major":
                content = nnc_part['contents']
                naver_content_orm = NaverContent(title=title, url=url, upload_time=upload_time,\
                                                media=media, data_type=data_type, content=content)
            elif new_type == "rt":
                naver_content_orm = NaverContent(title=title, url=url, upload_time=upload_time,\
                                                media=media, data_type=data_type)
            else:
                print("major와 rt 중에 선택하시오.")
            if PRODUCTION == True:
                naver_content_orm.using('contents').save()
            else:
                naver_content_orm.save()
        print('DB Send Success')
