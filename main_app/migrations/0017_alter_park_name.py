# Generated by Django 4.2.3 on 2023-07-12 21:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0016_alter_park_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='park',
            name='name',
            field=models.CharField(choices=[('acad', 'Acadia'), ('zi', 'Zion')]),
        ),
    ]
