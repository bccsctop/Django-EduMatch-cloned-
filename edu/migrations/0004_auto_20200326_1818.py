# Generated by Django 3.0.2 on 2020-03-26 18:18

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('edu', '0003_review_rate'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tutor',
            name='isMatched',
        ),
        migrations.AddField(
            model_name='review',
            name='date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]