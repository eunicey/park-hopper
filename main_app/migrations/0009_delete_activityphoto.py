# Generated by Django 4.2.1 on 2023-06-04 22:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0008_rename_photo_parkphoto_activityphoto'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ActivityPhoto',
        ),
    ]
