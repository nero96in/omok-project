# Generated by Django 2.2.4 on 2019-08-07 08:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('omok_main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='player1',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='room',
            name='player2',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='room',
            name='winner',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
