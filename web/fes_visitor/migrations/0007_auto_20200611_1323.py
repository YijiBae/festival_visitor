# Generated by Django 3.0.7 on 2020-06-11 04:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fes_visitor', '0006_results'),
    ]

    operations = [
        migrations.AddField(
            model_name='results',
            name='최고기온',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='results',
            name='최저기온',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='results',
            name='평균기온',
            field=models.FloatField(default=0.0),
        ),
        migrations.AlterField(
            model_name='option',
            name='fes_name',
            field=models.CharField(default='', max_length=100),
        ),
    ]
