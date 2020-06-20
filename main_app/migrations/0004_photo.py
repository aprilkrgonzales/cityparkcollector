# Generated by Django 3.0.5 on 2020-06-20 18:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0003_auto_20200619_0405'),
    ]

    operations = [
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(max_length=200)),
                ('park', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.Park')),
            ],
        ),
    ]
