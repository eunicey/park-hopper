# Generated by Django 4.2.1 on 2023-06-03 20:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0002_alter_park_year_visited'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='comments',
            field=models.TextField(blank=True, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='park',
            name='highlights',
            field=models.TextField(blank=True, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='park',
            name='year_visited',
            field=models.IntegerField(blank=True, null=True, verbose_name='If visited, what year'),
        ),
    ]
