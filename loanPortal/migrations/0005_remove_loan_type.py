# Generated by Django 3.2.3 on 2021-07-20 05:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('loanPortal', '0004_interest'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='loan',
            name='type',
        ),
    ]
