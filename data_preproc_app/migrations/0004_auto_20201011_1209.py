# Generated by Django 3.0.3 on 2020-10-11 06:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data_preproc_app', '0003_auto_20201011_1208'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userfileencoded',
            name='y_PredData',
            field=models.TextField(blank=True, null=True, verbose_name='Predicted Data'),
        ),
    ]
