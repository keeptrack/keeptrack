# Generated by Django 3.0.6 on 2020-06-09 12:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hire', '0002_auto_20200609_1351'),
    ]

    operations = [
        migrations.AddField(
            model_name='hirerequest',
            name='for_csp',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
