# Generated by Django 3.2.13 on 2022-06-02 21:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wiseapp', '0004_boterrors'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='boterrors',
            name='Timestamp',
        ),
    ]
