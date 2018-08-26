from celery import shared_task

from algorithms.nlp.eng_nlp import (
    text_freq,
    sentence_tokenize,
    word_pos_tag,
)
from algorithms.nlp.wanted import WantedProcessor

@shared_task
def hello():
    print('hello there!')
    return True

@shared_task
def text_freq_task(data):
    result = text_freq(data)
    return result

@shared_task
def sentence_tokenize_task(data):
    result = sentence_tokenize(data)
    return result

@shared_task
def word_pos_tag_task(data):
    result = word_pos_tag(data)
    return result

@shared_task
def view_all_wanted_data_structures():
    w = WantedProcessor()
    wanted_content_model = w.get_wanted_model_data()
    # DATA 1
    hire_title_list = w.create_hire_title_list(wanted_content_model)
    print('1 - hire_title_list')
    print(hire_title_list)
    print('======================')
    # DATA 2
    tech_list = w.create_tech_list(wanted_content_model)
    print('2 - tech_list')
    print(tech_list)
    print('======================')
    # DATA 3
    company_tech_dict = w.create_company_tech_dict(wanted_content_model)
    print('3 - company_tech_dict')
    print(company_tech_dict)
    print('======================')
    # DATA 4
    company_hire_url_dict = w.create_company_hire_url_dict(wanted_content_model)
    print('4 - company_hire_url_dict')
    print(company_hire_url_dict)
    print('======================')
    # DATA 5
    skill_category_count = w.create_skill_category_count(hire_title_list)
    print('5 - skill_category_count')
    print(skill_category_count)
    print('======================')
    # DATA 5.5
    highcharts_skill_category_count = w.create_highcharts_skill_category_count(skill_category_count)
    print('5.5 - highcharts_skill_category_count')
    print(highcharts_skill_category_count)
    print('======================')
    # DATA 6
    sorted_skill_hire_count_list = w.create_sorted_skill_hire_count_list(tech_list)
    print('6 - sorted_skill_hire_count_list')
    print(sorted_skill_hire_count_list)
    print('======================')
    # DATA 7
    clean_sorted_top_200_skill_hire_count_list = w.create_clean_sorted_top_200_skill_hire_count_list(tech_list)
    print('7 - clean_sorted_top_200_skill_hire_count_list')
    print(clean_sorted_top_200_skill_hire_count_list)
    print('======================')
    # DATA 8
    topskill_highcharts_list = w.create_topskill_highcharts_list(clean_sorted_top_200_skill_hire_count_list)
    print('8 - topskill_highcharts_list')
    print(topskill_highcharts_list)
    print('======================')
    # DATA 9
    full_wantedjob_list = w.create_full_wantedjob_list(clean_sorted_top_200_skill_hire_count_list, company_tech_dict)
    print('9 - full_wantedjob_list')
    print(full_wantedjob_list)
    print('======================')
    # DATA 10
    wantedjob_table_list = w.create_wantedjob_table_list(clean_sorted_top_200_skill_hire_count_list, company_tech_dict)
    print('10 - wantedjob_table_list')
    print(wantedjob_table_list)
    print('======================')
    # DATA 11
    category_skill_hire_count_highcharts_data = w.create_category_skill_hire_count_highcharts_data(full_wantedjob_list)
    print('11 - category_skill_hire_count_highcharts_data')
    print(category_skill_hire_count_highcharts_data)
    print('======================')

@shared_task
def make_wanted_data_and_cache():
    w = WantedProcessor()
    w.make_data_for_website()
    return True
