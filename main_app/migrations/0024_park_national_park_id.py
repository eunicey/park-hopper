# Generated by Django 4.2.3 on 2023-07-17 01:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0023_alter_nationalpark_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='park',
            name='national_park_id',
            field=models.ForeignKey(default=999, on_delete=django.db.models.deletion.CASCADE, to='main_app.nationalpark'),
            preserve_default=False,
        ),
    ]
