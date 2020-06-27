# Generated by Django 3.0.5 on 2020-06-27 23:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0009_remove_park_user'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='visit',
            options={'ordering': ['-date']},
        ),
        migrations.RemoveField(
            model_name='visit',
            name='user',
        ),
        migrations.AlterField(
            model_name='visit',
            name='date',
            field=models.DateField(verbose_name='Date of Visit'),
        ),
    ]