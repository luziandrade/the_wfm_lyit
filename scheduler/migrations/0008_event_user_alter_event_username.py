# Generated by Django 4.0.4 on 2022-05-22 15:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_resource_username'),
        ('scheduler', '0007_alter_addresource_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='user',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='event',
            name='username',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.resource'),
        ),
    ]
