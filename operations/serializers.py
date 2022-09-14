from functools import reduce
from rest_framework import serializers
from django.db.utils import IntegrityError
from accounts.serializers import UserSerializer
from operations.models import Applicant, Session, Staff, Role, Department, Faculty, Course, CourseRegistration, Result, Student, CourseRequirement, CourseRegistrationStatus, Payment
from django.db.utils import IntegrityError
from django.contrib.auth import get_user_model
from operations.utils import EmailThread
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q


User = get_user_model()

class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model= Session
        fields= [
                'id',
                'start_year',
                'end_year',
                'current_session'
                ]

    def validate(self, attrs):
        start_year= attrs.get('start_year')
        end_year= attrs.get('end_year') 
        if start_year > end_year:
            raise serializers.ValidationError("start year cannot be higher than end year")
        return attrs
    
    def create(self, validated_data):
        session_prev_obj= None
        try:
            session_prev_obj= Session.objects.latest('id')
            print("inside try")
        except ObjectDoesNotExist:
            print("inside except")
            pass
        try:
            session_obj= Session.objects.create(
                                            start_year= validated_data.get('start_year'),
                                            end_year= validated_data.get('end_year')
                                            )
            if session_prev_obj:
                session_prev_obj.current_session= False
                session_prev_obj.save()
        except IntegrityError:
            raise serializers.ValidationError({"detail":"session with same start year and end year already exists"})
        session_obj.save()
        return session_obj

class FacultyCreateListSerializer(serializers.ModelSerializer):
    class Meta:
        model= Faculty
        fields= [ 
                    'id',
                    'name'
                ]
                
    def validate(self, attrs):
        if attrs.get('name'):
            attrs['name']= attrs.get('name').title()
        return attrs

    def create(self, validated_data):
        try:
            faculty_obj= Faculty.objects.create(name=validated_data.get('name').lower())
        except IntegrityError:
            raise serializers.ValidationError("faculty with this name already exits")
        return faculty_obj

    def update(self, instance, validated_data):
        instance.name= validated_data.get('name', instance.name)
        instance.save()
        return instance


class DepartmentCreateListSerializer(serializers.ModelSerializer):
    faculty= FacultyCreateListSerializer(read_only=True)
    faculty_id= serializers.SlugRelatedField(slug_field="id", queryset=Faculty.objects.all(), required=False, write_only=True)
    class Meta:
        model= Department
        fields= [ 
                    'id',
                    'name',
                    'short_name',
                    'faculty',
                    'faculty_id'
                ]
    def validate(self, attrs):
        if attrs.get('name'):
            attrs['name']= attrs.get('name').title()
        if attrs.get('short_name'):
            attrs['short_name']= attrs.get('short_name').upper()
        return attrs

    def create(self, validated_data):
        try:
            department_obj= Department.objects.create(name=validated_data.get('name'),
                                                      short_name=validated_data.get('short_name'),
                                                      faculty=validated_data.get('faculty_id'))
        except IntegrityError:
            raise serializers.ValidationError("Department with this info already exits")
        return department_obj

class DepartmentUpdateSerializer(serializers.ModelSerializer):
    faculty= FacultyCreateListSerializer(read_only=True)
    faculty_id= serializers.SlugRelatedField(slug_field="id", queryset=Faculty.objects.all(), required=False, write_only=True)
    class Meta:
        model= Department
        fields= [ 
                    'id',
                    'name',
                    'short_name',
                    'faculty',
                    'faculty_id'
                ]

    def validate(self, attrs):
        if attrs.get('name'):
            attrs['name']= attrs.get('name').title()
        if attrs.get('short_name'):
            attrs['short_name']= attrs.get('short_name').upper()
        return attrs

    def update(self, instance, validated_data):
        try:
            instance.name= validated_data.get('name', instance.name)
            instance.short_name= validated_data.get('short_name', instance.short_name)
            instance.faculty= validated_data.get('faculty_id', instance.faculty)
            instance.save()
        except IntegrityError:
            raise serializers.ValidationError("Department with this info already exits")
        return instance

class ApplicantSerializer(serializers.ModelSerializer):
    user= UserSerializer(read_only=True)
    department= DepartmentCreateListSerializer(read_only=True)
    password= serializers.CharField(write_only=True, required=True)
    class Meta:
        model= Applicant
        fields= [
                'id',
                'user',
                'calendar',
                'email',
                'password',
                'first_name', 
                'last_name',
                'middle_name',
                'phone',
                'nationality',
                'state',
                'lga',
                'jamb_reg_no',
                'dob',
                'department',
                'gender',
                'mode_of_entry',
                'status',
                'is_admitted',
                'picture',
                'primary_cert',
                'secondary_cert',
                'testimonial',
                'birth_cert',
                'next_kin_name',
                'next_kin_relationship',
                'next_kin_email',
                'next_kin_address',
                'next_kin_phone',
                'application_fee_paid'
                ]
    
    def validate_email(self, value):
        email= value.lower()
        if Applicant.objects.filter(email=email).exists():
            raise serializers.ValidationError(["Email already exists"])
        return email

    def create(self, validated_data): 
        try:
            session_obj= Session.objects.get(current_session=True)
            calendar= f"{session_obj.start_year}/{session_obj.end_year}"
        except:
            raise serializers.ValidationError({"details":"Session not set"}) 
        applicant_id= int(str(session_obj.start_year) + "0000000") 
        user_obj= User.objects.create(
                                    user_type= "applicant"
                                    )
        applicant_id= applicant_id + user_obj.id
        username= f"egb{str(applicant_id)}"
        user_obj.username= username
        user_obj.set_password(validated_data.pop('password', None))

        applicant_obj = Applicant.objects.create(user=user_obj, session= session_obj, calendar=calendar, email= validated_data.get('email'), phone=validated_data.get('phone') )        
        # Constructing email parameters
        try:
            subject= 'Login details to Egbian College of Health'
            message= f'Dear Applicant, \nWe are glad to have you on, Use the ID below and your password to access the applicant portal\n \n \nAccout ID: {applicant_obj.user.username} \n \n \nPlease do not reply to this email. This email is not monitored'
            from_email= settings.EMAIL_HOST_USER
            recipient_list= [applicant_obj.email]
            fail_silently=False
             # Sending email on a new thread
            send_mail(subject, message, from_email, recipient_list, fail_silently)
            user_obj.save()
            applicant_obj.save()
        except:
            user_obj.delete()
            raise serializers.ValidationError({"details":"email not sent"})
        return applicant_obj

class ApplicantUpdateSerializer(serializers.ModelSerializer):
    user= UserSerializer(read_only=True)
    department= DepartmentCreateListSerializer(read_only=True)
    department_id= serializers.SlugRelatedField(slug_field="id", queryset=Department.objects.all(), required=False, write_only=True)
    class Meta:
        model= Applicant
        fields= [
                'id',
                'user',
                'calendar',
                'email',
                'first_name', 
                'last_name',
                'middle_name',
                'phone',
                'nationality',
                'state',
                'lga',
                'jamb_reg_no',
                'dob',
                'department',
                'department_id',
                'gender',
                'mode_of_entry',
                'status',
                'is_admitted',
                'picture',
                'primary_cert',
                'birth_cert',
                'secondary_cert',
                'testimonial',
                'next_kin_name',
                'next_kin_relationship',
                'next_kin_email',
                'next_kin_address',
                'next_kin_phone',
                'application_fee_paid'
                ]

    def validate(self, attrs):
        if attrs.get('first_name'):
            attrs['first_name']= attrs.get('first_name').title()
        if attrs.get('last_name'):
            attrs['last_name']= attrs.get('last_name').title()
        if attrs.get('middle_name'):
            attrs['middle_name']= attrs.get('middle_name').title()
        if attrs.get('nationality'):
            attrs['nationality']= attrs.get('nationality').title()
        if attrs.get('state'):
            attrs['state']= attrs.get('state').title()
        if attrs.get('lga'):
            attrs['lga']= attrs.get('lga').title()
        if attrs.get('mode_of_entry'):
            attrs['mode_of_entry']= attrs.get('mode_of_entry').lower()
        if attrs.get('jamb_reg_no'):
            attrs['jamb_reg_no']= attrs.get('jamb_reg_no').upper()
        return attrs

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name= validated_data.get('last_name', instance.last_name)
        instance.middle_name= validated_data.get('middle_name', instance.middle_name)
        instance.phone= validated_data.get('phone', instance.phone)
        instance.nationality= validated_data.get('nationality', instance.nationality)
        instance.state= validated_data.get('state', instance.state)
        instance.lga= validated_data.get('lga', instance.lga)
        instance.jamb_reg_no= validated_data.get('jamb_reg_no', instance.jamb_reg_no)
        instance.dob= validated_data.get('dob', instance.dob)
        instance.gender= validated_data.get('gender', instance.gender)
        instance.picture= validated_data.get('picture', instance.picture)
        instance.primary_cert= validated_data.get('primary_cert', instance.primary_cert)
        instance.birth_cert= validated_data.get('birth_cert', instance.birth_cert)
        instance.secondary_cert= validated_data.get('secondary_cert', instance.secondary_cert)
        instance.testimonial= validated_data.get('testimonial', instance.testimonial)
        instance.mode_of_entry= validated_data.get('mode_of_entry', instance.mode_of_entry)
        instance.department= validated_data.get('department_id', instance.department)
        instance.next_kin_name= validated_data.get('next_kin_name', instance.next_kin_name)
        instance.next_kin_relationship= validated_data.get('next_kin_relationship', instance.next_kin_relationship)
        instance.next_kin_email= validated_data.get('next_kin_email', instance.next_kin_email)
        instance.next_kin_address= validated_data.get('next_kin_address', instance.next_kin_address)
        instance.next_kin_phone= validated_data.get('next_kin_phone', instance.next_kin_phone)
        instance.application_fee_paid= validated_data.get('application_fee_paid', instance.application_fee_paid)
        instance.save()
        return instance

class StaffCreateListSerializer(serializers.ModelSerializer):
    user= UserSerializer(read_only=True)
    password= serializers.CharField(write_only=True, required=True)
    department= DepartmentCreateListSerializer(read_only=True)
    department_id= serializers.SlugRelatedField(slug_field="id", queryset=Department.objects.all(), required=False, write_only=True)
    class Meta:
        model= Staff
        fields= [
                    'id',
                    'user',
                    'first_name',
                    'last_name',
                    'middle_name',
                    'email',
                    'nationality',
                    'state',
                    'lga',
                    'phone',
                    'dob',
                    'gender',
                    'department',
                    'department_id',
                    'staff_type',
                    'picture',
                    'password'
                ]

    def validate(self, attrs):
        if attrs.get('first_name'):
            attrs['first_name']= attrs.get('first_name').title()
        if attrs.get('last_name'):
            attrs['last_name']= attrs.get('last_name').title()
        if attrs.get('middle_name'):
            attrs['middle_name']= attrs.get('middle_name').title()
        if attrs.get('nationality'):
            attrs['nationality']= attrs.get('nationality').title()
        if attrs.get('state'):
            attrs['state']= attrs.get('state').title()
        if attrs.get('lga'):
            attrs['lga']= attrs.get('lga').title()
        if attrs.get('staff_type'):
            attrs['staff_type']= attrs.get('staff_type').lower()
        return attrs

    def validate_email(self, value):
        email= value.lower()
        if Applicant.objects.filter(email=email).exists():
            raise serializers.ValidationError(["Email already exists"])
        return email

    def create(self, validated_data): 
        try:
            session_obj= Session.objects.get(current_session=True)
        except:
            raise serializers.ValidationError({"details":"Session not set"}) 
        staff_id= int(str(session_obj.start_year) + "0000000")
        user_obj= User.objects.create(
                                    user_type= "staff"
                                    )
 
        staff_id= f"EGB{staff_id + user_obj.id}ff"
        print("staff", staff_id)
        user_obj.username= staff_id
        user_obj.set_password(validated_data.pop('password'))

        staff_obj = Staff.objects.create(user=user_obj, 
                                        email= validated_data.get('email'),
                                        first_name= validated_data.get('first_name'),
                                        last_name= validated_data.get('last_name'),
                                        middle_name= validated_data.get('middle_name'),
                                        nationality= validated_data.get('nationality'),
                                        state= validated_data.get('state'),
                                        lga= validated_data.get('lga'),
                                        phone= validated_data.get('phone'),
                                        dob= validated_data.get('dob'),
                                        gender= validated_data.get('gender'),
                                        department= validated_data.get('department_id'),
                                        staff_type= validated_data.get('staff_type').lower()
                                        )
        try:
            subject= 'Login details to Egbian College of Health'
            message= f'Dear Staff, \nUse the ID below and your password to access the applicant portal\n \n \nAccout ID: {staff_obj.user.username} \n \n \nPlease do not reply to this email. This email is not monitored'
            from_email= settings.EMAIL_HOST_USER
            recipient_list= [staff_obj.email]
            fail_silently=False
            user_obj.save()
            staff_obj.save()
             # Sending email on a new thread
            send_mail(subject, message, from_email, recipient_list, fail_silently)
        except:
            user_obj.delete()
            raise serializers.ValidationError({"details":"email not sent"})
        return staff_obj

class StaffUpdateSerializer(serializers.ModelSerializer):
    user= UserSerializer(read_only=True)
    department= DepartmentCreateListSerializer(read_only=True)
    department_id= serializers.SlugRelatedField(slug_field="id", queryset=Department.objects.all(), required=False, write_only=True)
    class Meta:
        model= Staff
        fields= [
                    'id',
                    'user',
                    'first_name',
                    'last_name',
                    'middle_name',
                    'email',
                    'nationality',
                    'state',
                    'lga',
                    'phone',
                    'dob',
                    'gender',
                    'department',
                    'department_id',
                    'staff_type',
                    'picture',
                ]

    def validate(self, attrs):
        if attrs.get('first_name'):
            attrs['first_name']= attrs.get('first_name').title()
        if attrs.get('last_name'):
            attrs['last_name']= attrs.get('last_name').title()
        if attrs.get('middle_name'):
            attrs['middle_name']= attrs.get('middle_name').title()
        if attrs.get('nationality'):
            attrs['nationality']= attrs.get('nationality').title()
        if attrs.get('state'):
            attrs['state']= attrs.get('state').title()
        if attrs.get('lga'):
            attrs['lga']= attrs.get('lga').title()
        if attrs.get('staff_type'):
            attrs['staff_type']= attrs.get('staff_type').lower()
        return attrs
    
    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name= validated_data.get('last_name', instance.last_name)
        instance.middle_name= validated_data.get('middle_name', instance.middle_name)
        instance.phone= validated_data.get('phone', instance.phone)
        instance.nationality= validated_data.get('nationality', instance.nationality)
        instance.state= validated_data.get('state', instance.state)
        instance.lga= validated_data.get('lga', instance.lga)
        instance.dob= validated_data.get('dob', instance.dob)
        instance.gender= validated_data.get('gender', instance.gender)
        instance.picture= validated_data.get('picture', instance.picture)
        instance.staff_type= validated_data.get('staff_type', instance.staff_type)
        instance.department= validated_data.get('department_id', instance.department)
        instance.save()
        return instance

class RoleCreateListSerializer(serializers.ModelSerializer):
    staff= StaffUpdateSerializer(read_only=True)
    class Meta:
        model= Role
        fields= [ 
                'name',
                'staff'
                ]
    def create(self, validated_data):
        try:
            role_obj= Role.objects.create(name=validated_data.get('name').lower())
        except IntegrityError:
            raise serializers.ValidationError("role with this name already exists")
        return role_obj

    def update(self, instance, validated_data):
        instance.name= validated_data.get('name', instance.name)
        instance.save()
        return instance

class StaffAddRoleSerializer(serializers.ModelSerializer):
    staff_id_list= serializers.ListField(write_only=True)
    name= serializers.CharField(read_only=True)
    class Meta:
        model= Role
        fields= [ 
                'id',
                'name',
                'staff',
                'staff_id_list',
                ]

    def update(self, instance, validated_data):
        for id in validated_data.get('staff_id_list', instance.name):
            staff_obj= Staff.objects.get(id=id)
            instance.staff.add(staff_obj)
        instance.save()
        return instance

class CourseSerializer(serializers.ModelSerializer):
    department= DepartmentCreateListSerializer(read_only=True)
    class Meta:
        model= Course
        fields= [
                'id',
                'course_name',
                'course_code',
                'course_unit',
                'level',
                'compulsory',
                'prerequsite_for',
                'department',
                'semester'
        ]

    def validate(self, attrs):
        if attrs.get('course_name'):
            attrs['course_name']= attrs.get('course_name').title()
        if attrs.get('course_code'):
            attrs['course_code']= attrs.get('course_code').upper()
        if attrs.get('semester'):
            attrs['semester']= attrs.get('semester').lower()
        return attrs

class CourseCreateListUpdateSerializer(serializers.ModelSerializer):
    department= DepartmentCreateListSerializer(read_only=True)
    prerequsite_for= CourseSerializer(read_only=True)
    department_id= serializers.SlugRelatedField(slug_field="id", queryset=Department.objects.all(), required=True, write_only=True)
    prerequsite_for_id= serializers.SlugRelatedField(slug_field="id", queryset=Course.objects.all(), required=False, write_only=True, allow_null=True)
    class Meta:
        model= Course
        fields= [
                'id',
                'course_name',
                'course_code',
                'course_unit',
                'level',
                'compulsory',
                'prerequsite_for',
                'prerequsite_for_id',
                'department',
                'department_id',
                'semester'
        ]

    def validate(self, attrs):
        if attrs.get('course_name'):
            attrs['course_name']= attrs.get('course_name').title()
        if attrs.get('course_code'):
            attrs['course_code']= attrs.get('course_code').upper()
        if attrs.get('semester'):
            attrs['semester']= attrs.get('semester').lower()
        return attrs

    def create(self, validated_data):
        try:
            course_obj= Course.objects.create(course_name=validated_data.get('course_name'),
                                                            course_code= validated_data.get('course_code'),
                                                            course_unit= validated_data.get('course_unit'),
                                                            compulsory= validated_data.get('compulsory'),
                                                            prerequsite_for= validated_data.get('prerequsite_for_id'),
                                                            department= validated_data.get("department_id"), 
                                                            semester= validated_data.get('semester'),
                                                            level= validated_data.get('level'))
        except IntegrityError:
            raise serializers.ValidationError({"detail":"requirement with same department, Course name and level already exists"})
        return course_obj

    def update(self, instance, validated_data):
        try:
            instance.course_name = validated_data.get('course_name', instance.course_name)
            instance.course_code= validated_data.get('course_code', instance.course_code)
            instance.course_unit= validated_data.get('course_unit', instance.course_unit)
            instance.compulsory= validated_data.get('compulsory', instance.compulsory)
            instance.prerequsite_for= validated_data.get('prerequsite_for_id', instance.prerequsite_for)
            instance.department= validated_data.get('department_id', instance.department)
            instance.semester= validated_data.get('semester', instance.semester)
            instance.level= validated_data.get('level', instance.level)
        except IntegrityError:
            raise serializers.ValidationError({"detail":"requirement with same department, Course name and level already exists"})
        instance.save()
        return instance

class CourseRegistrationCreateListSerializer(serializers.ModelSerializer):
    total_credit_first= serializers.CharField(write_only=True)
    total_credit_second= serializers.CharField(write_only=True)
    course_list_first_selected= serializers.ListField(write_only=True, required=True)
    course_list_second_selected= serializers.ListField(write_only=True, required=True)
    course= CourseCreateListUpdateSerializer(read_only=True)
    class Meta:
        model= CourseRegistration
        fields= [
                'calendar',
                'student',
                'course',
                'total_credit_first',
                'total_credit_second',
                'course_list_first_selected',
                'course_list_second_selected'
                ]
    
    def create(self, validated_data):
        request= self.context.get('request')

        try:
                session_obj= Session.objects.get(current_session=True)
        except:
                raise serializers.ValidationError({"details":"Session not set"})

        sum_credit_first= reduce(self.add_course_unit, validated_data.get('course_list_first_selected'))

        if int(sum_credit_first.get("course_unit")) > int(validated_data.get("total_credit_first")):
            raise serializers.ValidationError({"details":"Max credit exceeded for first semester"})

        sum_credit_second= reduce(self.add_course_unit, validated_data.get('course_list_second_selected'))
        if int(sum_credit_second.get("course_unit")) > int(validated_data.get("total_credit_second")):
            raise serializers.ValidationError({"details":"Max credit exceeded for second semester"})
        validated_data.get("course_list_first_selected").extend(validated_data.get("course_list_second_selected"))
        try:
            course_to_register= [ CourseRegistration(session=session_obj, calendar=f"{session_obj.start_year}/{session_obj.end_year}", student=request.user.student, course= Course.objects.get(id=course['id'])) for course in validated_data.get("course_list_first_selected")]
            CourseRegistrationStatus.objects.create(student=request.user.student, session=session_obj, status=True)
        except:
            raise serializers.ValidationError({"details":"user not signed in or user not a student"})

        course_registration_objs= CourseRegistration.objects.bulk_create(course_to_register)
        return course_registration_objs

    
    def add_course_unit(self, course_a, course_b):
        return {"course_unit": course_a["course_unit"] + course_b["course_unit"]}

    def rid(self, course_a):
        return course_a.get("compulsory")

class CourseRequirementCreateListSerializer(serializers.ModelSerializer):
    department= DepartmentCreateListSerializer(read_only=True)
    department_id= serializers.CharField(write_only= True, required=True)
    class Meta:
        model= CourseRequirement
        fields= [
                "id",
                "department",
                "semester",
                "total_credit",
                "level",
                "department_id",
                ]
    
    def create(self, validated_data):
        try:
            department_obj= Department.objects.get(id=validated_data.get('department_id'))
        except Department.DoesNotExist:
            raise serializers.ValidationError({"detail":"department with this id does not exist"})
        try:
            course_requirement_object= CourseRequirement.objects.create(department= department_obj, 
                                                                        semester= validated_data.get('semester'),
                                                                        total_credit= validated_data.get('total_credit'),
                                                                        level= validated_data.get('level'))
        except IntegrityError:
            raise serializers.ValidationError({"detail":"requirement with same department, registration and level already exists"})
        return course_requirement_object

class StudentCreateListSerializer(serializers.ModelSerializer):
    user= UserSerializer(read_only=True)
    calendar= serializers.CharField(read_only=True)
    department= DepartmentCreateListSerializer(read_only=True)
    matric_no= serializers.CharField(read_only=True)
    class Meta:
        model= Student
        fields= [   'id',
                    'user', 
                    'applicant',
                    'calendar',
                    'email',
                    'first_name',
                    'last_name',
                    'middle_name',
                    'matric_no',
                    'dob',
                    'nationality',
                    'state',
                    'department',
                    'lga',
                    'jamb_reg_no',
                    'phone',
                    'level',
                    'address',
                    'blood_group',
                    'gender',
                    'marital_status',
                    'religion',
                    'phone',
                    'address',
                    'next_kin_name',
                    'next_kin_relationship',
                    'next_kin_address',
                    'next_kin_phone',
                    'next_kin_email',
                    'picture',
                    'primary_cert',
                    'birth_cert',
                    'secondary_cert',
                    'testimonial',
                    'mode_of_entry',
                    'status',
                    'student_type'
                ]

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model= Payment
        fields= [
                "id",
                "name",
                "amount",
                "ref",
                "session",
                "calender",
                "student",
                "verified",
                "timestamp",
                "date_made"
                ]

# class CourseRegistrationCreateListSerializer(serializers.ModelSerializer):
#     total_credit_first= serializers.CharField(write_only=True)
#     total_credit_second= serializers.CharField(write_only=True)
#     course_list_first= serializers.ListField(write_only=True, required=False)
#     course_list_first_selected= serializers.ListField(write_only=True, required=False)
#     course_list_second= serializers.ListField(write_only=True, required=False)
#     course_list_second_selected= serializers.ListField(write_only=True, required=False)
#     course= CourseCreateListSerializer(read_only=True)
#     class Meta:
#         model= CourseRegistration
#         fields= [
#                 'calendar',
#                 'student',
#                 'course',
#                 'total_credit_first',
#                 'total_credit_second',
#                 'course_list_first',
#                 'course_list_first_selected',
#                 'course_list_second',
#                 'course_list_second_selected'
#                 ]
    
#     def create(self, validated_data):
#         request= self.context.get('request')
#         try:
#                 session_obj= Session.objects.get(current_session=True)
#         except:
#                 raise serializers.ValidationError({"details":"Session not set"})

#         sum_credit_first= reduce(self.add_course_unit, validated_data.get('course_list_first_selected'))
#         if sum_credit_first.get("course_unit") > validated_data.get("total_credit_first"):
#             raise serializers.ValidationError({"details":"Max credit exceeded for first semester"})

#         sum_credit_second= reduce(self.add_course_unit, validated_data.get('course_list_second_selected'))
#         if sum_credit_second.get("course_unit") > validated_data.get("total_credit_second"):
#             raise serializers.ValidationError({"details":"Max credit exceeded for second semester"})

#         list_compulsory_course_first= list(filter(self.rid, validated_data.get("course_list_first")))
#         list_compulsory_course_selected_first= list(filter(self.rid, validated_data.get("course_list_first_selected")))
#         selected_all_first= any(x not in list_compulsory_course_first for x in list_compulsory_course_selected_first)
#         if not selected_all_first:
#             raise serializers.ValidationError({"details":"Please select all required courses for first semester"})

#         list_compulsory_course_second= list(filter(self.rid, validated_data.get("course_list_second")))
#         list_compulsory_course_selected_second= list(filter(self.rid, validated_data.get("course_list_second_selected")))
#         selected_all_second= any(x not in list_compulsory_course_second for x in list_compulsory_course_selected_second)
#         if not selected_all_second:
#             raise serializers.ValidationError({"details":"Please select all required courses for second semester"})

#         validated_data.get("course_list_first_selected").extend(validated_data.get("course_list_second_selected"))
#         try:
#             course_to_register= [ CourseRegistration(session=session_obj, calendar=f"{session_obj.start_year}/{session_obj.end_year}", student=request.user.student, course= course) for course in validated_data.get("course_list_first_selected")]
#         except:
#             raise serializers.ValidationError({"details":"user not signed in or user not a student"})

#         course_registration_objs= CourseRegistration.objects.bulk_create(course_to_register)
#         return course_registration_objs
