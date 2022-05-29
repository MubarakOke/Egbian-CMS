from django.urls import path
from operations.views import (SessionCreateListView,
                    ApplicantCreateView, ApplicantUpdateView)

app_name= 'operations'

urlpatterns = [
    # Session URL
    path('session/', SessionCreateListView.as_view(), name='create_session'),
    # Applicant URL
    path('applicant/', ApplicantCreateView.as_view(), name='create_applicant'),
    path('update/<id>/', ApplicantUpdateView.as_view(), name='update_applicant')
]