# Generated by Django 3.0.3 on 2020-10-11 07:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data_upload_app', '0003_auto_20201003_2109'),
    ]

    operations = [
        migrations.AddField(
            model_name='userfileinfo',
            name='model_file_location',
            field=models.FileField(blank=True, upload_to='model_file'),
        ),
    ]
