from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import auth

from scheduler.models import AddResource, Event
from users.forms import UserLoginForm, UserRegistrationForm, ResourcesForm, AdminRegistrationForm
from django.contrib.auth.decorators import login_required
from .models import Resource
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate

from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.contrib.admin.views.decorators import staff_member_required


# Create your views here.
def index(request):
    return render(request, 'index.html')


@login_required()
def logout(request):
    auth.logout(request)
    return redirect(reverse('index'))


def login(request):
    if request.user.is_authenticated:
        return redirect(reverse('index'))
    if request.method == "POST":
        login_form = UserLoginForm(request.POST)

        if login_form.is_valid():
            user = auth.authenticate(username=request.POST['username'],
                                     password=request.POST['password'])

            if user:
                auth.login(user=user, request=request)
                return redirect(reverse('index'))
            else:
                messages.error(request, 'Your username or password is incorrect')
    else:
        login_form = UserLoginForm()
    return render(request, 'registration/login.html', {'login_form': login_form})


@staff_member_required()
@login_required()
def add_resources(request):
    if request.method == "POST":
        resource_form = ResourcesForm(request.POST)
        if resource_form.is_valid():
            resource = resource_form.save()
            return redirect(active_resources)
    else:
        resource_form = ResourcesForm()
    return render(request, 'add_resource.html', {'resource_form': resource_form})


@staff_member_required()
@login_required()
def active_resources(request):
    resources = Resource.objects.all().filter(status=1).order_by('name')

    return render(request, 'all_resources.html', {'resources': resources})


@staff_member_required()
@login_required()
def set_inactive(request, id):
    resources = Resource.objects.get(id=id)
    resources.status = 0
    resources.save()
    return redirect(reverse('active_resources'))


@staff_member_required()
@login_required()
def edit_resource(request, id=None):
    resource = get_object_or_404(Resource, id=id) if id else None
    if request.method == "POST":
        resource_form = ResourcesForm(request.POST, request.FILES, instance=resource)
        if resource_form.is_valid():
            resource = resource_form.save()
            return redirect(active_resources)
    else:
        resource_form = ResourcesForm(instance=resource)
    return render(request, 'add_resource.html', {'resource_form': resource_form})


@staff_member_required()
@login_required()
def resource_detail(request, id):
    resource_form = get_object_or_404(Resource, id=id)
    resource_form.views += 1
    resource_form.save()
    return render(request, "resource.html", {'resource_form': resource_form})


@login_required()
def signup(request, id):
    resources = Resource.objects.get(id=id)

    if request.method == 'POST':

        form = AdminRegistrationForm(request.POST)

        resources.email_sent = 1
        resources.save()
        if form.is_valid():
            user = form.save(commit=False)
            user.is_superuser = True
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Workforce Management Tool '
            message = render_to_string('acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            return HttpResponse('Email Sent')
    else:
        form = AdminRegistrationForm()
    return render(request, 'signup.html', {'form': form, 'resources': resources})


@login_required()
def signup_regular(request, id):
    resources = Resource.objects.get(id=id)
    resources.email_sent = 1
    resources.save()
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)

            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Workforce Management Tool '
            message = render_to_string('acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            return HttpResponse('Email Sent')
    else:
        form = UserRegistrationForm()
    return render(request, 'signup.html', {'form': form, 'resources': resources})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        # return redirect('home')
        return HttpResponse('Activation link is invalid!')
    else:
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')


@staff_member_required()
@login_required()
def get_shifts(request):
    events = Event.objects.all().filter(user=request.user).filter(title='Holiday')
    return render(request, 'profile.html', {'events': events})
