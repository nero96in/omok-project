# Generated by Django 2.2.4 on 2019-08-09 13:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_auto_20190809_2254'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='nickname',
            field=models.CharField(max_length=30, null=True, unique=True),
        ),
    ]
