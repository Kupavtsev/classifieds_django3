from pyexpat import model
from rest_framework import serializers
from bboard.models import Rubric

class RubricSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Rubric
        fields = ('id', 'name')