from django.forms import ModelForm
from base.models import Question, Option, Survey
from django import forms
from django.forms import formset_factory, BaseFormSet
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _



class Create_survey_form(ModelForm):


    class Meta:
        model = Survey
        fields = ('survey', 'description')
        required = False


class Create_question_form(ModelForm):

    class Meta:
        model = Question
        fields = ('question',)

