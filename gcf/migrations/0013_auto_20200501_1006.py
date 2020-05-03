# Generated by Django 3.0.5 on 2020-05-01 10:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gcf', '0012_auto_20200501_0957'),
    ]

    operations = [
        migrations.AddField(
            model_name='playerconfig',
            name='crosshair_config',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='gcf.CrosshairConfig'),
        ),
        migrations.AddField(
            model_name='playerconfig',
            name='startup_config',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='gcf.StartUpSettings'),
        ),
        migrations.AddField(
            model_name='playerconfig',
            name='video_config',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='gcf.VideoConfig'),
        ),
    ]