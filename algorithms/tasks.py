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
def process_wanted_data():
    w = WantedProcessor()
    title_list, company_dict, tech_list, url_dict = w.wanted_model()
    final_sorted_list = w.refine_data(tech_list)
    top_skill = w.create_topskill_list(final_sorted_list, tech_list)
    wantedjob_list = w.create_wantedjob_list(final_sorted_list, company_dict)
    skill_count = w.create_skill_category_count(title_list)

    print(url_dict)
    print(top_skill)
    print(wantedjob_list)
    print(skill_count)

    w.save_data_to_db('COMPANY_URLS', url_dict)
    w.save_data_to_db('TOP_SKILLS', top_skill)
    w.save_data_to_db('WANTED_SKILL_COMPS', wantedjob_list)
    w.save_data_to_db('SKILL_COUNTS', skill_count)

@shared_task
def make_wanted_data_and_cache():
    w = WantedProcessor()
    w.make_data_for_website()
    return True
