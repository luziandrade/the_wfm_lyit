# Generated by Django 4.0.4 on 2022-05-21 13:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resource',
            name='username',
            field=models.CharField(default='', max_length=254),
        ),
    ]
