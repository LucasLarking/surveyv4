from django.shortcuts import render, get_object_or_404
from django.db.models.aggregates import Count
from django.forms import BaseFormSet, formset_factory


from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import QuestionSerializer, SurveySerializer
from .models import Survey, Question


class SurveyList(ListCreateAPIView):
    queryset = Survey.objects.annotate(question_count=Count('question')).all()
    serializer_class = SurveySerializer


class SurveyDetail(RetrieveUpdateDestroyAPIView):
    queryset = Survey.objects.annotate(question_count=Count('question'))
    serializer_class = SurveySerializer

    def delete(self, request, pk):
        survey_obj = get_object_or_404(Survey.objects.annotate(question_count=Count('question')), pk=pk)
        survey_obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class QuestionList(ListCreateAPIView):
    queryset = Question.objects.select_related('survey').all()
    serializer_class = QuestionSerializer

    def get_serializer_context(self):
        return {'request':self.request}


class QuestionDetail(RetrieveUpdateDestroyAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    def delete(self, request, pk):
        question_obj = get_object_or_404(Question, pk=pk)
        question_obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

