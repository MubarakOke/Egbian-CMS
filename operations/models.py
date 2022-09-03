from calendar import calendar
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

def applicant_secondary_cert_location(instance, filename):
    return f"Applicant/{instance.email}/secondary_cert/{filename}"

def applicant_testimonial_location(instance, filename):
    return f"Applicant/{instance.email}/testimonial/{filename}"
# Create your models here.
class Session(models.Model):
    start_year = models.CharField(max_length=10, blank=True, null=True)
    end_year = models.CharField(max_length=10, blank=True, null=True)
    current_session= models.BooleanField(default=True)
    date_created= models.DateTimeField(auto_now_add=True)
    timestamp = models.DateTimeField(auto_now=True)
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['start_year', 'end_year'], name='SessionConstraint')
        ]
    def __str__(self):
        return f"{self.start_year}/{self.end_year}"

class Faculty(models.Model):
    name= models.CharField(max_length=255, blank=False, null=False, unique=True)
    date_created= models.DateTimeField(auto_now_add=True)
    timestamp = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name
        
class Department(models.Model):
    name= models.CharField(max_length=255, blank=False, null=False, unique=True)
    short_name= models.CharField(max_length=255, blank=False, null=False, unique=True)
    faculty= models.ForeignKey(Faculty, blank=True, on_delete= models.CASCADE, related_name="department")
    date_created= models.DateTimeField(auto_now_add=True)
    timestamp = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name

ADMISSION_CHOICES =(
                ("admitted", "admitted"),
                ("rejected", "rejected"),
                ("pending", "pending"),
                )
class Applicant(models.Model):
    user= models.OneToOneField(User, blank=True, on_delete= models.CASCADE, related_name="applicant")
    session= models.ForeignKey(Session, blank=True, null=True, on_delete= models.SET_NULL, related_name="applicant")
    calendar=   models.CharField(max_length=255, blank=True, null=True)
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
    department= models.ForeignKey(Department, blank=True, null=True, on_delete= models.CASCADE, related_name="applicant")
    phone= models.CharField(max_length=15, blank=True, null=True)
    dob= models.DateField(blank=True, null=True)
    gender= models.CharField(max_length=10, blank=True, null=True)
    picture= models.ImageField(upload_to=applicant_image_location, blank=True, null=True)
    primary_cert= models.FileField(upload_to=applicant_primary_cert_location, blank=True, null=True)
    secondary_cert= models.FileField(upload_to=applicant_secondary_cert_location, blank=True, null=True)
    birth_cert= models.FileField(upload_to=applicant_birth_cert_location, blank=True, null=True)
    testimonial= models.FileField(upload_to=applicant_testimonial_location, blank=True, null=True)
    mode_of_entry= models.CharField(max_length=10, blank=True, null=True)
    status= models.CharField(max_length=155, blank=True, null=True, choices=ADMISSION_CHOICES, default="pending")
    next_kin_name= models.CharField(max_length=255, blank=True, null=True)
    next_kin_relationship= models.CharField(max_length=255, blank=True, null=True)
    next_kin_email= models.EmailField(max_length=255, blank=True, null=True)
    next_kin_address= models.CharField(max_length=255, blank=True, null=True)
    next_kin_phone= models.CharField(max_length=255, blank=True, null=True)
    is_admitted = models.BooleanField(default=False)
    date_created= models.DateTimeField(auto_now_add=True)
    timestamp = models.DateTimeField(auto_now=True)

    @property
    def pictureURL(self):
        if self.picture :
            return self.picture.url
        return None

    @property
    def primary_certURL(self):
        if self.primary_cert :
            return self.primary_cert.url
        return None
    
    @property
    def secondary_certURL(self):
        if self.secondary_cert:
            return self.secondary_cert.url
        return None
        
    @property
    def testimonialURL(self):
        if self.testimonial:
            return self.testimonial.url
        return None
    
    @property
    def birth_certURL(self):
        if self.birth_cert :
            return self.birth_cert.url
        return None

    def __str__(self):
        return self.user.username

class Student(models.Model):
    user= models.OneToOneField(User, blank=True, on_delete= models.CASCADE, related_name="student") 
    applicant= models.OneToOneField(Applicant, blank=True, null=True, on_delete= models.SET_NULL, related_name="student")
    calendar= models.CharField(max_length=255, blank=True, null=True)
    session= models.ForeignKey(Session, blank=True, null=True, on_delete= models.SET_NULL, related_name="student")
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
        blank=True, 
        null=True
    )
    first_name= models.CharField(max_length=255, blank=True, null=True)
    last_name= models.CharField(max_length=255, blank=True, null=True)
    middle_name= models.CharField(max_length=255, blank=True, null=True)
    matric_no= models.CharField(max_length=255, blank=True, null=True)
    dob= models.DateField(blank=True, null=True)
    nationality= models.CharField(max_length=100, blank=True, null=True)
    state= models.CharField(max_length=100, blank=True, null=True)
    department= models.ForeignKey(Department, blank=True, null=True, on_delete= models.CASCADE, related_name="student")
    lga= models.CharField(max_length=100, blank=True, null=True)
    jamb_reg_no= models.CharField(max_length=25, blank=True, null=True)
    phone= models.CharField(max_length=15, blank=True, null=True)
    level= models.CharField(max_length=255, blank=True, null=True)
    address= models.CharField(max_length=255, blank=True, null=True)
    blood_group= models.CharField(max_length=10, blank=True, null=True)
    gender= models.CharField(max_length=10, blank=True, null=True)
    marital_status= models.CharField(max_length=25, blank=True, null=True)
    religion= models.CharField(max_length=100, blank=True, null=True)
    phone= models.CharField(max_length=15, blank=True, null=True)
    address= models.CharField(max_length=255, blank=True, null=True)
    picture= models.ImageField(upload_to=applicant_image_location, blank=True, null=True)
    primary_cert= models.FileField(upload_to=applicant_primary_cert_location, blank=True, null=True)
    birth_cert= models.FileField(upload_to=applicant_birth_cert_location, blank=True, null=True)
    secondary_cert= models.FileField(upload_to=applicant_secondary_cert_location, blank=True, null=True)
    testimonial= models.FileField(upload_to=applicant_testimonial_location, blank=True, null=True)
    mode_of_entry= models.CharField(max_length=10, blank=True, null=True)
    status= models.CharField(max_length=155, blank=True, null=True, choices=ADMISSION_CHOICES, default="pending")
    student_type= models.CharField(max_length=255, blank=True, null=True)
    next_kin_name= models.CharField(max_length=255, blank=True, null=True)
    next_kin_relationship= models.CharField(max_length=255, blank=True, null=True)
    next_kin_email= models.EmailField(max_length=255, blank=True, null=True)
    next_kin_address= models.CharField(max_length=255, blank=True, null=True)
    next_kin_phone= models.CharField(max_length=255, blank=True, null=True)
    date_created= models.DateTimeField(auto_now_add=True)
    timestamp = models.DateTimeField(auto_now=True)
    
    @property
    def pictureURL(self):
        if self.picture:
            return self.picture.url
        return None

    @property
    def primary_certURL(self):
        if self.primary_cert:
            return self.primary_cert.url
        return None

    @property
    def secondary_certURL(self):
        if self.secondary_cert:
            return self.secondary_cert.url
        return None

    @property
    def testimonialURL(self):
        if self.testimonial:
            return self.testimonial.url
        return None

    @property
    def birth_certURL(self):
        if self.birth_cert :
            return self.birth_cert.url
        return None

    def __str__(self):
        return self.user.username

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
    date_created= models.DateTimeField(auto_now_add=True)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.last_name.upper()}, {self.first_name} {self.middle_name}"


SEMESTER_CHOICES =(
                ("first", "first"),
                ("second", "second"),
                )
class Course(models.Model):
    course_name= models.CharField(max_length=255, blank=True, null=True)
    course_code= models.CharField(max_length=255, blank=True, null=True)
    level= models.CharField(max_length=255, blank=True, null=True)
    course_unit = models.IntegerField(blank=True,  null=True)
    compulsory= models.BooleanField(default=False)
    prerequsite_for= models.ForeignKey('self', blank=True,  null=True, on_delete= models.SET_NULL, related_name="course",)
    department= models.ForeignKey(Department, blank=True,  null=True, on_delete= models.CASCADE, related_name="course")
    semester= models.CharField(max_length=255, blank=True, null=True, choices=SEMESTER_CHOICES)
    date_created= models.DateTimeField(auto_now_add=True)
    timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        ordering= ('id',)
        constraints = [
            models.UniqueConstraint(fields=['course_name', 'course_code', 'department'], name='CourseConstraint')
        ]

    def __str__(self):
        return self.course_code

class CourseRegistration(models.Model):
    session= models.ForeignKey(Session, blank=True, null=True, on_delete= models.SET_NULL, related_name="courseregistration")
    calendar= models.CharField(max_length=255, blank=True, null=True)
    student= models.ForeignKey(Student, blank=True, on_delete= models.CASCADE, related_name="courseregistration")
    course= models.ForeignKey(Course, blank=True, null=True, on_delete= models.SET_NULL, related_name="courseregistration")
    date_created= models.DateTimeField(auto_now_add=True)
    timestamp = models.DateTimeField(auto_now=True)
    

class CourseRegistrationStatus(models.Model):
    student= models.ForeignKey(Student, blank=True, on_delete= models.CASCADE, related_name="courseregistrationstatus")
    session= models.ForeignKey(Session, blank=True, null=True, on_delete= models.SET_NULL, related_name="courseregistrationstatus")
    status= models.BooleanField(default=False)

class NotificationStudent(models.Model):
    student= models.ForeignKey(Student, blank=True, on_delete= models.CASCADE, related_name="notificationstudent")
    topic= models.CharField(max_length=255, blank=True, null=True)
    date_created= models.DateTimeField(auto_now_add=True)
    timestamp = models.DateTimeField(auto_now=True)

class NotificationStaff(models.Model):
    staff= models.ForeignKey(Staff, blank=True, on_delete= models.CASCADE, related_name="notificationstaff")
    topic= models.CharField(max_length=255, blank=True, null=True)
    date_created= models.DateTimeField(auto_now_add=True)
    timestamp = models.DateTimeField(auto_now=True)

class Role(models.Model):
    name= models.CharField(max_length=255, blank=False, null=False, unique=True)
    staff= models.ManyToManyField(Staff, related_name="role", blank=True)
    date_created= models.DateTimeField(auto_now_add=True)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name}"

GRADE_CHOICES =(
                ("A1", "A1"),
                ("B2", "B2"),
                ("B3", "B3"),
                ("C4", "C4"),
                ("C5", "C5"),
                ("C6", "C6"),
                ("D7", "D7"),
                ("E8", "E8"),
                ("F9", "F9"),
                )
class Result(models.Model):
    session= models.ForeignKey(Session, blank=True, null=True, on_delete= models.SET_NULL, related_name="result")
    calendar= models.CharField(max_length=255, blank=True, null=True)
    course= models.ForeignKey(Course, blank=True, null=True, on_delete=models.SET_NULL, related_name="result")
    grade= models.CharField(max_length=255, blank=True, null=True, choices=GRADE_CHOICES)
    score= models.FloatField(blank=True, null=True)
    student= models.ForeignKey(Student, blank=True, on_delete= models.CASCADE, related_name="result")
    date_created= models.DateTimeField(auto_now_add=True)
    timestamp = models.DateTimeField(auto_now=True)

LEVEL_CHOICES= (
                ("100", "100"),
                ("200", "200"),
                ("300", "300"),
                ("400", "400"),
                ("500", "500"),
                ("600", "600"),
                ("700", "700"),
                ("800", "800"),
               )

class CourseRequirement(models.Model):
    department= models.ForeignKey(Department, blank=True,  null=True, on_delete= models.CASCADE, related_name="courserequirement")
    semester= models.CharField(max_length=255, blank=True, null=True, choices=SEMESTER_CHOICES)
    total_credit= models.IntegerField(blank=True, null=True)
    level= models.CharField(max_length=255, blank=True, null=True, choices=LEVEL_CHOICES)
    date_created= models.DateTimeField(auto_now_add=True)
    timestamp = models.DateTimeField(auto_now=True)
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['department', 'semester', 'level'], name='CourseRequirementConstraint')
        ]

class Payment(models.Model):
    name= models.CharField(max_length=255)
    amount= models.PositiveBigIntegerField()
    ref= models.CharField(max_length=255)
    session= models.ForeignKey(Session, blank=True, null=True, on_delete= models.SET_NULL, related_name="payment")
    calendar= models.CharField(max_length=255, blank=True, null=True)
    student= models.ForeignKey(Student, blank=True, null=True, on_delete= models.SET_NULL, related_name="payment")
    verified= models.BooleanField(default=False)
    timestamp= models.DateTimeField(auto_now=True)
    date_made= models.DateTimeField(auto_now_add=True)

FEE_CHOICES= (
                ("tuition", "tuition"),
                ("acceptance", "acceptance")
               )
class Fee(models.Model):
    name= models.CharField(max_length=255, choices=FEE_CHOICES)
    amount= models.PositiveBigIntegerField()
    session= models.ForeignKey(Session, blank=True, null=True, on_delete= models.SET_NULL, related_name="fee")
    calendar= models.CharField(max_length=255, blank=True, null=True)
    department= models.ForeignKey(Department, blank=True, null=True, on_delete= models.SET_NULL, related_name="fee")
    date_created= models.DateTimeField(auto_now_add=True)
    timestamp = models.DateTimeField(auto_now=True)
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['department', 'calendar', 'amount'], name='FeeConstraint')
        ]











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