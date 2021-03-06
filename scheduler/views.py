from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import Event, AddResource
from .forms import EventForm, AddResourceForm
from django.contrib.admin.views.decorators import staff_member_required
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from .serializers import EventSerializer


@login_required()
@staff_member_required()
def create_event(request):
    form = EventForm(request.POST or None)
    if request.POST and form.is_valid():
        title = form.cleaned_data["title"]
        description = form.cleaned_data["description"]
        start_time = form.cleaned_data["start_time"]
        end_time = form.cleaned_data["end_time"]
        Event.objects.get_or_create(
            title=title,
            description=description,
            start_time=start_time,
            end_time=end_time,
        )
        return HttpResponseRedirect(reverse("scheduler:calendar"))
    return render(request, "event.html", {"form": form})


@login_required()
def event_holiday(request):
    form = EventForm(request.POST or None)
    if request.user.is_authenticated and request.POST and form.is_valid():
        description = form.cleaned_data["description"]
        start_time = form.cleaned_data["start_time"]
        end_time = form.cleaned_data["end_time"]
        Event.objects.get_or_create(
            user=request.user,
            title='Holiday',
            description=description,
            start_time=start_time,
            end_time=end_time,
            defaults={'status': 2}
        )
        return HttpResponseRedirect(reverse("scheduler:calendar"))
    return render(request, "event_holiday.html", {"form": form})


@login_required()
def getcalender(request):
    forms = EventForm
    events = Event.objects.get_all_events().filter(status=1)
    events_month = Event.objects.get_running_events().filter(status=1)
    event_list = []
    # start: '2020-09-16T16:00:00'
    for event in events:
        event_list.append(
            {
                "title": event.title,
                "start": event.start_time.strftime("%Y-%m-%dT%H:%M", ),
                "end": event.end_time.strftime("%Y-%m-%dT%H:%M", ),

            }
        )
    context = {"form": forms, "events": event_list,
               "events_month": events_month, }
    return render(request, "cal_dash.html", context)


@login_required()
def event_details(request, id):
    event = Event.objects.get(id=id)
    eventresource = AddResource.objects.filter(event=event).filter(status=1)
    context = {"event": event, "eventresource": eventresource}
    return render(request, "event_details.html", context)



@staff_member_required()
@login_required()
def shift_resource(request, id):
    forms = AddResourceForm()
    if request.method == "POST":
        forms = AddResourceForm(request.POST)
        if forms.is_valid():
            member = AddResource.objects.filter(event=id)
            event = Event.objects.get(id=id)
            if member.count() <= 9:
                username = forms.cleaned_data["username"]
                AddResource.objects.create(event=event, username=username)
                return redirect("scheduler:event_details", event.id)
            else:
                print("--------------User limit exceed!-----------------")
    context = {"forms": forms}
    return render(request, "add_shift_resource.html", context)


@staff_member_required()
@login_required()
def all_holiday(request):
    holidays = Event.objects.all().filter(status=2).order_by('start_time')
    return render(request, 'holiday_list.html', {'holidays': holidays})




@staff_member_required()
@login_required()
def deny_holiday(request, id):
    holidays = Event.objects.get(id=id)
    holidays.status = 0
    holidays.save()
    return redirect(reverse('scheduler:all_holiday'))


@staff_member_required()
@login_required()
def accept_holiday(request, id):
    holidays = Event.objects.get(id=id)
    holidays.status = 1
    holidays.save()
    return redirect(reverse('scheduler:all_holiday'))


class EventListApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        events = Event.objects.all()
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
