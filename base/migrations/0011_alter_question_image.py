# Generated by Django 4.2 on 2023-04-10 23:57

import base.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0010_alter_survey_customer_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='base/images', validators=[base.validators.validate_file_size]),
        ),
    ]
