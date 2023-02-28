from django.forms import ModelForm
from .models import Question, Option
from django import forms
from django.forms import formset_factory, BaseFormSet
from django.core.exceptions import ValidationError


class Create_question_form(ModelForm):

    question = forms.CharField(
        label='Question',
        widget=forms.TextInput(attrs={
            'value': 'my question',
        })

    )

    class Meta:
        model = Question
        fields = ('question',)
        required = False


class BaseOptionFormset(BaseFormSet):
    def clean(self):
        if any(self.errors):
            return
        options = []
        for form in self.forms:
            if self.can_delete and self._should_delete_form(form):
                continue
            option = form.cleaned_data.get('option')
            if option in options:
                raise ValidationError('disitinct')
            if len(option) == 1:
                raise ValidationError('TO SHORT')
            options.append(option)


class Create_option_form(ModelForm):

    option = forms.CharField(
        label='option',
        widget=forms.TextInput(attrs={
            'value': 'a',
        })

    )

    class Meta:
        model = Option
        fields = ('option', )
        required = False


Create_option_formset = formset_factory(
    Create_option_form, formset=BaseOptionFormset, extra=2)
