from django_filters.rest_framework import FilterSet
from .models import Question

class QuestionFilter(FilterSet):
    class Meta:
        model = Question
        fields = {
            'survey': ['exact'],
            'lenght': ['lt', 'gt']
        }