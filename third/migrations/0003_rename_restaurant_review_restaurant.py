# Generated by Django 3.2.12 on 2022-03-14 15:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('third', '0002_review'),
    ]

    operations = [
        migrations.RenameField(
            model_name='review',
            old_name='Restaurant',
            new_name='restaurant',
        ),
    ]
