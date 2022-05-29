from django.shortcuts import render
from rest_framework.generics import ListAPIView, RetrieveAPIView, UpdateAPIView, CreateAPIView
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin, DestroyModelMixin, ListModelMixin
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from django.conf import settings
from operations.renderers import DefaultRenderer
from operations.models import Applicant, Session
from operations import serializers
from operations.utils import EmailThread

# Create your views here.

class SessionCreateListView(CreateModelMixin, ListAPIView):
    parser_classes = (JSONParser, MultiPartParser, FormParser)
    serializer_class= serializers.SessionSerializer
    renderer_classes= [DefaultRenderer]
    queryset= Session.objects.all()
    permission_classes= []

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
        
class ApplicantCreateView(CreateAPIView):
    parser_classes = (JSONParser, MultiPartParser, FormParser)
    serializer_class= serializers.ApplicantSerializer
    renderer_classes= [DefaultRenderer]
    permission_classes= []
class ApplicantUpdateView(UpdateAPIView):
    parser_classes = (JSONParser, MultiPartParser, FormParser)
    serializer_class= serializers.ApplicantSerializer
    renderer_classes= [DefaultRenderer]
    permission_classes= []
