from django.shortcuts import render, get_object_or_404
from django.db.models.aggregates import Count
from django.forms import BaseFormSet, formset_factory


from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .forms import Create_question_form, Create_option_form, BaseOptionFormset
from .serializers import QuestionSerializer, SurveySerializer
from .models import Survey, Question, Option


class SurveyList(APIView):
    def get(self, request):
        surveys_qs = Survey.objects.annotate(
            question_count=Count('question')).all()
        serializer = SurveySerializer(surveys_qs, many=True)
        return Response(serializer.data)
  
    def post(self, request):
        serializer = SurveySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        print(serializer.validated_data)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)



@api_view(['GET', 'POST'])
def survey_list(request):
    if request.method == 'GET':
        surveys_qs = Survey.objects.annotate(
            question_count=Count('question')).all()
        serializer = SurveySerializer(surveys_qs, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = SurveySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        print(serializer.validated_data)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
def survey_detail(request, pk):
    survey_obj = get_object_or_404(
        Survey.objects.annotate(
            question_count=Count('question')), pk=pk)

    if request.method == 'GET':
        serializer = SurveySerializer(survey_obj)

        return Response(serializer.data)

    if request.method == 'PUT':
        serializer = SurveySerializer(survey_obj, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    elif request.method == 'DELETE':
        survey_obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def question_list(request):
    if request.method == 'GET':
        questions_qs = Question.objects.select_related('survey').all()
        serializer = QuestionSerializer(questions_qs, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = QuestionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        print(serializer.validated_data)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
def question_detail(request, pk):
    question_obj = get_object_or_404(Question, pk=pk)

    if request.method == 'GET':
        serializer = QuestionSerializer(question_obj)

        return Response(serializer.data)

    if request.method == 'PUT':
        serializer = QuestionSerializer(question_obj, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    elif request.method == 'DELETE':
        question_obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
