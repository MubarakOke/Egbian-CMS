# Generated by Django 3.2 on 2022-09-21 13:34

from django.db import migrations, models
import operations.models


class Migration(migrations.Migration):

    dependencies = [
        ('operations', '0013_applicant_application_fee_paid'),
    ]

    operations = [
        migrations.AddField(
            model_name='applicant',
            name='result_first',
            field=models.FileField(blank=True, null=True, upload_to=operations.models.applicant_result_first_location),
        ),
        migrations.AddField(
            model_name='applicant',
            name='result_second',
            field=models.FileField(blank=True, null=True, upload_to=operations.models.applicant_result_second_location),
        ),
        migrations.AddField(
            model_name='student',
            name='result_first',
            field=models.FileField(blank=True, null=True, upload_to=operations.models.applicant_result_first_location),
        ),
        migrations.AddField(
            model_name='student',
            name='result_second',
            field=models.FileField(blank=True, null=True, upload_to=operations.models.applicant_result_second_location),
        ),
    ]