from django.db import models
from django.urls import reverse


class Survey(models.Model):
    survey = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)

    def __str__(self) -> str:
        return self.survey

class Question(models.Model):
    question = models.CharField(max_length=200)
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, null=True, blank=True)

    def get_absolute_url(self):
        return reverse('question-detail', kwargs={'pk': self.pk})

    def __str__(self) -> str:
        return self.question


class Option(models.Model):
    option = models.CharField(max_length=200)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)


