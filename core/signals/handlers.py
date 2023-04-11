from django.dispatch import receiver

from base.signals import question_created


@receiver(question_created)
def on_question_created(sender, **kwargs):
    print(kwargs['question'])