from django.shortcuts import render, redirect,get_object_or_404,HttpResponse
from django.contrib import messages
from .form import ApplicantForm,RecruitmentApplicationForm,JobApplicationForm
from .models import Applicant,RecruitmentApplication,JobApplication,HR
from ManagerApp.models import RecruitmentRequest
from django.db.models import Q
from django.utils import timezone
from django.contrib.auth.decorators import login_required
def CareerPage(request,application_id):
    Jobdetails = JobApplication.objects.get(ApplicationID=application_id)
    if request.method == 'POST':
        form = ApplicantForm(request.POST, request.FILES)

        if form.is_valid():
            applicant=form.save()
            recruitment_application = Jobdetails.recruitmentapplication_set.create(
                ApplicantID=applicant,
                ApplicationDate=timezone.now(),
                Status='None'
            )
            messages.success(request, 'Your application has been submitted successfully!')
            return redirect("/home")
    else:
        form = ApplicantForm()
        
    content={
        'job_application': Jobdetails,
        'form': form
    }
    return render(request, 'CareerPage.html', content)


def home(request):
    Jobdetails = JobApplication.objects.all()
    # recruitmentdetails=RecruitmentApplication.objects.all()
    context = {
        'Jobdetails': Jobdetails,
    }
    return render(request, 'index.html', context)

def HrDashboard(request):
    username = request.session.get('username')
    if not username:
        return HttpResponse("Session expired or not logged in.")
    try:
        Hr = HR.objects.get(Username=username)
    except HR.DoesNotExist:
        return HttpResponse("Manager does not exist.")
    applicants = Applicant.objects.all()
    recruit_count=RecruitmentRequest.objects.all().count()
    applicant_count = applicants.count()
    if request.method == 'POST':
        if 'approve' in request.POST:
            redirect ("/createrecruitment")
    
    
    context = {
        'applicants': applicants,
        'applicant_count': applicant_count ,
        'recruit_count':recruit_count,
        'hr':Hr
    }
    return render(request, 'Hr/hr_dashboard.html', context)

def ApplicantList(request):
    # applicant_ids=RecruitmentApplication.objects.filter(~Q(Status='Approved') & ~Q(Status='Pending')).values_list('ApplicantID', flat=True)
    # applicants = Applicant.objects.filter(ApplicantID__in=applicant_ids)
    username = request.session.get('username')
    if not username:
        return HttpResponse("Session expired or not logged in.")
    try:
        Hr = HR.objects.get(Username=username)
    except HR.DoesNotExist:
        return HttpResponse("Manager does not exist.")
    applicants = Applicant.objects.all()
    Recruitment=RecruitmentApplication.objects.all()
    context = {
        'applicants': applicants,
        'recruitment':Recruitment,
        'hr':Hr
        
    }
    return render(request, 'Hr/hr_applicant.html', context)


def update_status(request, applicant_id):
    username = request.session.get('username')
    if not username:
        return HttpResponse("Session expired or not logged in.")
    try:
        Hr = HR.objects.get(Username=username)
    except HR.DoesNotExist:
        return HttpResponse("Manager does not exist.")
    
    
    applicant = get_object_or_404(Applicant, ApplicantID=applicant_id)
    if 'reject' in request.POST:
        applicant.status = 'Rejected'
        applicant.delete()
        return redirect('/applicantnoti')



def create_recruitment_application(request, applicant_id):
    username = request.session.get('username')
    if not username:
        return HttpResponse("Session expired or not logged in.")
    
    try:
        hr = HR.objects.get(Username=username)
    except HR.DoesNotExist:
        return HttpResponse("HR does not exist.")

    applicant = Applicant.objects.get(pk=applicant_id)
    recruitment_application, created = RecruitmentApplication.objects.get_or_create(ApplicantID=applicant)

    if request.method == 'POST':
        form = RecruitmentApplicationForm(request.POST, instance=recruitment_application)
        if form.is_valid():
            form.save()
            return redirect('/applicantnoti')  # Redirect to a page displaying a list of recruitment applications
    else:
        form = RecruitmentApplicationForm(instance=recruitment_application)
        
    context = {
        'form': form,
        'hr': hr
    }
    return render(request, 'Hr/hr_recruit.html', context)

def recruitment_request_detail(request):
    username = request.session.get('username')
    if not username:
        return HttpResponse("Session expired or not logged in.")
    try:
        Hr = HR.objects.get(Username=username)
    except HR.DoesNotExist:
        return HttpResponse("Manager does not exist.")
    recruitment_request = RecruitmentRequest.objects.filter(HRID=Hr)
    
    context = {
        'recruitment_request': recruitment_request,
        'hr':Hr
    }
    return render(request, 'Hr/hr_Request.html', context)








def JobApplications(request,request_id):
    username = request.session.get('username')
    if not username:
        return HttpResponse("Session expired or not logged in.")
    try:
        Hr = HR.objects.get(Username=username)
    except HR.DoesNotExist:
        return HttpResponse("Manager does not exist.")

    recruitment_request = RecruitmentRequest.objects.get(RequestID=request_id)
    if request.method == 'POST':
        form = JobApplicationForm(request.POST)
        if form.is_valid():
            job_application = form.save(commit=False)
            job_application.RequestID = recruitment_request
            job_application.save()
            return redirect('/recruitmentRequest')  # Redirect to a success page
    else:
        form = JobApplicationForm()
        
        
    context={
        'form': form,
         'hr':Hr
        }
    return render(request, 'Hr/hr_createjob.html', context)