# Generated by Django 3.0.3 on 2020-10-25 15:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data_upload_app', '0011_auto_20201023_0827'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userfileinfo',
            name='model_Name',
        ),
        migrations.RemoveField(
            model_name='usermodeldetails',
            name='scatter_digImage',
        ),
        migrations.AddField(
            model_name='usermodeldetails',
            name='generated_model_name',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='usermodeldetails',
            name='scatter_digImage_name',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='usermodeldetails',
            name='url_Prefix',
            field=models.CharField(blank=True, max_length=355),
        ),
        migrations.AlterField(
            model_name='userfileinfo',
            name='file_uploaded_by_user',
            field=models.FileField(upload_to='userfiles', verbose_name='Select file to analyze'),
        ),
    ]
