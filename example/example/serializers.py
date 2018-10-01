from rest_framework import serializers

from .models import Question, Choice


class QuestionSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Question


class ChoiceSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Choice