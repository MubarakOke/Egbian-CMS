from django.urls import path
from accounts.views import AuthenticateApplicantView, AuthenticateStudentView, AuthenticateAdminView

app_name= 'accounts'

urlpatterns = [
    path('auth/applicant/', AuthenticateApplicantView.as_view(), name='auth_applicant'),
    path('auth/student/', AuthenticateStudentView.as_view(), name='auth_student'),
    path('auth/staff/admin/', AuthenticateAdminView.as_view(), name='auth_admin')
]