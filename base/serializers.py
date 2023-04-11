from rest_framework import serializers
from .models import Survey, Question, Option
from core.models import Customer
from django.http import HttpResponseRedirect
# from .signals import question_created



class OptionwSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ['option']

    def create(self, validated_data):
        question_id = self.context['question_id']
        return Option.objects.create(
            question_id=question_id,
            **validated_data
        )


class QuestionSerializer(serializers.ModelSerializer):
    option_set = OptionwSerializer(many=True, read_only=True)
    class Meta:
        model = Question
        fields = ['id', 'question', 'survey', 'option_set']
       # read_only_fields = ['survey']

    def create(self, validated_data):
        question_obj = Question(**validated_data)
        question_obj.survey = Survey.objects.get(id=1)
        question_obj.save()
        return question_obj

    def update(self, instance, validated_data):
        instance.question = validated_data.get('question')
        instance.save()
        return instance

    def validate(self, data):
        if len(data['question']) < 2:
            return serializers.ValidationError('Too short')
        return data


class AddQuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Question
        fields = ['question', 'survey', 'image']
        read_only_fields = ['survey']
    
    def validate_survey(self, value):
        print('asdsad')
        if not Survey.objects.get(pk=value).exists():
            raise serializers.ValidationError('No survey with given id')
        return value

    def save(self, **kwargs):
        survey = Survey.objects.get(id=self.context['survey'])
        question = self.validated_data['question']
        # image = self.validated_data['image']

        self.instance = Question.objects.create(
            survey = survey,
            question = question,
            # image = image
        )
        print(self.instance.id, '###id')
        # question_created.send_robust(self.__class__, question=self.instance)
        # return {'question': self.instance.question, 'id': self.instance.id}
        return self.instance


class OptionSerializer(serializers.ModelSerializer):
    question = AddQuestionSerializer()
    print('question', question)

    class Meta:
        model = Option
        fields = ('option', 'question')

    def create(self, validated_data):
        print('creatubng iotuibn')
        question_data = validated_data.pop('option')
        question = Question.objects.create(**question_data)
        validated_data['question'] = question
        return super().create(validated_data)

    def save(self, **kwargs):
        print('question', question)
        survey = Survey.objects.get(id=self.context['survey'])
        question = self.validated_data['question']
        # image = self.validated_data['image']

        self.instance = Question.objects.create(
            survey = survey,
            question = question,
            # image = image
        )
        print(self.instance.id, '###id')
        # question_created.send_robust(self.__class__, question=self.instance)
        # return {'question': self.instance.question, 'id': self.instance.id}
        return self.instance


class EditQuestionSerializer(serializers.ModelSerializer):
    print('asdsaasdasd')
    class Meta:
        model = Question
        fields = ['question']


class SurveySerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    question_set = QuestionSerializer(many=True, read_only=True)
    # question_set = AddQuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Survey
        fields = ['id', 'customer_id', 'survey', 'description', 'question_count', 'question_set']
        read_only_fields = ['customer_id']

    question_count = serializers.IntegerField(read_only=True)

    def validate_description(self, description):
        if description == 'desc':
            raise serializers.ValidationError('Description cannot be desc')
        return description

    def save(self, **kwargs):
        print('###### ')
        print('Validated Data: ', self.validated_data)
        print('Context: ', self.context)
        self.instance = Survey.objects.create(
            survey=self.validated_data['survey'],
            description=self.validated_data['description'],

            customer_id=Customer.objects.get(id=self.context['customer_id'])
        )

        return self.instance
        



class UpdateSurveySerializer(serializers.ModelSerializer):
    class Meta:
        model = Survey
        fields = ['survey', 'description']