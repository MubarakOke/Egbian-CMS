from django.shortcuts import render

from rest_framework.response import Response
from django.db.models import Q

from rest_framework.views import APIView

from . import serializers

from django.contrib.auth import get_user_model

from rest_framework_simplejwt.authentication import JWTAuthentication

from .permissions import SuperuserPermissionOnly
from operations.serializers import AdminSerializer
from accounts.serializers import UserSerializer
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


# Authenticate
# generate token
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

# Authenticate User view
class AuthenticateView(APIView):
    permission_classes= []
    authentication_classes= []

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return Response({"detail":"You are already authenticated"}, status= 400)
        phone= request.data.get('phone', None)
        email= request.data.get('email', None)
        password= request.data.get('password')

        obj=None
        if phone:
            obj= User.objects.filter(Q(phone__iexact= phone)&Q(user_type="Vendor"))
        if email:
            obj= User.objects.filter(Q(email__iexact= email))

        if obj.count()==1:
            user_obj= obj.first() 
            if user_obj.check_password(password):
                user = user_obj
                token= get_tokens_for_user(user)
                if user.user_type == 'Vendor':
                    return Response({
                                    "email": user.email, 
                                    "refresh": token["refresh"], 
                                    "access_token": token["access"],
                                    "id": user.vendor.id,
                                    "user": UserSerializer(user).data,                                          
                                    }, status=201)

                elif user.user_type == 'Rider':
                    return Response({
                                    "email": user.email, 
                                    "refresh": token["refresh"], 
                                    "access_token": token["access"],
                                    "id": user.rider.id,
                                    "user": UserSerializer(user).data,                                          
                                    }, status=201)

                elif user.user_type == 'Admin':
                    return Response({"email": user.email, 
                                    "refresh": token["refresh"], 
                                    "access_token": token["access"],
                                    "id": user.admin.id,  
                                    "user": UserSerializer(user).data,
                                    "company_name": user.admin.company_name,
                                    "description": user.admin.description,                                            
                                    })
                elif user.user_type == 'Super Admin':
                    return Response({"email": user.email, 
                                    "refresh": token["refresh"], 
                                    "access_token": token["access"],
                                    "user": UserSerializer(user).data,                                           
                                    })
                else:
                    Response({"error":"Unknown user"}, status=400)

            return Response({"error": "invalid password"}, status=401)
        return Response({"error": "invalid login details"}, status=400)


class AuthenticateSuperAdminView(APIView):
    permission_classes= []
    authentication_classes= []

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return Response({"detail":"You are already authenticated"}, status= 400)
        email= request.data.get('email', None)
        password= request.data.get('password')

        obj=None
        if email and password:
            obj= User.objects.filter(Q(email__iexact= email))
        else:
            return Response({"error": "Please enter your amail and password"}, status=400)
  
        if obj and obj.count()==1:
            user_obj= obj.first() 
            print(user_obj)
            if user_obj.check_password(password) and user_obj.user_type == 'Super Admin':
                token= get_tokens_for_user(user_obj)
                return Response({"email": user_obj.email, 
                                "refresh": token["refresh"], 
                                "access_token": token["access"],
                                "user": UserSerializer(user_obj).data,                                           
                                }, status=200)
        return Response({"error": "invalid login details"}, status=400)

class AuthenticateAdminView(APIView):
    permission_classes= []
    authentication_classes= []

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return Response({"detail":"You are already authenticated"}, status= 400)
        email= request.data.get('email', None)
        password= request.data.get('password', None)

        obj=None
        if email and password:
            obj= User.objects.filter(Q(email__iexact= email))
        else:
            return Response({"error": "Please enter login credentials"}, status=400)
        
        if obj and obj.count()==1:
            user_obj= obj.first() 
            if user_obj.check_password(password) and user_obj.user_type == 'Admin':
                token= get_tokens_for_user(user_obj)
                return Response({"email": user_obj.email, 
                                "refresh": token["refresh"], 
                                "access_token": token["access"],
                                "id": user_obj.admin.id,  
                                "user": UserSerializer(user_obj).data,
                                "company_name": user_obj.admin.company_name,
                                "description": user_obj.admin.description,                                            
                                }, status=200)
        return Response({"error": "invalid login details"}, status=400)

class AuthenticateRiderView(APIView):
    permission_classes= []
    authentication_classes= []

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return Response({"detail":"You are already authenticated"}, status= 400)
        email= request.data.get('email', None)
        phone= request.data.get('phone', None)
        password= request.data.get('password', None)

        obj=None
        if phone and password:
            obj= User.objects.filter(Q(phone__iexact= phone))
        elif email and password:
            obj= User.objects.filter(Q(email__iexact= email))
        else:
            return Response({"error": "Please enter login credentials"}, status=400)
        
        if obj and obj.count()==1:
            user_obj= obj.first() 
            if user_obj.check_password(password) and user_obj.user_type == 'Rider':
                token= get_tokens_for_user(user_obj)
                return Response({
                                    "email": user_obj.email, 
                                    "refresh": token["refresh"], 
                                    "access_token": token["access"],
                                    "id": user_obj.rider.id,
                                    "user": UserSerializer(user_obj).data,                                          
                                    }, status=200)
        return Response({"error": "invalid login details"}, status=400)

class AuthenticateVendorView(APIView):
    permission_classes= []
    authentication_classes= []

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return Response({"detail":"You are already authenticated"}, status= 400)
        email= request.data.get('email', None)
        phone= request.data.get('phone', None)
        password= request.data.get('password', None)

        obj=None
        if phone and password:
            obj= User.objects.filter(Q(phone__iexact= phone))
        elif email and password:
            obj= User.objects.filter(Q(email__iexact= email))
        else:
            return Response({"error": "Please enter login credentials"}, status=400)
        
        if obj and obj.count()==1:
            user_obj= obj.first() 
            if user_obj.check_password(password) and user_obj.user_type == 'Vendor':
                token= get_tokens_for_user(user_obj)
                return Response({
                                "email": user_obj.email, 
                                "refresh": token["refresh"], 
                                "access_token": token["access"],
                                "id": user_obj.vendor.id,
                                "user": UserSerializer(user_obj).data,                                          
                                }, status=200)
        return Response({"error": "invalid login details"}, status=400)




class UserListView(ListAPIView): 
    serializer_class= serializers.UserSerializer
    queryset= User.objects.all()


class UserDetailView(RetrieveAPIView):
    authentication_classes= [] 
    permission_classes= [] 
    serializer_class= serializers.UserSerializer
    queryset= User.objects.all()
    lookup_field= 'email'

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
    def patch(self, request, *args, **kwargs):
        return self.update(request, *args, kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


