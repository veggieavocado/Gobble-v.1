import nltk
import operator

import ssl

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context
    
nltk.download('punkt')
nltk.download("stopwords")
nltk.download('averaged_perceptron_tagger')
from nltk import FreqDist, ngrams, pos_tag
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize

def text_freq(text):
    tokens = nltk.word_tokenize(text)
    stop_words = set(stopwords.words('english'))
    stop_words.add(',')
    stop_words.add('.')
    filtered_sentence = [w for w in tokens if not w.lower() in stop_words]
    filtered_sentence = [word for word in filtered_sentence if len(word) > 3]
    filtered_sentence = [word for word in filtered_sentence if not word.isnumeric()]
    freq= FreqDist(filtered_sentence)
    word_freq = sorted(dict(freq).items(), key=operator.itemgetter(1), reverse=True)
    hc_list = [{'name':name,'y':value} for name, value in word_freq] # y로 값을 반환하지 않으면 highcharts가 뜨지 않음
    # hc_list = [[name, value] for name, value in word_freq]
    return hc_list

def sentence_tokenize(text):
    sentence_tokens = sent_tokenize(text)
    sentence_list = {'sentences':sentence_tokens}
    return sentence_list

def word_pos_tag(text):
    tokens = nltk.word_tokenize(text)
    stop_words = set(stopwords.words('english'))
    stop_words.add(',')
    stop_words.add('.')
    filtered_sentence = [w for w in tokens if not w.lower() in stop_words]
    filtered_sentence = [word for word in filtered_sentence if len(word) > 3]
    filtered_sentence = [word for word in filtered_sentence if not word.isnumeric()]
    pos_tag_list = pos_tag(filtered_sentence)
    pos_tag_result = {'pos_tags':pos_tag_list}
    return pos_tag_result
