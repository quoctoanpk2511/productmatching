# Generated by Django 3.1.1 on 2021-02-21 11:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('matcher', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='new_cluster',
            field=models.IntegerField(null=True),
        ),
    ]
