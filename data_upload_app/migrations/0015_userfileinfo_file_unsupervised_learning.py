# Generated by Django 3.1.5 on 2021-05-06 02:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data_upload_app', '0014_auto_20201107_2051'),
    ]

    operations = [
        migrations.AddField(
            model_name='userfileinfo',
            name='file_unsupervised_learning',
            field=models.BooleanField(default=False, verbose_name='Unsupervised learning?'),
        ),
    ]
