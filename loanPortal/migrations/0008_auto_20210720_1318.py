# Generated by Django 3.2.5 on 2021-07-20 07:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loanPortal', '0007_loan_userloan'),
    ]

    operations = [
        migrations.AddField(
            model_name='userloan',
            name='status',
            field=models.CharField(choices=[('N', 'New'), ('R', 'Rejected'), ('A', 'Approved')], default='N', max_length=1),
        ),
        migrations.AddField(
            model_name='userloan',
            name='tenure',
            field=models.DurationField(null=True),
        ),
    ]
