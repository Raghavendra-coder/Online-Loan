# Generated by Django 3.2.5 on 2021-07-20 12:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loanPortal', '0011_remove_userloan_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userloan',
            name='tenure',
            field=models.CharField(default='1Year', max_length=20),
        ),
    ]