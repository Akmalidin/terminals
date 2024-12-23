# Generated by Django 5.1.2 on 2024-10-25 14:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_remove_terminal_collection_interval_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='terminal',
            options={},
        ),
        migrations.AddField(
            model_name='terminal',
            name='latitude',
            field=models.DecimalField(decimal_places=6, default=1, max_digits=9, verbose_name='Широта'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='terminal',
            name='longitude',
            field=models.DecimalField(decimal_places=6, default=1, max_digits=9, verbose_name='Долгота'),
            preserve_default=False,
        ),
    ]
