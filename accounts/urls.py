from django.urls import path
from accounts.views import AuthenticateApplicantView

app_name= 'accounts'

urlpatterns = [
    path('auth/applicant/', AuthenticateApplicantView.as_view(), name='auth_applicant')
]