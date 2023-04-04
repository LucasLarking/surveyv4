from django.urls import path, include

from rest_framework_nested import routers
from .views import SurveyViewSet, SurveyQuestionViewSet, QuestionViewSet, OptionViewSet
from core.views import CustomerViewSet

router = routers.DefaultRouter()
router.register('questions', QuestionViewSet, basename='questions')
router.register('surveys', SurveyViewSet)
router.register('customer', CustomerViewSet)

survey_router = routers.NestedDefaultRouter(router, 'surveys', lookup='survey')
survey_router.register('questions', SurveyQuestionViewSet, basename='survey-question')

question_router = routers.NestedDefaultRouter(router, 'questions', lookup='question')
question_router.register('options', OptionViewSet, basename='question-option')

# urlpatterns = [

#     path('', include(router.urls))
# ]


urlpatterns = router.urls + survey_router.urls + question_router.urls