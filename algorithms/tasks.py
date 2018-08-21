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
    company_dict, tech_list, url_dict = w.wanted_model()
    final_sorted_list = w.refine_data(tech_list)
    top_skill = w.create_topskill_list(final_sorted_list, tech_list)
    wantedjob_list = w.create_wantedjob_list(final_sorted_list, company_dict)

    print(tech_list)
