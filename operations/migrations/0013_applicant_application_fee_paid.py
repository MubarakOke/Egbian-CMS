# Generated by Django 3.2 on 2022-09-04 02:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operations', '0012_staff_picture'),
    ]

    operations = [
        migrations.AddField(
            model_name='applicant',
            name='application_fee_paid',
            field=models.BooleanField(default=False),
        ),
    ]