from django.shortcuts import render, get_object_or_404
from django.db.models.aggregates import Count
from django.forms import BaseFormSet, formset_factory
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q

from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, DestroyModelMixin
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .pagination import DefaultPagination
from .serializers import SurveySerializer, AddQuestionSerializer, EditQuestionSerializer, QuestionSerializer, OptionSerializer
from .models import Survey, Question, Option
from core.models import User, Customer
from .permissions import IsAdminOrReadOnly

class SurveyViewSet(ModelViewSet):

    queryset = Survey.objects.annotate(question_count=Count('question')).all()
    serializer_class = SurveySerializer
    # permission_classes = [IsAdminOrReadOnly]
    permission_classes = [IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    

    def get_serializer_context(self):
        return {'customer_id': self.request.user.id}


class SurveyQuestionViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']
    def get_queryset(self):
        return Question.objects.filter(survey=self.kwargs['survey_pk']).select_related('survey')

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddQuestionSerializer
        elif self.request.method == 'PATCH':
            return EditQuestionSerializer
        return QuestionSerializer
    
    def get_serializer_context(self):
        return {'survey': self.kwargs['survey_pk']}




class QuestionViewSet(ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['survey']
    pagination_class = DefaultPagination
    search_fields = ['question']
    ordering_fields = ['question']
    permission_classes = [IsAuthenticated]
    # filter_class = QuestionFilter

    def get_queryset(self):
        print('###########################################')



        if self.request.user.is_staff:
            return Question.objects.all()
        customer_id = Customer.objects.only('id').get(user_id=self.request.user.id)

        return Question.objects.filter(customer_id=customer_id)

    def get_serializer_context(self):
        return {'request': self.request}

    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)




class OptionViewSet(ModelViewSet):

    serializer_class = OptionSerializer

    def get_queryset(self):
        return Option.objects.filter(question_id=self.kwargs['question_pk'])

    def get_serializer_context(self):
        return {'question_id': self.kwargs['question_pk']}

######
class CartViewSet(CreateModelMixin, RetrieveModelMixin, DestroyModelMixin, GenericViewSet):
    queryset = Survey.objects.all()
    serializer_class = SurveySerializer
