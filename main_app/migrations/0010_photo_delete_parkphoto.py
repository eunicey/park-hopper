# Generated by Django 4.2.1 on 2023-06-04 22:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0009_delete_activityphoto'),
    ]

    operations = [
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(max_length=250)),
                ('activity', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='main_app.activity')),
            ],
        ),
        migrations.DeleteModel(
            name='ParkPhoto',
        ),
    ]
