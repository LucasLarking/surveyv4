# Generated by Django 4.2 on 2023-04-10 21:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
        ('base', '0009_alter_question_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='survey',
            name='customer_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.customer'),
        ),
    ]
