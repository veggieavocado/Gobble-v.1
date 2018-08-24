import pytest

from algorithms.nlp.kor_nlp import korean_text_pre
from tests.expected_value import (
    token_value,
    pos_value,
    noun_value,
    )
##### korean NLP 테스트 #####

TEXT_SENT = '금융감독원이 삼성바이오로직스 회계처리 위반에 대한 재감리에 돌입했다.15일 금융당국에 따르면 금감원은 최근 재감리를 시작하고 최대한 빨리 진행하기로 했다. 특히 연말까지는 감리 조치안을 마무리한다는 방침이다.'
TEXT_SENT2 = '안녕 안녕 감사'

## Test 시작 ##
def test_text_tokenize():
    result = korean_text_pre(TEXT_SENT, 'token')
    assert result == token_value

def test_text_freq():
    result = korean_text_pre(TEXT_SENT2, 'count')
    assert result == [{'name':'안녕', 'y':2},{'name':'감사','y':1}]

def test_text_pos():
    result = korean_text_pre(TEXT_SENT, 'pos')
    assert result == pos_value

def test_text_noun():
    result = korean_text_pre(TEXT_SENT, 'noun')
    assert result == noun_value

def test_text_noun_value():
    result = korean_text_pre(TEXT_SENT2, 'noun_count')
    assert result == [{'name':'감사','y':1}]
