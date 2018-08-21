from django.shortcuts import render
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from algorithms.tasks import (
    text_freq_task,
    sentence_tokenize_task,
    word_pos_tag_task,
)


#*** UPDATE: 20180816 ***#
class TestAPIView(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request, *args, **kwargs):
        result = {'status': 'GOOD'}
        return Response(result, status=status.HTTP_200_OK)


#*** UPDATE: 20180816 ***#
class AlgorithmTestAPIView(APIView):
    # 레퍼런스: http://www.django-rest-framework.org/api-guide/status-codes/ (status code)

    ## /gobble/api/<version>/algo_test/ ##
    # version: v1
    # algorithm: NLP
    # taskname: i.e. TEXT_FREQ, SENTENCE_TOKENIZE etc.
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        algorithm = request.data['algorithm']
        type = request.data['type']
        data = request.data['data']

        taskname = type.lower()

        ##### ALGO #1 #####
        if algorithm == 'NLP':
            # 태스크 처리하기
            if taskname == 'text_freq':
                result = text_freq_task(data)
            elif taskname == 'sentence_tokenize':
                result = sentence_tokenize_task(data)
            elif taskname == 'word_pos_tag':
                result = word_pos_tag_task(data)

        # 없는 알고리즘 예외 처리하기
        else:
            # 받은 알고리즘 값이 존재하지 않는 알고리즘이면 '없는 알고리즘'이라고 리턴
            result = '없는 알고리즘'

        # 위에서 받은 result 값을 result_json에 result키값으로 넣어준다
        if result == '없는 알고리즘':
            result_json = {'status': 'FAIL', 'result': result}
            return Response(result_json, status=status.HTTP_400_BAD_REQUEST)
        else:
            result_json = {'status': 'GOOD', 'result': result}
            return Response(result_json, status=status.HTTP_200_OK)


#*** UPDATE: 20180816 ***#
class TaskAPIView(APIView):
    # 레퍼런스: http://www.django-rest-framework.org/api-guide/status-codes/ (status code)

    ## /gobble/api/<version>/ ##
    # version: v1
    # algorithm: NLP
    # taskname: i.e. TEXT_FREQ, SENTENCE_TOKENIZE etc.
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        algorithm = request.data['algorithm']
        type = request.data['type']
        data = request.data['data']

        taskname = type.lower()

        ##### ALGO #1 #####
        if algorithm == 'NLP':
            # 태스크 처리하기
            if taskname == 'text_freq':
                text_freq_task.delay(data)
            elif taskname == 'sentence_tokenize':
                sentence_tokenize_task.delay(data)
            elif taskname == 'word_pos_tag':
                word_pos_tag_task.delay(data)

            result = '태스크 전송 성공'

        # 없는 알고리즘 예외 처리하기
        else:
            # 받은 알고리즘 값이 존재하지 않는 알고리즘이면 '없는 알고리즘'이라고 리턴
            result = '없는 알고리즘'

        # 위에서 받은 result 값을 result_json에 result키값으로 넣어준다
        if result == '없는 알고리즘':
            result_json = {'status': 'FAIL', 'result': result}
            return Response(result_json, status=status.HTTP_400_BAD_REQUEST)
        else:
            result_json = {'status': 'GOOD', 'result': result}
            return Response(result_json, status=status.HTTP_200_OK)
