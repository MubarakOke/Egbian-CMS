from django.urls import path
from accounts.views import AuthenticateApplicantView, AuthenticateStudentView

app_name= 'accounts'

urlpatterns = [
    path('auth/applicant/', AuthenticateApplicantView.as_view(), name='auth_applicant'),
    path('auth/student/', AuthenticateStudentView.as_view(), name='auth_student')
]