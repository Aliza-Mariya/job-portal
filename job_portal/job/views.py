from django.contrib import messages, auth
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import render, redirect

from job.forms import RegisterForm, JobForm
from job.models import Job, JobApplication, User

# Create your views here.
from django.shortcuts import render, redirect


def home(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('admin_home')
        else:
            return redirect('user_home')

    return render(request, 'home.html')


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, "Registration successful")
            return redirect('login')
    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            if user.is_superuser:
                return redirect('admin_home')
            else:
                return redirect('user_home')
        else:
            messages.error(request, "Invalid email or password")
    return render(request, 'login.html')


def view_job_list(request):
    jobs = Job.objects.filter(is_active=True)
    return render(request, 'view_job_list.html', {'jobs': jobs})


@login_required
def apply_job(request, job_id):
    job = Job.objects.get(id=job_id)

    JobApplication.objects.get_or_create(
        job=job,
        user=request.user
    )
    messages.success(request, "Applied successfully")
    return redirect('job_list')


def add_job(request):
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('job_list')
    else:
        form = JobForm()
    return render(request, 'add_job.html', {'form': form})


@login_required()
def logout(request):
    auth.logout(request)
    return redirect('home')


@login_required()
def admin_home(request):
    if not request.user.is_superuser:
        return redirect('home')

    context = {
        'jobs_count': Job.objects.count(),
        'users_count': User.objects.filter(is_superuser=False).count(),
        'applications_count': JobApplication.objects.count(),
    }
    return render(request, 'admin_home.html', context)


@login_required()
def user_home(request):
    return render(request, 'user_home.html')


def job_list(request):
    jobs = Job.objects.filter(is_active=True)

    # For admin: annotate application count
    if request.user.is_staff:
        jobs = jobs.annotate(app_count=Count('applications'))
    else:
        jobs = jobs

    applied_jobs = []
    if request.user.is_authenticated and not request.user.is_staff:
        applied_jobs = JobApplication.objects.filter(
            user=request.user
        ).values_list('job_id', flat=True)

    return render(request, 'job_list.html', {
        'jobs': jobs,
        'applied_jobs': applied_jobs
    })
