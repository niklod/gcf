# Generated by Django 3.0.5 on 2020-04-19 16:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gcf', '0006_player_nickname'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='nickname',
            field=models.CharField(max_length=100),
        ),
    ]