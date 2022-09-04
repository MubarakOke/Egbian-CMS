from rest_framework.response import Response
from rest_framework.generics import ListAPIView, RetrieveAPIView, UpdateAPIView, CreateAPIView, GenericAPIView
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin, DestroyModelMixin, ListModelMixin
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from rest_framework.views import APIView
from django.conf import settings
from operations.renderers import DefaultRenderer
from operations.models import Applicant, Session, Staff, Role, Department, Faculty, Course, CourseRegistration, CourseRequirement, Result, Payment, Fee
from operations import serializers
from rest_framework.response import Response
from operations.utils import EmailThread
from django.core.mail import send_mail
from django.db.models import Q, F

from .models import Role, Student, Department, Session, Applicant, CourseRegistrationStatus, CourseRegistration

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
                return self.queryset.filter(Q(session__start_year=q) & Q(is_admitted=False))
                
        try:
            session_obj= Session.objects.get(current_session=True)
        except:
            return ""
        return self.queryset.filter(Q(session=session_obj) & Q(is_admitted=False))

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

class StaffDetailView(UpdateModelMixin, DestroyModelMixin, RetrieveAPIView):
    parser_classes = (JSONParser, MultiPartParser, FormParser)
    renderer_classes= [DefaultRenderer]
    serializer_class= serializers.StaffUpdateSerializer
    queryset= Staff.objects.all()
    permission_classes= []
    lookup_field= 'id'

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
    def patch(self, request, *args, **kwargs):
        return self.update(request, *args, kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

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
    serializer_class= serializers.CourseCreateListUpdateSerializer
    queryset= Course.objects.all()
    permission_classes= []

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class CourseDetailView(UpdateModelMixin, DestroyModelMixin, RetrieveAPIView):
    parser_classes = (JSONParser, MultiPartParser, FormParser)
    renderer_classes= [DefaultRenderer]
    serializer_class= serializers.CourseCreateListUpdateSerializer
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
            return Response({"Error": "user is not a student"}, 404)

        try:
                session_obj= Session.objects.get(current_session=True)
        except:
                raise serializers.ValidationError({"details":"Session not set"})

        registration_status= student_obj.courseregistrationstatus.filter(Q(session=session_obj) & Q(status=True))
        if registration_status:
            registered_courses=  CourseRegistration.objects.filter(Q(student=student_obj) & Q(session=session_obj)).select_related("course").values(
                                                                                                                                                    course_name=F("course__course_name"),  
                                                                                                                                                    course_code=F("course__course_code"),
                                                                                                                                                    level=F("course__level"),
                                                                                                                                                    course_unit=F("course__course_unit"),
                                                                                                                                                    compulsory=F("course__compulsory"),
                                                                                                                                                    department=F("course__department"),
                                                                                                                                                    semester=F("course__semester")
                                                                                                                                                    )

            course_registered_first= registered_courses.filter(course__semester="first")
            course_registered_second= registered_courses.filter(course__semester="second")
            return Response({"status":"registered",
                            "details": {
                                    "course_registered_first": course_registered_first,
                                    "course_registered_second": course_registered_second,
                                    }})

        course_requirement_obj= CourseRequirement.objects.filter(Q(level=student_obj.level) & Q(department=student_obj.department)).order_by('semester')
        course_requirement_obj_first= course_requirement_obj[0]
        course_requirement_obj_second= course_requirement_obj[1]
        course_objs= Course.objects.filter(Q(level=student_obj.level) & Q(department=student_obj.department))
        course_list_first= course_objs.filter(Q(semester="first"))
        course_list_second= course_objs.filter(Q(semester="second"))

        
        return Response({"status":"unregistered",
                        "details": {
                                    "requirement_first": serializers.CourseRequirementCreateListSerializer(course_requirement_obj_first).data,
                                    "course_first":serializers.CourseCreateListSerializer(course_list_first, many=True).data,
                                    "requirement_second": serializers.CourseRequirementCreateListSerializer(course_requirement_obj_second).data,
                                    "course_second": serializers.CourseCreateListSerializer(course_list_second, many=True).data,
                                    }})

class CourseWareView(APIView):
    parser_classes = (JSONParser, MultiPartParser, FormParser)
    renderer_classes= [DefaultRenderer]
    permission_classes= []

    def get(self, request, *args, **kwargs):
        try:
            student_obj= request.user.student
        except:
            return Response({"Error": "user is not a student"}, 404)

        course_ware= Course.objects.filter(Q(department=student_obj.department))
        course_ware_first= course_ware.filter(Q(semester="first"))
        course_ware_second= course_ware.filter(Q(semester="second"))
        
        return Response({"details": {
                                    "course_ware_first": serializers.CourseCreateListSerializer(course_ware_first, many=True).data,
                                    "course_ware_second": serializers.CourseCreateListSerializer(course_ware_second, many=True).data,
                                    }})


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
            level=100
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
                    "student_type": student_type,
                    "next_kin_name": applicant_obj.next_kin_name,
                    "next_kin_relationship": applicant_obj.next_kin_relationship,
                    "next_kin_email": applicant_obj.next_kin_email,
                    "next_kin_address": applicant_obj.next_kin_address,
                    "next_kin_phone": applicant_obj.next_kin_phone,
                    "secondary_cert": applicant_obj.secondary_cert,
                    "testimonial": applicant_obj.testimonial
                    }
            student_obj, created= Student.objects.update_or_create(user__username=applicant_obj.user.username, defaults=data)
            try:
                subject= 'Admission Offer'
                message= f'Dear {student_obj.last_name} {student_obj.first_name} {student_obj.middle_name}, \nCongratulation on your admission into Egbian College of Health Science, We are glad to have you on, Use your appliacant details to access your student portal\n \n \nAccount ID: {student_obj.user.username} \n \n \nPlease do not reply to this email. This email is not monitored'
                from_email= settings.EMAIL_HOST_USER
                recipient_list= [student_obj.email]
                fail_silently=False
                # Sending email on a new thread
                send_mail(subject, message, from_email, recipient_list, fail_silently)
            except:
                student_obj.delete()
                raise serializers.ValidationError({"details":"email not sent"})
            # print(student_obj)
        applicant_obj.save()
        return Response({"details": "applicant status changed successfully"}, 200)


class TuitionPaymentView(APIView):
    parser_classes = (JSONParser, MultiPartParser, FormParser)
    renderer_classes= [DefaultRenderer]
    permission_classes= []

    def get(self, request, *args, **kwargs):
        try:
            student_obj= request.user.student
        except:
            return Response({"Error": "user is not a student"}, 404)
        
        try:
            session_obj= Session.objects.get(current_session=True)
        except:
            return Response({"Error": "Session not set"}, 404)
        
        get_tuition_payment= Payment.objects.filter(Q(student=student_obj) & Q(session=session_obj))
        if get_tuition_payment:
            return Response({"status": "paid",
                             "details": serializers.PaymentSerializer(get_tuition_payment)}, 200)
        # fee_obj= Fee.objects.get(Q(name="tuition") & Q(session=))


        

















# class CourseToRegisterView(APIView):
#     parser_classes = (JSONParser, MultiPartParser, FormParser)
#     renderer_classes= [DefaultRenderer]
#     permission_classes= []

#     def get(self, request, *args, **kwargs):
#         try:
#             student_obj= request.user.student
#         except:
#             return Response({"detail": "user is not a student"}, 404)
#         course_requirement_obj= CourseRequirement.objects.filter(Q(level=student_obj.level) & Q(department=student_obj.department)).order_by('semester')
#         course_requirement_obj_first= course_requirement_obj[0]
#         course_requirement_obj_second= course_requirement_obj[1]
#         course_objs= Course.objects.filter(Q(level=student_obj.level) & Q(department=student_obj.department))
#         course_list_first= []
#         course_list_second= []
#         carried_over_courses= result_for_course= Result.objects.filter(Q(score_lt=40) & Q(student= request.user.student)).latest()
#         for course in course_objs:
#             if course.prerequsite_for:
#                 prerequsite_course_obj= Course.objects.filter(prerequsite_for=course.prerequsite_for).first()
#                 # try:
#                 #     result_for_course= Result.objects.filter(Q(course=prerequsite_course_obj) & Q(student= request.user.student)).latest()
#                 # except:
#                 #     return Response({"details":"no result of prerequsite course"})
#                 result_for_course= Result.objects.filter(Q(course=prerequsite_course_obj) & Q(student= request.user.student)).latest()
#                 if not result_for_course:
#                     if prerequsite_course_obj.semester.lower() == "first":
#                         course_list_first.append(prerequsite_course_obj)
#                     else:
#                         course_list_second.append(prerequsite_course_obj)
#                 elif result_for_course.score < 40.0:
#                     if prerequsite_course_obj.semester.lower() == "first":
#                         course_list_first.append(prerequsite_course_obj)
#                     else:
#                         course_list_second.append(prerequsite_course_obj)
#                 else:
#                     if prerequsite_course_obj.semester.lower() == "first":
#                         course_list_first.append(course)
#                     else:
#                         course_list_second.append(course)
#             else:
#                 if course.semester.lower() == "first":
#                     course_list_first.append(course)
#                 else:
#                     course_list_second.append(course)
#         return Response({"details": {
#                                     "requirement_first": serializers.CourseRequirementCreateListSerializer(course_requirement_obj_first).data,
#                                     "courses_first":serializers.CourseCreateListSerializer(course_list_first, many=True).data,
#                                     "requirement_second": serializers.CourseRequirementCreateListSerializer(course_requirement_obj_second).data,
#                                     "courses_second": serializers.CourseCreateListSerializer(course_list_second, many=True).data
#                                     }})