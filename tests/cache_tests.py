'''
Molecular.

 ʕ•ﻌ•ʔ     ʕ•ﻌ•ʔ
( >  <) ♡ (>  < )
 u   u     u   u

feat. peepee
with love...
'''
import pytest

from django.core.cache import cache
from molecular.settings import DOCKER


## Test 시작 ##
@pytest.fixture
def cache_data():
    if DOCKER == 'False':
        return 1
    else:
        cache_data = '장고 캐시 데이터'
        res = cache.set('test_cache_key', cache_data)
        assert res == True # 캐시 데이터를 저장할 수 있다
        return cache_data

def test_cache_can_get_and_delete_key(cache_data):
    if DOCKER == 'False':
        assert cache_data == 1
    else:
        value = cache.get('test_cache_key')
        assert value == cache_data

        res = cache.delete('test_cache_key')
        assert res == True
