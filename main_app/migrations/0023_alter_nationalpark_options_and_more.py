# Generated by Django 4.2.3 on 2023-07-17 00:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0022_nationalpark_state'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='nationalpark',
            options={'ordering': ['name']},
        ),
        migrations.RenameField(
            model_name='nationalpark',
            old_name='image_url',
            new_name='img_url',
        ),
    ]
