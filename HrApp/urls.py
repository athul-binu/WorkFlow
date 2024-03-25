from django.urls import path
from HrApp import views



urlpatterns = [
    path('home/', views.home, name='home'),
    path('HrDashboard/', views.HrDashboard, name='Dashboard'),
    path('applicantnoti/', views.ApplicantList, name='applicantnoti'),
    path('updatestatus/<int:applicant_id>', views.update_status, name='update_status'),
    path('createrecruitment/<int:applicant_id>', views.create_recruitment_application, name='create_recruitment_application'),
    path('CareerPage/<int:application_id>', views.CareerPage, name='CareerPage'),
    path('recruitmentRequest/', views.recruitment_request_detail, name='recruitment_request_detail'), 
    path('createJobApplication/<int:request_id>', views.JobApplications, name='create_job_application'), 
]
