import pytest

from algorithms.nlp.eng_nlp import (
    text_freq,
    sentence_tokenize,
    word_pos_tag,
)

##### English NLP 테스트 #####

TEXT_SENT = 'hello hello world world'

## Test 시작 ##
def test_text_freq():
    result = text_freq(TEXT_SENT)
    assert result == [{'name': 'hello', 'y': 2}, {'name': 'world', 'y': 2}]
