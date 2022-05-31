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
    serializer_class= serializers.UpdateApplicantSerializer
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
