# Generated by Django 3.0.8 on 2020-07-28 14:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('image_processing', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='height',
            field=models.PositiveIntegerField(default=0, verbose_name='высота'),
        ),
        migrations.AddField(
            model_name='image',
            name='width',
            field=models.PositiveIntegerField(default=0, verbose_name='ширина'),
        ),
    ]
