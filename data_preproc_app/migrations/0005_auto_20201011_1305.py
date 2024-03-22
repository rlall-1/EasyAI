# Generated by Django 3.0.3 on 2020-10-11 07:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data_preproc_app', '0004_auto_20201011_1209'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userfileencoded',
            name='x_TestData',
        ),
        migrations.RemoveField(
            model_name='userfileencoded',
            name='x_TrainData',
        ),
        migrations.RemoveField(
            model_name='userfileencoded',
            name='y_PredData',
        ),
        migrations.RemoveField(
            model_name='userfileencoded',
            name='y_TestData',
        ),
        migrations.RemoveField(
            model_name='userfileencoded',
            name='y_TrainData',
        ),
        migrations.AddField(
            model_name='userfileencoded',
            name='model_file_location',
            field=models.FileField(blank=True, upload_to='model_file'),
        ),
    ]