from django.forms import ModelForm, DateInput, SelectMultiple
from .models import Event, AddResource
from django import forms


class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = ["title" ,"description", "start_time", "end_time"]
        # datetime-local is a HTML5 input type
        widgets = {
            "description": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter shift description",
                }
            ),
            "start_time": DateInput(
                attrs={"type": "datetime-local", "class": "form-control"},
                format="%Y-%m-%dT%H:%M",
            ),
            "end_time": DateInput(
                attrs={"type": "datetime-local", "class": "form-control"},
                format="%Y-%m-%dT%H:%M",
            ),
        }

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        # input_formats to parse HTML5 datetime-local input to datetime field
        self.fields["start_time"].input_formats = ("%Y-%m-%dT%H:%M",)
        self.fields["end_time"].input_formats = ("%Y-%m-%dT%H:%M",)


class AddResourceForm(forms.ModelForm):
    # this would use widget 'SelectMultiple' by default
    class Meta:
        model = AddResource
        fields = ["username"]