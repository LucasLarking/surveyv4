from django.urls import path
from .views import SurveyList, SurveyDetail, QuestionList, QuestionDetail



urlpatterns = [

   
    path('surveys/', SurveyList.as_view(), name="survey_list"),
    path('surveys/<int:pk>/', SurveyDetail.as_view(), name="survey_detail"),
    path('questions/', QuestionList.as_view(), name="question_list"),
    path('questions/<int:pk>/', QuestionDetail.as_view(), name="question_detail"),


]
