from django.forms import ModelForm
from .models import Question, Option
from django import forms
from django.forms import formset_factory, BaseFormSet
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

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
        errors = []

        for form in self.forms:

            if self.can_delete and self._should_delete_form(form):
                continue
            option = form.cleaned_data.get('option')
            if option in options:
                errors.append(ValidationError(_('distinct'), code='error1'))
            if len(option) == 1:
                errors.append(ValidationError(_('too short'), code='error2'))
            options.append(option)

        raise ValidationError(errors)


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