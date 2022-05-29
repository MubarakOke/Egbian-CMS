from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User= get_user_model()


def applicant_primary_cert_location(instance, filename):
    return f"Applicant/{instance.user.email}/primary_cert/{filename}"

def applicant_birth_cert_location(instance, filename):
    return f"Applicant/{instance.user.email}/birth_cert/{filename}"

def applicant_image_location(instance, filename):
    return f"Applicant/{instance.email}/passport/{filename}"
# Create your models here.
class Session(models.Model):
    start_year = models.CharField(max_length=10, blank=True, null=True)
    end_year = models.CharField(max_length=10, blank=True, null=True)
    current_session= models.BooleanField(default=True)

class Applicant(models.Model):
    user= models.OneToOneField(User, blank=True, on_delete= models.CASCADE, related_name="applicant")
    session= models.ForeignKey(Session, blank=True, on_delete= models.CASCADE, related_name="applicant")
    first_name= models.CharField(max_length=255, blank=True, null=True)
    last_name= models.CharField(max_length=255, blank=True, null=True)
    middle_name= models.CharField(max_length=255, blank=True, null=True) 
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
        blank=True, 
        null=True
    )
    nationality= models.CharField(max_length=100, blank=True, null=True)
    state= models.CharField(max_length=100, blank=True, null=True)
    lga= models.CharField(max_length=100, blank=True, null=True)
    jamb_reg_no= models.CharField(max_length=25, blank=True, null=True)
    phone= models.CharField(max_length=15, blank=True, null=True)
    dob= models.DateField(blank=True, null=True)
    gender= models.CharField(max_length=10, blank=True, null=True)
    picture= models.ImageField(upload_to=applicant_image_location, blank=True, null=True)
    primary_cert= models.FileField(upload_to=applicant_primary_cert_location, blank=True, null=True)
    birth_cert= models.FileField(upload_to=applicant_birth_cert_location, blank=True, null=True)
    mode_of_entry= models.CharField(max_length=10, blank=True, null=True)
    is_admitted = models.BooleanField(default=False)

class Student(models.Model):
    user= models.OneToOneField(User, blank=True, on_delete= models.CASCADE, related_name="student") 
    applicant= models.OneToOneField(Applicant, blank=True, on_delete= models.CASCADE, related_name="student")
    first_name= models.CharField(max_length=255, blank=True, null=True)
    last_name= models.CharField(max_length=255, blank=True, null=True)
    middle_name= models.CharField(max_length=255, blank=True, null=True) 
    place_of_birth= models.CharField(max_length=255, blank=True, null=True)
    blood_group= models.CharField(max_length=10, blank=True, null=True)
    gender= models.CharField(max_length=10, blank=True, null=True)
    marital_status= models.CharField(max_length=25, blank=True, null=True)
    religion= models.CharField(max_length=100, blank=True, null=True)
    phone= models.CharField(max_length=15, blank=True, null=True)
    address= models.CharField(max_length=255, blank=True, null=True)
    
class staff(models.Model):
    user= models.OneToOneField(User, blank=True, on_delete= models.CASCADE, related_name="staff") 
    first_name= models.CharField(max_length=255, blank=True, null=True)
    last_name= models.CharField(max_length=255, blank=True, null=True)
    middle_name= models.CharField(max_length=255, blank=True, null=True) 
    nationality= models.CharField(max_length=100, blank=True, null=True)
    state= models.CharField(max_length=100, blank=True, null=True)
    lga= models.CharField(max_length=100, blank=True, null=True)
    phone= models.CharField(max_length=15, blank=True, null=True)
    dob= models.DateField(blank=True, null=True)
    gender= models.CharField(max_length=10, blank=True, null=True)
    picture= models.ImageField(upload_to=applicant_image_location, blank=True, null=True)
    primary_cert= models.FileField(upload_to=applicant_primary_cert_location, blank=True, null=True)
    birth_cert= models.FileField(upload_to=applicant_birth_cert_location, blank=True, null=True)
    mode_of_entry= models.CharField(max_length=10, blank=True, null=True)
    is_admitted = models.BooleanField(default=False)























# class Student(models.Model):
#     user= models.OneToOneField(User, blank=True, on_delete= models.CASCADE, related_name="admin") 
#     first_name= models.CharField(max_length=255, blank=True, null=True)
#     last_name= models.CharField(max_length=255, blank=True, null=True)
#     middle_name= models.CharField(max_length=255, blank=True, null=True) 
#     email = models.EmailField(
#         verbose_name='email address',
#         max_length=255,
#         unique=True,
#         blank=True, 
#         null=True
#     )
#     nationality= models.CharField(max_length=100, blank=True, null=True)
#     state= models.CharField(max_length=100, blank=True, null=True)
#     lga= models.CharField(max_length=100, blank=True, null=True)
#     jamb_reg_no= models.CharField(max_length=25, blank=True, null=True)
#     phone= models.CharField(max_length=15, blank=True, null=True)
#     dob= models.DateField(blank=True, null=True)
#     gender= models.CharField(max_length=10, blank=True, null=True)
#     picture= models.ImageField(upload_to=applicant_image_location, blank=True, null=True)
#     primary_cert= models.FileField(upload_to=applicant_primary_cert_location, blank=True, null=True)
#     birth_cert= models.FileField(upload_to=applicant_birth_cert_location, blank=True, null=True)
#     mode_of_entry= models.CharField(max_length=10, blank=True, null=True)
#     is_admitted = models.BooleanField(default=True)