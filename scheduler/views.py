from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.views import generic
from django.utils.safestring import mark_safe
from datetime import timedelta, datetime, date
import calendar
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from users.models import Resource
from .models import Event, AddResource
from .utils import Calendar
from .forms import EventForm, AddResourceForm
from django.contrib.auth.models import User


def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split("-"))
        return date(year, month, day=1)
    return datetime.today()


def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = "month=" + str(prev_month.year) + "-" + str(prev_month.month)
    return month


def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = "month=" + str(next_month.year) + "-" + str(next_month.month)
    return month


class CalendarView(LoginRequiredMixin, generic.ListView):
    model = Event
    template_name = "calendar.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        d = get_date(self.request.GET.get("month", None))
        cal = Calendar(d.year, d.month)
        html_cal = cal.formatmonth(withyear=True)
        context["calendar"] = mark_safe(html_cal)
        context["prev_month"] = prev_month(d)
        context["next_month"] = next_month(d)
        return context


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


# need to set permission here
def event_holiday(request):
    form = EventForm(request.POST or None)
    if request.user.is_authenticated and request.POST and form.is_valid():
        description = form.cleaned_data["description"]
        start_time = form.cleaned_data["start_time"]
        end_time = form.cleaned_data["end_time"]
        Event.objects.get_or_create(

            description=description,
            start_time=start_time,
            end_time=end_time,
            defaults={'status': 2, 'title': 'Holiday'}
        )
        return HttpResponseRedirect(reverse("scheduler:calendar"))
    return render(request, "event_holiday.html", {"form": form})


class EventEdit(generic.UpdateView):
    model = Event
    fields = ["title", "description", "start_time", "end_time"]
    template_name = "event.html"


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
                "start": event.start_time.strftime("%Y-%m-%d"),
                "end": event.end_time.strftime("%Y-%m-%d"),

            }
        )
    context = {"form": forms, "events": event_list,
               "events_month": events_month, }
    return render(request, "cal_dash.html", context)


def event_details(request, id):
    event = Event.objects.get(id=id)
    eventresource = AddResource.objects.filter(event=event)
    context = {"event": event, "eventresource": eventresource}
    return render(request, "event-details.html", context)


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
                return redirect("scheduler:event_detail", event.id)
            else:
                print("--------------User limit exceed!-----------------")
    context = {"forms": forms}
    return render(request, "add_shift_resource.html", context)


def all_holiday(request):
    holidays = Event.objects.all().filter(status=2).order_by('start_time')
    return render(request, 'holiday_list.html', {'holidays': holidays})


def event(request):
    events = Event.objects.all()
    return render(request, 'events.html', {'events': events})


def deny_holiday(request, id):
    holidays = Event.objects.get(id=id)
    holidays.status = 0
    holidays.save()
    return redirect(reverse('scheduler:all_holiday'))


def accept_holiday(request, id):
    holidays = Event.objects.get(id=id)
    holidays.status = 1
    holidays.save()
    return redirect(reverse('scheduler:all_holiday'))
