from rest_framework import serializers
from bboard.models import Bb
from bboard.models import Rubric

class RubricSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Rubric
        fields = ('id', 'name')

class BbSerializer(serializers.ModelSerializer):
# class BbSerializer(serializers.HyperLinkedModelSerializer):

    class Meta:
        model = Bb
        fields = ('title', 'price', 'rubric')