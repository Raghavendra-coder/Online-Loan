# Generated by Django 3.2.3 on 2021-07-20 06:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('loanPortal', '0005_remove_loan_type'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Interest',
        ),
        migrations.DeleteModel(
            name='Loan',
        ),
    ]
