from django.urls import path
from .views import SurveyList, survey_list, survey_detail, question_list, question_detail



urlpatterns = [

   
    path('surveys/', SurveyList.as_view(), name="survey_list"),
    path('surveys/<int:pk>/', survey_detail, name="survey_detail"),
    path('questions/', question_list, name="question_list"),
    path('questions/<int:pk>/', question_detail, name="question_detail"),


]
