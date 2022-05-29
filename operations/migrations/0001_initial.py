# Generated by Django 3.2 on 2022-05-28 12:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import operations.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Applicant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(blank=True, max_length=255, null=True)),
                ('last_name', models.CharField(blank=True, max_length=255, null=True)),
                ('middle_name', models.CharField(blank=True, max_length=255, null=True)),
                ('email', models.EmailField(blank=True, max_length=255, null=True, unique=True, verbose_name='email address')),
                ('nationality', models.CharField(blank=True, max_length=100, null=True)),
                ('state', models.CharField(blank=True, max_length=100, null=True)),
                ('lga', models.CharField(blank=True, max_length=100, null=True)),
                ('jamb_reg_no', models.CharField(blank=True, max_length=25, null=True)),
                ('phone', models.CharField(blank=True, max_length=15, null=True)),
                ('dob', models.DateField(blank=True, null=True)),
                ('gender', models.CharField(blank=True, max_length=10, null=True)),
                ('picture', models.ImageField(blank=True, null=True, upload_to=operations.models.applicant_image_location)),
                ('primary_cert', models.FileField(blank=True, null=True, upload_to=operations.models.applicant_primary_cert_location)),
                ('birth_cert', models.FileField(blank=True, null=True, upload_to=operations.models.applicant_birth_cert_location)),
                ('mode_of_entry', models.CharField(blank=True, max_length=10, null=True)),
                ('is_admitted', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_year', models.CharField(blank=True, max_length=10, null=True)),
                ('end_year', models.CharField(blank=True, max_length=10, null=True)),
                ('current_session', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(blank=True, max_length=255, null=True)),
                ('last_name', models.CharField(blank=True, max_length=255, null=True)),
                ('middle_name', models.CharField(blank=True, max_length=255, null=True)),
                ('place_of_birth', models.CharField(blank=True, max_length=255, null=True)),
                ('blood_group', models.CharField(blank=True, max_length=10, null=True)),
                ('gender', models.CharField(blank=True, max_length=10, null=True)),
                ('marital_status', models.CharField(blank=True, max_length=25, null=True)),
                ('religion', models.CharField(blank=True, max_length=100, null=True)),
                ('phone', models.CharField(blank=True, max_length=15, null=True)),
                ('address', models.CharField(blank=True, max_length=255, null=True)),
                ('applicant', models.OneToOneField(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='student', to='operations.applicant')),
                ('user', models.OneToOneField(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='student', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='staff',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(blank=True, max_length=255, null=True)),
                ('last_name', models.CharField(blank=True, max_length=255, null=True)),
                ('middle_name', models.CharField(blank=True, max_length=255, null=True)),
                ('nationality', models.CharField(blank=True, max_length=100, null=True)),
                ('state', models.CharField(blank=True, max_length=100, null=True)),
                ('lga', models.CharField(blank=True, max_length=100, null=True)),
                ('phone', models.CharField(blank=True, max_length=15, null=True)),
                ('dob', models.DateField(blank=True, null=True)),
                ('gender', models.CharField(blank=True, max_length=10, null=True)),
                ('picture', models.ImageField(blank=True, null=True, upload_to=operations.models.applicant_image_location)),
                ('primary_cert', models.FileField(blank=True, null=True, upload_to=operations.models.applicant_primary_cert_location)),
                ('birth_cert', models.FileField(blank=True, null=True, upload_to=operations.models.applicant_birth_cert_location)),
                ('mode_of_entry', models.CharField(blank=True, max_length=10, null=True)),
                ('is_admitted', models.BooleanField(default=False)),
                ('user', models.OneToOneField(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='staff', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='applicant',
            name='session',
            field=models.OneToOneField(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='applicant', to='operations.session'),
        ),
        migrations.AddField(
            model_name='applicant',
            name='user',
            field=models.OneToOneField(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='applicant', to=settings.AUTH_USER_MODEL),
        ),
    ]