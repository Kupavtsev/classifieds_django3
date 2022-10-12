from rest_framework import serializers
from bboard.models import Bb

class BbSerializer(serializers.ModelSerializer):
# class BbSerializer(serializers.HyperLinkedModelSerializer):

    class Meta:
        model = Bb
        fields = ('title', 'price', 'rubric')