from requests import session
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, RetrieveAPIView, UpdateAPIView, CreateAPIView, GenericAPIView
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin, DestroyModelMixin, ListModelMixin
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from rest_framework.views import APIView
from django.conf import settings
from operations.renderers import DefaultRenderer
from operations.models import Applicant, Session, Staff, Role, Department, Faculty, Course, CourseRegistration, CourseRequirement, Result
from operations import serializers
from rest_framework.response import Response
from operations.utils import EmailThread
from django.db.models import Q

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
        
class ApplicantCreateListView(CreateModelMixin, ListAPIView):
    parser_classes = (JSONParser, MultiPartParser, FormParser)
    serializer_class= serializers.ApplicantSerializer
    renderer_classes= [DefaultRenderer]
    queryset= Applicant.objects.all()
    permission_classes= []

    def get_queryset(self):
        q= self.request.GET.get('q', None)
        if q:
            if q=="all":
                return self.queryset
            else:
                return self.queryset.filter(session__start_year=q)
                
        try:
            session_obj= Session.objects.get(current_session=True)
        except:
            return ""
        return self.queryset.filter(session=session_obj)

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

class StudentCreateListView(CreateModelMixin, ListAPIView):
    parser_classes = (JSONParser, MultiPartParser, FormParser)
    renderer_classes= [DefaultRenderer]
    serializer_class= serializers.StudentCreateListSerializer
    queryset= Student.objects.all()
    permission_classes= []

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class StudentDetailView(UpdateModelMixin, DestroyModelMixin, RetrieveAPIView):
    parser_classes = (JSONParser, MultiPartParser, FormParser)
    renderer_classes= [DefaultRenderer]
    serializer_class= serializers.StudentCreateListSerializer
    queryset= Student.objects.all()
    permission_classes= []
    lookup_field= 'id'

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
    def patch(self, request, *args, **kwargs):
        return self.update(request, *args, kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

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

class CourseCreateListView(CreateModelMixin, ListAPIView):
    parser_classes = (JSONParser, MultiPartParser, FormParser)
    renderer_classes= [DefaultRenderer]
    serializer_class= serializers.CourseCreateListSerializer
    queryset= Course.objects.all()
    permission_classes= []

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class CourseDetailView(UpdateModelMixin, DestroyModelMixin, RetrieveAPIView):
    parser_classes = (JSONParser, MultiPartParser, FormParser)
    renderer_classes= [DefaultRenderer]
    serializer_class= serializers.CourseCreateListSerializer
    queryset= Course.objects.all()
    lookup_field= 'id'
    permission_classes= []

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
    def patch(self, request, *args, **kwargs):
        return self.update(request, *args, kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

class CourseRequirementCreateListView(CreateModelMixin, ListAPIView):
    parser_classes = (JSONParser, MultiPartParser, FormParser)
    renderer_classes= [DefaultRenderer]
    serializer_class= serializers.CourseRequirementCreateListSerializer
    queryset= CourseRequirement.objects.all()
    lookup_field= 'id'
    permission_classes= []

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class CourseRequirementdetailView(UpdateModelMixin, DestroyModelMixin, RetrieveAPIView):
    parser_classes = (JSONParser, MultiPartParser, FormParser)
    renderer_classes= [DefaultRenderer]
    serializer_class= serializers.CourseRequirementCreateListSerializer
    queryset= CourseRequirement.objects.all()
    lookup_field= 'id'
    permission_classes= []

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
    def patch(self, request, *args, **kwargs):
        return self.update(request, *args, kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class CourseRegistrationListCreateView(CreateModelMixin, ListAPIView):
    parser_classes = (JSONParser, MultiPartParser, FormParser)
    renderer_classes= [DefaultRenderer]
    serializer_class= serializers.CourseRegistrationCreateListSerializer
    queryset= CourseRegistration.objects.all()
    permission_classes= []

    def get_serializer_context(self):
        return {"request": self.request}

    def get_queryset(self):
        q= self.request.GET.get('q', None)
        try:
                session_obj= Session.objects.get(current_session=True)
        except:
                return ""
        if q:
            try:
                session_obj= Session.objects.get(start_year=q)
            except:
                return ""
        try:
            return self.queryset.filter(Q(session=session_obj) and Q(student=self.request.user.sudent))
        except:
            return ""

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class CourseToRegisterView(APIView):
    parser_classes = (JSONParser, MultiPartParser, FormParser)
    renderer_classes= [DefaultRenderer]
    permission_classes= []

    def get(self, request, *args, **kwargs):
        try:
            student_obj= request.user.student
        except:
            return Response({"detail": "user is not a student"}, 404)
        course_requirement_obj= CourseRequirement.objects.filter(Q(level=student_obj.level) & Q(department=student_obj.department)).order_by('semester')
        course_requirement_obj_first= course_requirement_obj[0]
        course_requirement_obj_second= course_requirement_obj[1]
        course_objs= Course.objects.filter(Q(level=student_obj.level) & Q(department=student_obj.department))
        course_list_first= []
        course_list_second= []
        for course in course_objs:
            if course.prerequsite_for:
                prerequsite_course_obj= Course.objects.filter(prerequsite_for=course.prerequsite_for).first()
                try:
                    result_for_course= Result.objects.filter(Q(course=prerequsite_course_obj) & Q(student= request.user.student)).latest()
                except:
                    return Response({"details":"no result of prerequsite course"})
                if result_for_course.score < 40.0:
                    if prerequsite_course_obj.semester.lower() == "first":
                        course_list_first.append(prerequsite_course_obj)
                    else:
                        course_list_second.append(prerequsite_course_obj)
                else:
                    if prerequsite_course_obj.semester.lower() == "first":
                        course_list_first.append(course)
                    else:
                        course_list_second.append(course)
            else:
                if course.semester.lower() == "first":
                    course_list_first.append(course)
                else:
                    course_list_second.append(course)
        return Response({"details": {
                                    "requirement_first": serializers.CourseRequirementCreateListSerializer(course_requirement_obj_first).data,
                                    "courses_first":serializers.CourseCreateListSerializer(course_list_first, many=True).data,
                                    "requirement_second": serializers.CourseRequirementCreateListSerializer(course_requirement_obj_second).data,
                                    "courses_second": serializers.CourseCreateListSerializer(course_list_second, many=True).data
                                    }})

                
class ApplicantStatusChangeView(APIView):
    parser_classes = (JSONParser, MultiPartParser, FormParser)
    renderer_classes= [DefaultRenderer]
    permission_classes= []

    def post(self, request, *args, **kwargs):
        id= self.kwargs.get("id")
        adm_status= request.data.get('status', None)
        department_id= request.data.get('department_id', None)
        applicant_obj= Applicant.objects.get(id=id)
        applicant_obj.status= adm_status
        if department_id:
            department_obj= Department.objects.get(id=department_id) 
            department= department_obj
        else:
            department= applicant_obj.department
        if adm_status=="admitted":
            applicant_obj.is_admitted= True
            applicant_obj.user.user_type="student"
            applicant_obj.user.save()
            if applicant_obj.mode_of_entry=="utme":
                level= 100
                student_type= "undergraduate"
            elif applicant_obj.mode_of_entry=="direct entry":
                level= 200
                student_type= "undergraduate"
            elif not applicant_obj.mode_of_entry:
                level= 100
                student_type= "undergraduate"
            data= {
                    "user" : applicant_obj.user,
                    "applicant" : applicant_obj,
                    "session": applicant_obj.session,
                    "calendar": f"{applicant_obj.calendar}",
                    "department": department,
                    "email": applicant_obj.email,
                    "first_name": applicant_obj.first_name,
                    "last_name": applicant_obj.last_name,
                    "middle_name": applicant_obj.middle_name,
                    "dob": applicant_obj.dob,
                    "gender": applicant_obj.gender,
                    "nationality": applicant_obj.nationality,
                    "state": applicant_obj.state,
                    "lga": applicant_obj.lga,
                    "jamb_reg_no": applicant_obj.jamb_reg_no,
                    "phone": applicant_obj.phone,
                    "level":level,
                    "picture": applicant_obj.picture,
                    "primary_cert": applicant_obj.primary_cert,
                    "birth_cert": applicant_obj.birth_cert,
                    "mode_of_entry": applicant_obj.mode_of_entry,
                    "status": applicant_obj.status,
                    "student_type": student_type
                    }
            student_obj= Student.objects.update_or_create(user__username=applicant_obj.user.username, defaults=data)
            # print(student_obj)
        applicant_obj.save()
        return Response({"details": "applicant status changed successfully"}, 200)

