from tracemalloc import start
from rest_framework import serializers
from accounts.serializers import UserSerializer
from operations.models import Applicant, Session
from django.contrib.auth import get_user_model
from operations.utils import EmailThread
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.core.exceptions import ObjectDoesNotExist


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
            raise ValidationError("start year cannot be higher than end year")
        return attrs
    
    def create(self, validated_data):
        try:
            session_prev_obj= Session.objects.latest('id')
            session_prev_obj.current_session= False
            session_prev_obj.save()
            print("inside try")
        except ObjectDoesNotExist:
            print("inside except")
            pass

        session_obj= Session.objects.create(
                                            start_year= validated_data.get('start_year'),
                                            end_year= validated_data.get('end_year')
                                            )
        session_obj.save()
        return session_obj



class ApplicantSerializer(serializers.ModelSerializer):
    user= UserSerializer(read_only=True)
    password= serializers.CharField(write_only=True, required=True)
    class Meta:
        model= Applicant
        fields= [
                'id',
                'user',
                'email',
                'password'
                ]

    def create(self, validated_data): 
        try:
            session_obj= Session.objects.get(current_session=True)
        except:
            raise serializers.ValidationError({"details":"Session not set"}) 
        applicant_id= int(str(session_obj.start_year) + "00000") 
        user_obj= User.objects.create(
                                    user_type= "applicant",
                                    position= "applicant",
                                    )
        username= f"APP{str(applicant_id + int(user_obj.id))}"
        user_obj.username= username
        user_obj.set_password(validated_data.pop('password', None))

        applicant_obj = Applicant.objects.create(user=user_obj, session= session_obj, email= validated_data.get('email'))        
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
            raise serializers.ValidationError({"details":"email not sent"})
        return applicant_obj

class UpdateApplicantSerializer(serializers.ModelSerializer):
    user= UserSerializer(read_only=True)
    class Meta:
        model= Applicant
        fields= [
                'id',
                'user',
                'email',
                'first_name', 
                'last_name',
                'phone',
                'nationality',
                'state',
                'lga',
                'jamb_reg_no',
                'dob',
                'gender',
                'mode_of_entry',
                'is_admitted',
                'picture',
                'primary_cert',
                'birth_cert',
                ]

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name).lower()
        instance.last_name= validated_data.get('last_name', instance.last_name).lower()
        instance.phone= validated_data.get('phone', instance.phone)
        instance.nationality= validated_data.get('nationality', instance.nationality).lower()
        instance.state= validated_data.get('state', instance.state).lower()
        instance.lga= validated_data.get('lga', instance.lga).lower()
        instance.jamb_reg_no= validated_data.get('jamb_reg_no', instance.jamb_reg_no).upper()
        instance.dob= validated_data.get('dob', instance.dob)
        instance.gender= validated_data.get('gender', instance.gender).lower()
        instance.picture= validated_data.get('picture', instance.picture)
        instance.primary_cert= validated_data.get('primary_cert', instance.primary_cert)
        instance.birth_cert= validated_data.get('birth_cert', instance.birth_cert)
        instance.mode_of_entry= validated_data.get('mode_of_entry', instance.mode_of_entry).lower()
        instance.save()
        return instance