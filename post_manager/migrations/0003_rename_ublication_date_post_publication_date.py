# Generated by Django 4.2.16 on 2024-11-01 06:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('post_manager', '0002_remove_post_publication_date_post_ublication_date'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='ublication_date',
            new_name='publication_date',
        ),
    ]
