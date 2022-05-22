from datetime import datetime
from django.db import models
from django.urls import reverse
from users.models import Resource


class EventAbstract(models.Model):
    """ Event abstract model """

    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class EventManager(models.Manager):
    """ Event manager """

    def get_all_events(self):
        events = Event.objects.filter(is_active=True, is_deleted=False)
        return events

    def get_running_events(self):
        running_events = Event.objects.filter(
            is_active=True,
            is_deleted=False,
            end_time__gte=datetime.now().date(),
        ).order_by("start_time")
        return running_events


class Event(EventAbstract):
    """ Event model """
    SHIFTS = [
        ('Early', "E"),
        ('Middle', "M"),
        ('Late', "L"),
        ('Holiday', "H"),
        ('Bank Holiday', "BH"),
        ('', "")
    ]

    username = models.ForeignKey(
        Resource, on_delete=models.CASCADE, blank=True, null=True
    )
    user = models.CharField(max_length=200, default='')
    status = models.IntegerField(default=1)
    title = models.CharField(max_length=30, choices=SHIFTS, default='')
    description = models.TextField()
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)

    objects = EventManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("scheduler:event-detail", args=(self.id,))

    @property
    def get_html_url(self):
        url = reverse("scheduler:event-detail", args=(self.id,))
        return f'<a href="{url}"> {self.title} </a>'


class AddResource(EventAbstract):
    """ Event member model """

    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="events")
    username = models.ForeignKey(
        Resource, on_delete=models.CASCADE, blank=True, null=True, related_name="event_members"
    )

    def __str__(self):
        return str(self.username)

