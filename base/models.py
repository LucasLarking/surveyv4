from django.db import models
from django.urls import reverse
from uuid import uuid4
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from core.models import Customer
def validate_even(value):
    if len(value) < 2:
        raise ValidationError(
            _('%(value)s is too short'),
            params={'value': value},
        )

    if value == 'questino':
        raise ValidationError(
            _('Cannot name question question'),
            params={'value': value},
        )


class Survey(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    survey = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.survey
    
    class Meta:
        permissions = [
            ('freeze_survey', 'Can freeze a survey')
        ]


class Question(models.Model):

    question = models.CharField(max_length=255, validators=[validate_even])
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, null=True, blank=True)
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True)

    def get_absolute_url(self):
        return reverse('question-detail', kwargs={'pk': self.pk})

    def __str__(self) -> str:
        return self.question


class Option(models.Model):

    option = models.CharField(max_length=255)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.option

