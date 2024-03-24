from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import messages
from .form import ApplicantForm,RecruitmentApplicationForm
from .models import Applicant,RecruitmentApplication,JobApplication
from django.db.models import Q
def CareerPage(request,application_id):
    Jobdetails = JobApplication.objects.get(ApplicationID=application_id)
    print(Jobdetails)
    if request.method == 'POST':
        form = ApplicantForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
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
    applicants = Applicant.objects.all()
    applicant_count = applicants.count()
    if request.method == 'POST':
        if 'approve' in request.POST:
            redirect ("/createrecruitment")
    
    
    context = {
        'applicants': applicants,
        'applicant_count': applicant_count 
    }
    return render(request, 'Hr/hr_dashboard.html', context)

def ApplicantList(request):
    applicant_ids=RecruitmentApplication.objects.filter(~Q(Status='Approved') & ~Q(Status='Pending')).values_list('ApplicantID', flat=True)
    applicants = Applicant.objects.filter(ApplicantID__in=applicant_ids)
    context = {
        'applicants': applicants,
    }
    return render(request, 'Hr/hr_applicant.html', context)


def update_status(request, applicant_id):
    applicant = get_object_or_404(Applicant, ApplicantID=applicant_id)
    if 'reject' in request.POST:
        applicant.status = 'Rejected'
        applicant.delete()
        return redirect('/applicantnoti')



def create_recruitment_application(request, applicant_id):
    if request.method == 'POST':
        form = RecruitmentApplicationForm(request.POST)
        if form.is_valid():
            applicantname = Applicant.objects.get(pk=applicant_id)
            recruitment_application = form.save(commit=False)
            recruitment_application.ApplicantID = applicantname
            recruitment_application.save()
            return redirect('/applicantnoti')  # Redirect to a page displaying a list of recruitment applications
    else:
        form = RecruitmentApplicationForm()
        
    context = {
        'form': form,
    }
    return render(request, 'Hr/hr_recruit.html', context)