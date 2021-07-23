# Generated by Django 3.2.3 on 2021-07-20 05:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loanPortal', '0003_auto_20210720_0959'),
    ]

    operations = [
        migrations.CreateModel(
            name='Interest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('H', 'Home'), ('C', 'Car'), ('E', 'Education')], max_length=1)),
                ('interest', models.FloatField()),
            ],
        ),
    ]