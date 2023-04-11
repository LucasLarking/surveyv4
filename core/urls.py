from django.urls import path, include
from django.views.generic import TemplateView
from . import views
from .views import CreateSurveyView, CreateQuestionsView, LoginView
urlpatterns = [

    path('', TemplateView.as_view(template_name="core/index.html")),
    path('create_survey', CreateSurveyView.as_view(), name='create_survey'),
    path('surveys/<str:pk>', CreateQuestionsView.as_view(), name='create_questions'),
    path('login', LoginView.as_view(), name='login'),
]


