# Generated by Django 4.1 on 2022-10-04 06:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0004_alter_profile_picture"),
    ]

    operations = [
        migrations.DeleteModel(
            name="Profile",
        ),
    ]
