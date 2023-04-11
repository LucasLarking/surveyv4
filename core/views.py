import logging

from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, DestroyModelMixin, UpdateModelMixin

from .models import Customer
from .serializers import CustomerSerializer
from base.permissions import FullDjangoModelPermissions, ViewCustomerHistoryPermission
from .forms import Create_survey_form, Create_question_form
from base.models import Survey

logger = logging.getLogger(__name__)


class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    # permission_classes = [IsAdminUser]
    permission_classes = [FullDjangoModelPermissions]

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated()]

    @action(detail=False, methods=['GET', 'PUT'], permission_classes=[IsAuthenticated])
    def me(self, request):
        customer_obj = Customer.objects.get(user_id=request.user.id)
        if request.method == 'GET':
            serializer = CustomerSerializer(customer_obj)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = CustomerSerializer(customer_obj, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
    
    @action(detail=True, permission_classes=[ViewCustomerHistoryPermission])
    def history(self, request, pk):
        return Response('OK')


class CreateSurveyView(View):

    def get(self, request):

        context = {
            'Create_survey_form': Create_survey_form()
        }
        return render(request, 'core/create_survey.html', context)
    

class CreateQuestionsView(View):
    def get(self, request, pk):
        surveyObj = Survey.objects.get(id=pk)
        context = {
            'Create_question_form': Create_question_form()
        }
        return render(request, 'core/create_question.html', context)

class LoginView(View):
    def get(self, request):

        return render(request, 'core/login.html')