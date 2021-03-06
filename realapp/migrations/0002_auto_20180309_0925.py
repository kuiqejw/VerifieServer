# Generated by Django 2.0.2 on 2018-03-09 01:25

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('realapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='myuser',
            name='photo1',
            field=models.FileField(null=True, upload_to='userimage'),
        ),
        migrations.AddField(
            model_name='myuser',
            name='photo2',
            field=models.FileField(null=True, upload_to='userimage'),
        ),
        migrations.AddField(
            model_name='myuser',
            name='photo3',
            field=models.FileField(null=True, upload_to='userimage'),
        ),
        migrations.AlterField(
            model_name='myuser',
            name='create_date',
            field=models.DateTimeField(default=datetime.datetime(2018, 3, 9, 1, 25, 53, 335774, tzinfo=utc)),
        ),
    ]
