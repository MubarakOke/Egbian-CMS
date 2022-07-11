from django.shortcuts import render
from rest_framework.generics import ListAPIView, RetrieveAPIView, UpdateAPIView, CreateAPIView, GenericAPIView
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin, DestroyModelMixin, ListModelMixin
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from rest_framework.views import APIView
from django.conf import settings
from operations.renderers import DefaultRenderer
from operations.models import Applicant, Session, Staff, Role, Department, Faculty
from operations import serializers
from rest_framework.response import Response
from operations.utils import EmailThread

from .models import Role, Student, Department, Session, Applicant

# Create your views here.

class SessionCreateListView(CreateModelMixin, ListAPIView):
    parser_classes = (JSONParser, MultiPartParser, FormParser)
    serializer_class= serializers.SessionSerializer
    renderer_classes= [DefaultRenderer]
    queryset= Session.objects.all()
    permission_classes= []

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
        
class ApplicantCreateView(CreateModelMixin, ListAPIView):
    parser_classes = (JSONParser, MultiPartParser, FormParser)
    serializer_class= serializers.ApplicantSerializer
    renderer_classes= [DefaultRenderer]
    queryset= Applicant.objects.all()
    permission_classes= []

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class ApplicantUpdateView(UpdateModelMixin, DestroyModelMixin, RetrieveAPIView):
    parser_classes = (JSONParser, MultiPartParser, FormParser)
    serializer_class= serializers.ApplicantUpdateSerializer
    renderer_classes= [DefaultRenderer]
    lookup_field= 'id'
    queryset= Applicant.objects.all()
    permission_classes= []

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
    def patch(self, request, *args, **kwargs):
        return self.update(request, *args, kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class DashboardView(APIView):
    parser_classes = (JSONParser, MultiPartParser, FormParser)
    renderer_classes= [DefaultRenderer]
    permission_classes= []

    def get(self, request, *args, **kwargs):
        student_count= Student.objects.all().count()
        department_count= Department.objects.all().count()
        applicant_count= Applicant.objects.filter(session__current_session=True).count()

        return Response({"student_count": student_count, 
                        "department_count":department_count,
                        "applicant_count":applicant_count}, 200)


class StaffCreateListView(CreateModelMixin, ListAPIView):
    parser_classes = (JSONParser, MultiPartParser, FormParser)
    renderer_classes= [DefaultRenderer]
    serializer_class= serializers.StaffCreateListSerializer
    queryset= Staff.objects.all()
    permission_classes= []

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class RoleCreateListView(CreateModelMixin, ListAPIView):
    parser_classes = (JSONParser, MultiPartParser, FormParser)
    renderer_classes= [DefaultRenderer]
    serializer_class= serializers.RoleCreateListSerializer
    queryset= Role.objects.all()
    permission_classes= []

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class RoleDetailView(UpdateModelMixin, DestroyModelMixin, RetrieveAPIView):
    parser_classes = (JSONParser, MultiPartParser, FormParser)
    renderer_classes= [DefaultRenderer]
    serializer_class= serializers.RoleCreateListSerializer
    queryset= Role.objects.all()
    lookup_field= 'id'
    permission_classes= []

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
    def patch(self, request, *args, **kwargs):
        return self.update(request, *args, kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

class StaffAddRoleView(UpdateAPIView):
    parser_classes = (JSONParser, MultiPartParser, FormParser)
    renderer_classes= [DefaultRenderer]
    serializer_class= serializers.StaffAddRoleSerializer
    queryset= Role.objects.all()
    lookup_field= 'id'
    permission_classes= []

class DepartmentCreateListView(CreateModelMixin, ListAPIView):
    parser_classes = (JSONParser, MultiPartParser, FormParser)
    renderer_classes= [DefaultRenderer]
    serializer_class= serializers.DepartmentCreateListSerializer
    queryset= Department.objects.all()
    permission_classes= []
    search_fields= ('faculty__name', 'name')

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class DepartmentDetailView(UpdateModelMixin, DestroyModelMixin, RetrieveAPIView):
    parser_classes = (JSONParser, MultiPartParser, FormParser)
    renderer_classes= [DefaultRenderer]
    serializer_class= serializers.DepartmentUpdateSerializer
    queryset= Department.objects.all()
    lookup_field= 'id'
    permission_classes= []

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
    def patch(self, request, *args, **kwargs):
        return self.update(request, *args, kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

class FacultyCreateListView(CreateModelMixin, ListAPIView):
    parser_classes = (JSONParser, MultiPartParser, FormParser)
    renderer_classes= [DefaultRenderer]
    serializer_class= serializers.FacultyCreateListSerializer
    queryset= Faculty.objects.all()
    permission_classes= []
    search_fields= ('name')

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class FacultyDetailView(UpdateModelMixin, DestroyModelMixin, RetrieveAPIView):
    parser_classes = (JSONParser, MultiPartParser, FormParser)
    renderer_classes= [DefaultRenderer]
    serializer_class= serializers.FacultyCreateListSerializer
    queryset= Faculty.objects.all()
    lookup_field= 'id'
    permission_classes= []

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
    def patch(self, request, *args, **kwargs):
        return self.update(request, *args, kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)