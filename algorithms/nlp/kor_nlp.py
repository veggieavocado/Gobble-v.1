from konlpy.tag import Okt, Hannanum, Kkma, Mecab, Komoran
from nltk import pos_tag, FreqDist
from nltk.corpus import stopwords
from collections import Counter
twitter = Okt()
hannanum = Hannanum()
kkma = Kkma()
komoran = Komoran()

import operator

def korean_text_pre(sentence, func):
    tokens = hannanum.morphs(sentence)
    pos = hannanum.pos(sentence, ntags=22)
    noun = hannanum.nouns(sentence)
    stop_words = set(stopwords.words('english'))
    stop_words.add(',')
    stop_words.add('.')
    filtered_sentence = [w for w in tokens if not w in stop_words]
    filtered_sentence = [word for word in filtered_sentence if len(word) > 1]
    filtered_sentence = [word for word in filtered_sentence if not word.isnumeric()]
    if func == 'count':
        freq = Counter(filtered_sentence)
        word_freq = sorted(dict(freq).items(), key=operator.itemgetter(1), reverse=True)
        result = [{'name':name,'y':value} for name, value in word_freq]
    elif func == 'token':
        result = filtered_sentence
    elif func == 'pos':
        filtered_sentence = [w for w in pos if not w[0] in stop_words]
        filtered_sentence = [word for word in filtered_sentence if not word[1] == 'JC']
        filtered_sentence = [word for word in filtered_sentence if not word[1] == 'ET']
        result = filtered_sentence
    elif func == 'noun':
        result = noun
    return result

test_data = '금융감독원이 삼성바이오로직스 회계처리 위반에 대한 재감리에 돌입했다.15일 금융당국에 따르면 금감원은 최근 재감리를 시작하고 최대한 빨리 진행하기로 했다. 특히 연말까지는 감리 조치안을 마무리한다는 방침이다.'

korean_text_pre(test_data, 'token')
korean_text_pre(test_data, 'count')
korean_text_pre(test_data, 'pos')
korean_text_pre(test_data, 'noun')
