# Generated by Django 2.0.8 on 2020-04-30 17:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='album_logo',
            field=models.ImageField(upload_to='images/'),
        ),
    ]