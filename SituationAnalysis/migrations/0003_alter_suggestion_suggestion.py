# Generated by Django 4.2.11 on 2024-05-20 03:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SituationAnalysis', '0002_suggestion_delete_apilog'),
    ]

    operations = [
        migrations.AlterField(
            model_name='suggestion',
            name='suggestion',
            field=models.TextField(),
        ),
    ]
