# Generated by Django 4.2.3 on 2023-07-17 00:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0021_nationalpark'),
    ]

    operations = [
        migrations.AddField(
            model_name='nationalpark',
            name='state',
            field=models.CharField(default='NY', max_length=20),
            preserve_default=False,
        ),
    ]
