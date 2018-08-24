from rest_framework import serializers
from contents.models import (
    WantedContent,
    WantedUrl,
    WantedData,
    NaverData,
    NaverContent,
    KreditJobContent,
    GoogleTrendsContent,
    )


class WantedContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = WantedContent
        fields = "__all__"


class WantedUrlSerializer(serializers.ModelSerializer):
    class Meta:
        model = WantedUrl
        fields = "__all__"


class WantedDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = WantedData
        fields = "__all__"


class NaverContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = NaverContent
        fields = "__all__"


class NaverDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = NaverData
        fields = "__all__"


class KreditJobContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = KreditJobContent
        fields = "__all__"


class GoogleTrendsContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoogleTrendsContent
        fields = "__all__"
