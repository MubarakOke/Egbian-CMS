from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from accounts.serializers import UserSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.db.models import Q
from operations.models import  Applicant
from operations.renderers import DefaultRenderer
from operations.serializers import SessionSerializer, DepartmentCreateListSerializer

User = get_user_model()


# Authenticate
# generate token
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class AuthenticateApplicantView(APIView):
    permission_classes= []
    authentication_classes= []
    renderer_classes= [DefaultRenderer]

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return Response({"detail":"You are already authenticated"}, status= 400)
        username= request.data.get('username', None)
        password= request.data.get('password')

        obj=None
        if username and password:
            obj= User.objects.filter(Q(username__iexact=username))
        else:
            return Response({"error": "Please enter your username and password"}, status=400)
  
        if obj and obj.count()==1:
            user_obj= obj.first() 
            print(user_obj)
            if user_obj.check_password(password) and (user_obj.user_type == 'applicant' or user_obj.user_type == 'student'):
                token= get_tokens_for_user(user_obj)
                return Response({"token": token["access"],
                                "id": user_obj.applicant.id,
                                "user": UserSerializer(user_obj).data, 
                                "session": SessionSerializer(user_obj.applicant.session).data,
                                "email":user_obj.applicant.email,
                                "first_name":user_obj.applicant.first_name, 
                                "last_name":user_obj.applicant.last_name,
                                "phone":user_obj.applicant.phone,
                                "nationality":user_obj.applicant.nationality,
                                "state":user_obj.applicant.state,
                                "lga":user_obj.applicant.lga,
                                "jamb_reg_no":user_obj.applicant.jamb_reg_no,
                                "dob":user_obj.applicant.dob,
                                "gender":user_obj.applicant.gender,
                                "mode_of_entry":user_obj.applicant.mode_of_entry,
                                "department": DepartmentCreateListSerializer(user_obj.applicant.department).data,
                                "status": user_obj.applicant.status,
                                "is_admitted":user_obj.applicant.is_admitted,
                                "picture":user_obj.applicant.pictureURL,
                                "primary_cert":user_obj.applicant.primary_certURL,
                                "secondary_cert":user_obj.applicant.secondary_certURL,
                                "testimonial":user_obj.applicant.testimonialURL,
                                "birth_cert":user_obj.applicant.birth_certURL,
                                "result_first":user_obj.applicant.result_firstURL,
                                "result_second":user_obj.applicant.result_secondURL,
                                "next_kin_name":user_obj.applicant.next_kin_name,
                                "next_kin_relationship":user_obj.applicant.next_kin_relationship,
                                "next_kin_email":user_obj.applicant.next_kin_email,
                                "next_kin_address":user_obj.applicant.next_kin_address,
                                "next_kin_phone":user_obj.applicant.next_kin_phone,
                                }, status=200)
        return Response({"error": "invalid login details"}, status=400)

class AuthenticateStudentView(APIView):
    permission_classes= []
    authentication_classes= []
    renderer_classes= [DefaultRenderer]

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return Response({"detail":"You are already authenticated"}, status= 400)
        username= request.data.get('username', None)
        password= request.data.get('password')

        obj=None
        if username and password:
            obj= User.objects.filter(Q(username__iexact= username))
        else:
            return Response({"error": "Please enter your amail and password"}, status=400)
  
        if obj and obj.count()==1:
            user_obj= obj.first() 
            print(user_obj)
            if user_obj.check_password(password) and user_obj.user_type == 'student':
                token= get_tokens_for_user(user_obj)
                return Response({"token": token["access"],
                                "user": UserSerializer(user_obj).data, 
                                "id": user_obj.student.id,
                                "user": UserSerializer(user_obj).data, 
                                "session": SessionSerializer(user_obj.student.session).data,
                                "email":user_obj.student.email,
                                "first_name":user_obj.student.first_name, 
                                "last_name":user_obj.student.last_name,
                                "phone":user_obj.student.phone,
                                "nationality":user_obj.student.nationality,
                                "state":user_obj.student.state,
                                "lga":user_obj.student.lga,
                                "jamb_reg_no":user_obj.student.jamb_reg_no,
                                "level":user_obj.student.level,
                                "dob":user_obj.student.dob,
                                "gender":user_obj.student.gender,
                                "mode_of_entry":user_obj.student.mode_of_entry,
                                "department": DepartmentCreateListSerializer(user_obj.student.department).data,
                                "status": user_obj.student.status,
                                "picture":user_obj.student.pictureURL,
                                "primary_cert":user_obj.student.primary_certURL,
                                "secondary_cert":user_obj.student.secondary_certURL,
                                "testimonial":user_obj.student.testimonialURL,
                                "result_first":user_obj.applicant.result_firstURL,
                                "result_second":user_obj.applicant.result_secondURL,
                                "birth_cert":user_obj.student.birth_certURL,
                                "marital_status":user_obj.student.marital_status,
                                "religion":user_obj.student.religion,
                                "address":user_obj.student.address,
                                "blood_group":user_obj.student.blood_group,
                                "student_type":user_obj.student.student_type,
                                "next_kin_name":user_obj.student.next_kin_name,
                                "next_kin_relationship":user_obj.student.next_kin_relationship,
                                "next_kin_email":user_obj.student.next_kin_email,
                                "next_kin_address":user_obj.student.next_kin_address,
                                "next_kin_phone":user_obj.student.next_kin_phone,
                                }, status=200)
        return Response({"error": "invalid login details"}, status=400)


class AuthenticateAdminView(APIView):
    permission_classes= []
    authentication_classes= []

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return Response({"detail":"You are already authenticated"}, status= 400)
        username= request.data.get('username', None)
        password= request.data.get('password')

        obj=None
        if username and password:
            obj= User.objects.filter(Q(username__iexact= username))
        else:
            return Response({"error": "Please enter your username and password"}, status=400)
  
        if obj and obj.count()==1:
            user_obj= obj.first() 
            print(user_obj)
            if user_obj.check_password(password) and user_obj.user_type == 'staff':
                if user_obj.staff.staff_type== 'admin':
                    token= get_tokens_for_user(user_obj)
                    return Response({"token": token["access"],
                                    "user": UserSerializer(user_obj).data, 
                                    "id": user_obj.staff.id,
                                    "user": UserSerializer(user_obj).data, 
                                    "email":user_obj.staff.email,
                                    "first_name":user_obj.staff.first_name, 
                                    "last_name":user_obj.staff.last_name,
                                    "phone":user_obj.staff.phone,
                                    "nationality":user_obj.staff.nationality,
                                    "state":user_obj.staff.state,
                                    "lga":user_obj.staff.lga,
                                    "dob":user_obj.staff.dob,
                                    "gender":user_obj.staff.gender,
                                    "department": DepartmentCreateListSerializer(user_obj.staff.department).data,
                                    "staff_type": user_obj.staff.staff_type,
                                    "picture":user_obj.staff.pictureURL,                                          
                                    }, status=200)
        return Response({"error": "invalid login details"}, status=400)
    
# class AuthenticateLecturerView(APIView):
#     permission_classes= []
#     authentication_classes= []
#     renderer_classes= [DefaultRenderer]

#     def post(self, request, *args, **kwargs):
#         if request.user.is_authenticated:
#             return Response({"detail":"You are already authenticated"}, status= 400)
#         username= request.data.get('username', None)
#         password= request.data.get('password')

#         obj=None
#         if username and password:
#             obj= User.objects.filter(Q(username__iexact= username))
#         else:
#             return Response({"error": "Please enter your amail and password"}, status=400)
  
#         if obj and obj.count()==1:
#             user_obj= obj.first() 
#             print(user_obj)
#             if user_obj.check_password(password) and user_obj.user_type == 'staff':
#                 if user_obj.staff.staff_type== 'admin':
#                     token= get_tokens_for_user(user_obj)
#                     return Response({"token": token["access"],
#                                     "user": UserSerializer(user_obj).data,                                           
#                                     }, status=200)
#         return Response({"error": "invalid login details"}, status=400)

# class AuthenticateRegistrarView(APIView):
#     permission_classes= []
#     authentication_classes= []

#     def post(self, request, *args, **kwargs):
#         if request.user.is_authenticated:
#             return Response({"detail":"You are already authenticated"}, status= 400)
#         username= request.data.get('username', None)
#         password= request.data.get('password')

#         obj=None
#         if username and password:
#             obj= User.objects.filter(Q(username__iexact= username))
#         else:
#             return Response({"error": "Please enter your amail and password"}, status=400)
  
#         if obj and obj.count()==1:
#             user_obj= obj.first() 
#             print(user_obj)
#             if user_obj.check_password(password) and user_obj.user_type == 'staff' and user_obj.position=='registrar':
#                 token= get_tokens_for_user(user_obj)
#                 return Response({"token": token["access"],
#                                 "user": UserSerializer(user_obj).data, 
#                                 "id": user_obj.staff.id,
#                                 "user": UserSerializer(user_obj).data, 
#                                 "email":user_obj.staff.email,
#                                 "first_name":user_obj.staff.first_name, 
#                                 "last_name":user_obj.staff.last_name,
#                                 "phone":user_obj.staff.phone,
#                                 "nationality":user_obj.staff.nationality,
#                                 "state":user_obj.staff.state,
#                                 "lga":user_obj.staff.lga,
#                                 "dob":user_obj.staff.dob,
#                                 "gender":user_obj.staff.gender,
#                                 "department": DepartmentCreateListSerializer(user_obj.staff.department).data,
#                                 "staff_type": user_obj.staff.staff_type,
#                                 "picture":user_obj.staff.pictureURL,                                          
#                                 }, status=200)
#         return Response({"error": "invalid login details"}, status=400)

# class AuthenticateVcView(APIView):
#     permission_classes= []
#     authentication_classes= []

#     def post(self, request, *args, **kwargs):
#         if request.user.is_authenticated:
#             return Response({"detail":"You are already authenticated"}, status= 400)
#         username= request.data.get('username', None)
#         password= request.data.get('password')

#         obj=None
#         if username and password:
#             obj= User.objects.filter(Q(username__iexact= username))
#         else:
#             return Response({"error": "Please enter your amail and password"}, status=400)
  
#         if obj and obj.count()==1:
#             user_obj= obj.first() 
#             print(user_obj)
#             if user_obj.check_password(password) and user_obj.user_type == 'staff' and user_obj.position=='vc':
#                 token= get_tokens_for_user(user_obj)
#                 return Response({"token": token["access"],
#                                 "user": UserSerializer(user_obj).data,                                           
#                                 }, status=200)
#         return Response({"error": "invalid login details"}, status=400)


