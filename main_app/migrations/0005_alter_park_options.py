# Generated by Django 4.2.1 on 2023-06-03 22:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0004_alter_activity_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='park',
            options={'ordering': ['-year_visited']},
        ),
    ]