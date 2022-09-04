from django.urls import path
from operations.views import (DashboardView, SessionCreateListView, RoleCreateListView, RoleDetailView,
                            StaffCreateListView, StaffDetailView, FacultyCreateListView, FacultyDetailView, DepartmentCreateListView, DepartmentDetailView,
                            ApplicantCreateListView, ApplicantUpdateView, ApplicantStatusChangeView,
                            StudentCreateListView, StudentDetailView,
                            CourseCreateListView, CourseDetailView,
                            CourseRequirementCreateListView, CourseRequirementdetailView,
                            CourseRegistrationListCreateView, CourseToRegisterView, CourseWareView,)

app_name= 'operations'

urlpatterns = [
    # Session URL
    path('session/', SessionCreateListView.as_view(), name='create_list_session'),
    # Applicant URL
    path('applicant/', ApplicantCreateListView.as_view(), name='create_applicant'),
    path('applicant/<int:id>/', ApplicantUpdateView.as_view(), name='update_applicant'),
    path('applicant/update/<int:id>/', ApplicantStatusChangeView.as_view(), name='update_status_applicant'),
    # student
    path('student/', StudentCreateListView.as_view(), name='create_list_student'),
    path('student/<int:id>/', StudentDetailView.as_view(), name='detail_student'),
    # Staff
    path('staff/', StaffCreateListView.as_view(), name='create_list_staff'),
    path('staff/<int:id>/', StaffDetailView.as_view(), name='detail_staff'),
    # Dashboard
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    # Role
    path('role/', RoleCreateListView.as_view(), name='create_role'),
    path('role/<int:id>/', RoleDetailView.as_view(), name='detail_role'),
    # Faculty
    path('faculty/', FacultyCreateListView.as_view(), name='create_faculty'),
    path('faculty/<int:id>/', FacultyDetailView.as_view(), name='detail_faculty'),
    # Department
    path('department/', DepartmentCreateListView.as_view(), name='create_department'),
    path('department/<int:id>/', DepartmentDetailView.as_view(), name='detail_department'),
    # Course
    path('course/', CourseCreateListView.as_view(), name='create_course'),
    path('course/<int:id>/', CourseDetailView.as_view(), name='create_detail'),
    # Course requirement
    path('course/requirement/', CourseRequirementCreateListView.as_view(), name='create_requirement_course'),
    path('course/requirement/<int:id>/', CourseRequirementdetailView.as_view(), name='detail_requirement_detail'),
    # Course Registration
    path('course/registration/', CourseRegistrationListCreateView.as_view(), name='create_registration_course'),
    path('course/registration/info/', CourseToRegisterView.as_view(), name='create_registration_course'),
    # Course Wares
    path('courseware/', CourseWareView.as_view(), name='course_wares'),

]