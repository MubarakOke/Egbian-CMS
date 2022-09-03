# Generated by Django 3.2 on 2022-09-03 11:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operations', '0007_alter_fee_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='student',
            old_name='next_kin_fullname',
            new_name='next_kin_name',
        ),
        migrations.AddField(
            model_name='applicant',
            name='next_kin_address',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='applicant',
            name='next_kin_email',
            field=models.EmailField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='applicant',
            name='next_kin_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='applicant',
            name='next_kin_phone',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='applicant',
            name='next_kin_relationship',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='student',
            name='next_kin_email',
            field=models.EmailField(blank=True, max_length=255, null=True),
        ),
    ]
