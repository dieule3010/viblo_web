# Generated by Django 5.1.3 on 2024-11-10 06:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='tags',
            field=models.CharField(max_length=255),
        ),
    ]
