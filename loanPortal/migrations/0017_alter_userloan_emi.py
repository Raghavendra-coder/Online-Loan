# Generated by Django 3.2.5 on 2021-07-21 06:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loanPortal', '0016_alter_userloan_tenure'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userloan',
            name='emi',
            field=models.FloatField(null=True),
        ),
    ]
