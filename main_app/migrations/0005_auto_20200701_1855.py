# Generated by Django 3.0.5 on 2020-07-01 18:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0004_auto_20200628_0549'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='visit',
            name='user_id',
        ),
        migrations.AddField(
            model_name='visit',
            name='park',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='main_app.Park'),
            preserve_default=False,
        ),
    ]
