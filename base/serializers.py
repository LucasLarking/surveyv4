from rest_framework import serializers
from .models import Survey, Question, Option


class SurveySerializer(serializers.ModelSerializer):
    class Meta:
        model = Survey
        fields = ['id', 'survey', 'question_count']

    question_count = serializers.IntegerField()


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'question', 'survey']

    def create(self, validated_data):
        question_obj = Question(**validated_data)
        question_obj.survey = Survey.objects.get(id=1)
        question_obj.save()
        return question_obj

    def update(self, instance, validated_data):
        instance.question = validated_data.get('question')
        instance.save()
        return instance

    def validate(self, data):
        if len(data['question']) < 2:
            return serializers.ValidationError('Too short')
        return data
