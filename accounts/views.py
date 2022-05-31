from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from accounts.serializers import UserSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.db.models import Q
from operations.renderers import DefaultRenderer

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
            if user_obj.check_password(password) and user_obj.user_type == 'applicant':
                token= get_tokens_for_user(user_obj)
                return Response({"token": token["access"],
                                "user": UserSerializer(user_obj).data,                                           
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
                                }, status=200)
        return Response({"error": "invalid login details"}, status=400)
    
class AuthenticateLecturerView(APIView):
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
            if user_obj.check_password(password) and user_obj.user_type == 'staff' and user_obj.position=='lecturer':
                token= get_tokens_for_user(user_obj)
                return Response({"token": token["access"],
                                "user": UserSerializer(user_obj).data,                                           
                                }, status=200)
        return Response({"error": "invalid login details"}, status=400)

class AuthenticateRegistrarView(APIView):
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
            return Response({"error": "Please enter your amail and password"}, status=400)
  
        if obj and obj.count()==1:
            user_obj= obj.first() 
            print(user_obj)
            if user_obj.check_password(password) and user_obj.user_type == 'staff' and user_obj.position=='registrar':
                token= get_tokens_for_user(user_obj)
                return Response({"token": token["access"],
                                "user": UserSerializer(user_obj).data,                                           
                                }, status=200)
        return Response({"error": "invalid login details"}, status=400)

class AuthenticateVcView(APIView):
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
            return Response({"error": "Please enter your amail and password"}, status=400)
  
        if obj and obj.count()==1:
            user_obj= obj.first() 
            print(user_obj)
            if user_obj.check_password(password) and user_obj.user_type == 'staff' and user_obj.position=='vc':
                token= get_tokens_for_user(user_obj)
                return Response({"token": token["access"],
                                "user": UserSerializer(user_obj).data,                                           
                                }, status=200)
        return Response({"error": "invalid login details"}, status=400)