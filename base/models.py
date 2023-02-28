from django.db import models


class Question(models.Model):
    question = models.CharField(max_length=200)


class Option(models.Model):
    option = models.CharField(max_length=200)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
