from django.shortcuts import render
from .forms import Create_question_form, Create_option_form, BaseOptionFormset
from django.forms import BaseFormSet, formset_factory

def home(request):
    option_formset = formset_factory(Create_option_form, formset=BaseOptionFormset, extra=2)
    create_option_formset = option_formset()
    if request.method == 'POST':
        print('########################################################')
        print('########################################################')
        print('########################################################')
        create_option_formset = option_formset(request.POST, request.FILES)

        question_form = Create_question_form(request.POST)

        if question_form.is_valid():
            print('Question valid')
        if create_option_formset.is_valid():
            print('option valid')

            for form in create_option_formset:
                print('option', form.cleaned_data)
        else:
            print('not valid')
            print(create_option_formset.errors)
            print(create_option_formset.non_form_errors())

    context = {
        'Create_question_form': Create_question_form(),
        'option_formset': create_option_formset
    }

    return render(request, 'base/home.html', context)
