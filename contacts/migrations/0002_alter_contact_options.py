# Generated by Django 4.2.7 on 2024-02-13 21:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='contact',
            options={'ordering': ['fullname']},
        ),
    ]