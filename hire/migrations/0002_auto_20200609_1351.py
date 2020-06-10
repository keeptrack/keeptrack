# Generated by Django 3.0.6 on 2020-06-09 12:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hire', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('email', models.EmailField(max_length=254)),
                ('cid', models.CharField(blank=True, max_length=16, null=True)),
                ('event_from', models.DateField()),
                ('event_to', models.DateField()),
                ('description', models.TextField()),
            ],
        ),
        migrations.RemoveField(
            model_name='hirerequest',
            name='for_csp',
        ),
    ]
