from django.urls import path

from . import views

app_name = "scheduler"


urlpatterns = [
    path("calender/", views.getcalender, name="calendar"),
    path("calenders/", views.CalendarView.as_view(), name="calendars"),
    path("event/new/", views.create_event, name="event_new"),
    path("event_details/<int:id>/", views.event_details, name="event_details"),
    path("shift_resource/<int:id>", views.shift_resource, name="shift_resource"),
    path("holiday_list/", views.all_holiday, name="all_holiday"),
    path("event_holiday/", views.event_holiday, name="event_holiday"),
    path("deny/<int:id>", views.deny_holiday, name="deny_holiday"),
    path("accept/<int:id>", views.accept_holiday, name="accept_holiday"),
    path("event/", views.event, name="event"),

]