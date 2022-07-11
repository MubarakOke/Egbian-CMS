from django.urls import path
from operations.views import (DashboardView, SessionCreateListView, RoleCreateListView, RoleDetailView,
                            StaffCreateListView, FacultyCreateListView, FacultyDetailView, DepartmentCreateListView, DepartmentDetailView,
                            ApplicantCreateView, ApplicantUpdateView)

app_name= 'operations'

urlpatterns = [
    # Session URL
    path('session/', SessionCreateListView.as_view(), name='create_list_session'),
    # Applicant URL
    path('applicant/', ApplicantCreateView.as_view(), name='create_applicant'),
    path('applicant/<int:id>/', ApplicantUpdateView.as_view(), name='update_applicant'),
    # Staff
    path('staff/', StaffCreateListView.as_view(), name='create_list_staff'),
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
]