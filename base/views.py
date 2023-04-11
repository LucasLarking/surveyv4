import requests

from django.core.cache import cache
from django.shortcuts import render, get_object_or_404
from django.db.models.aggregates import Count
from django.forms import BaseFormSet, formset_factory
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from rest_framework import status, generics
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, DestroyModelMixin
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.views import APIView
from .pagination import DefaultPagination
from .serializers import SurveySerializer, UpdateSurveySerializer, AddQuestionSerializer, EditQuestionSerializer, QuestionSerializer, OptionSerializer
from .models import Survey, Question, Option
from core.models import User, Customer
from .permissions import IsAdminOrReadOnly

@cache_page(5*60)
def say_hello(request):
    response = requests.get('https://httpbin.org/delay/2')
    data = response.json()
    return render(request, 'hello.html', {'cache': data})


class HelloView(APIView):
    @method_decorator(cache_page(5*60))
    def get(self, request):
        response = requests.get('https://httpbin.org/delay/2')
        data = response.json()
        return render(request, 'hello.html', {'cache': data})


class SurveyViewSet(ModelViewSet):
    http_method_names = ['get', 'patch', 'delete', 'head', 'option', 'post']
    queryset = Survey.objects.annotate(question_count=Count('question')).prefetch_related('question_set').all()
    # serializer_class = SurveySerializer
    # permission_classes = [IsAdminOrReadOnly]
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.request.method in ['PATCH', 'DELETE']:
            return [IsAdminUser()]
        return [IsAuthenticated()]

    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    

    def get_serializer_context(self):
        return {'customer_id': self.request.user.id}
    
    def get_serializer_class(self):
        if self.request.method == 'PATCH':
            return UpdateSurveySerializer
        return SurveySerializer


class SurveyQuestionViewSet(ModelViewSet):
    queryset = Option.objects.all()
    serializer_class = OptionSerializer
    print('asdas')
    def get_serializer_context(self):
        return {'customer_id': self.request.user.id}

    def create(self, request, *args, **kwargs):
        print(23142341234)
        serializer = OptionSerializer
        # serializer.is_valid(raise_exception=True)
        instance = self.perform_create(serializer)
        response_data = {'id': instance.id}
        return Response(response_data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        print(23142341234)
        question_data = self.request.data.get('question')
        question_serializer = QuestionSerializer(data=question_data)
        question_serializer.is_valid(raise_exception=True)
        question = question_serializer.save()
        print('a qyest', question)
        return serializer.save(question=question)




class SurveyQuesssstionViewSet(ModelViewSet):
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
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Save the new instance
        self.perform_create(serializer)
        data = {
            "id": serializer.instance.id,
            "data": serializer.data
        }
        
        return Response(data, status=status.HTTP_201_CREATED)




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
