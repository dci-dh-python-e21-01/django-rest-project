# Generated by Django 4.0.3 on 2022-03-09 09:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dog',
            name='is_friendly',
            field=models.BooleanField(),
        ),
    ]
