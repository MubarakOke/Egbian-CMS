from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User= get_user_model()


def applicant_primary_cert_location(instance, filename):
    return f"Applicant/{instance.email}/primary_cert/{filename}"

def applicant_birth_cert_location(instance, filename):
    return f"Applicant/{instance.email}/birth_cert/{filename}"

def applicant_image_location(instance, filename):
    return f"Applicant/{instance.email}/passport/{filename}"
# Create your models here.
class Session(models.Model):
    start_year = models.CharField(max_length=10, blank=True, null=True)
    end_year = models.CharField(max_length=10, blank=True, null=True)
    current_session= models.BooleanField(default=True)

class Faculty(models.Model):
    name= models.CharField(max_length=255, blank=False, null=False, unique=True)

class Department(models.Model):
    name= models.CharField(max_length=255, blank=False, null=False, unique=True)
    short_name= models.CharField(max_length=255, blank=False, null=False, unique=True)
    faculty= models.ForeignKey(Faculty, blank=True, on_delete= models.CASCADE, related_name="department")


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
    level= models.CharField(max_length=255, blank=True, null=True)
    place_of_birth= models.CharField(max_length=255, blank=True, null=True)
    blood_group= models.CharField(max_length=10, blank=True, null=True)
    gender= models.CharField(max_length=10, blank=True, null=True)
    marital_status= models.CharField(max_length=25, blank=True, null=True)
    religion= models.CharField(max_length=100, blank=True, null=True)
    phone= models.CharField(max_length=15, blank=True, null=True)
    address= models.CharField(max_length=255, blank=True, null=True)
    student_type= models.CharField(max_length=255, blank=True, null=True)
    
class Staff(models.Model):
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
    department= models.ForeignKey(Department, blank=True, on_delete= models.CASCADE, related_name="staff")
    position= models.CharField(max_length=15, blank=True, null=True)
    staff_type= models.CharField(max_length=255, blank=True, null=True)


class Course(models.Model):
    course_name= models.CharField(max_length=255, blank=True, null=True)
    course_id= models.CharField(max_length=255, blank=True, null=True)
    level= models.CharField(max_length=255, blank=True, null=True)
    staff= models.ManyToManyField(Staff)
    student= models.ManyToManyField(Student)
    compulsory= models.BooleanField(default=False)
    prerequsite_for= models.ForeignKey('self', blank=True, on_delete= models.CASCADE, related_name="course")
    department= models.ForeignKey(Department, blank=True, on_delete= models.CASCADE, related_name="course")
    semester= models.CharField(max_length=255, blank=True, null=True)

class CourseRegistration(models.Model):
    session= models.ForeignKey(Session, blank=True, on_delete= models.CASCADE, related_name="courseregistration")
    student= models.ForeignKey(Student, blank=True, on_delete= models.CASCADE, related_name="courseregistration")
    course= models.ForeignKey(Course, blank=True, on_delete= models.CASCADE, related_name="courseregistration")

class NotificationStudent(models.Model):
    student= models.ForeignKey(Student, blank=True, on_delete= models.CASCADE, related_name="notification")
    course= models.ForeignKey(Course, blank=True, on_delete= models.CASCADE, related_name="notification")

class Role(models.Model):
    name= models.CharField(max_length=255, blank=False, null=False, unique=True)
    staff= models.ManyToManyField(Staff, related_name="role", blank=True)














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