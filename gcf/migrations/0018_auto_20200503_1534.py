# Generated by Django 3.0.5 on 2020-05-03 15:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gcf', '0017_auto_20200503_1256'),
    ]

    operations = [
        migrations.RenameField(
            model_name='playerinfo',
            old_name='name',
            new_name='firstname',
        ),
        migrations.AddField(
            model_name='playerinfo',
            name='lastname',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
