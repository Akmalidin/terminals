# Generated by Django 5.1.2 on 2024-11-26 18:03

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_alter_terminal_options_terminal_latitude_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='terminal',
            name='get',
        ),
        migrations.RemoveField(
            model_name='terminal',
            name='interval',
        ),
        migrations.AddField(
            model_name='terminal',
            name='rent',
            field=models.DecimalField(decimal_places=2, default=1000, max_digits=10, verbose_name='Аренда'),
        ),
        migrations.CreateModel(
            name='Incassation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_collected', models.DateField(default=django.utils.timezone.now, verbose_name='Дата последней инкассации')),
                ('interval_days', models.PositiveIntegerField(default=30, verbose_name='Интервал дней для инкассации')),
                ('next_collection', models.DateField(blank=True, null=True, verbose_name='Дата следующей инкассации')),
                ('terminal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='incassations', to='core.terminal', verbose_name='Терминал')),
            ],
        ),
    ]
