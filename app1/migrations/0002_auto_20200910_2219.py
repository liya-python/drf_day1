# Generated by Django 2.0.6 on 2020-09-10 14:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='gender',
            field=models.IntegerField(choices=[(1, 'female'), (2, 'other'), (0, 'male')], default=0),
        ),
    ]
