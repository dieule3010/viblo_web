# Generated by Django 5.1.3 on 2024-11-10 15:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0003_alter_comment_parent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='react',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reactions', to='posts.post'),
        ),
    ]