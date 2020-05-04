# Generated by Django 3.0.5 on 2020-05-04 18:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gcf', '0019_auto_20200503_2001'),
    ]

    operations = [
        migrations.CreateModel(
            name='PlayerStats',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.FloatField(null=True)),
                ('headshots_percent', models.FloatField(null=True)),
                ('total_kills', models.IntegerField(null=True)),
                ('total_deaths', models.IntegerField(null=True)),
                ('rounds_played', models.IntegerField(null=True)),
                ('damage_per_round', models.FloatField(null=True)),
                ('grenade_damage_per_round', models.FloatField(null=True)),
                ('assists_per_round', models.FloatField(null=True)),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gcf.Game')),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gcf.Player')),
            ],
        ),
    ]
