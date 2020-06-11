from django.forms import DateInput
from hire.models import HireRequest, Event
from django import forms


class HireForm(forms.ModelForm):
    class Meta:
        model = HireRequest
        # date is a HTML5 input type, format to make date show on fields
        format = '%Y-%m-%d'
        widgets = {
            'hire_from': DateInput(attrs={'type': 'date'}, format=format),
            'hire_to': DateInput(attrs={'type': 'date'}, format=format),
        }
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(HireForm, self).__init__(*args, **kwargs)
        frmt = '%Y-%m-%d'
        # input_formats parses HTML5 datetime-local input to datetime field
        self.fields['hire_from'].input_formats = (frmt,)
        self.fields['hire_to'].input_formats = (frmt,)
        self.fields['is_hidden'].widget = forms.HiddenInput()
        self.fields['colour'].widget = forms.HiddenInput()


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        format = '%Y-%m-%d'

        widgets = {
            'event_from': DateInput(attrs={'type': 'date'}, format=format),
            'event_to': DateInput(attrs={'type': 'date'}, format=format)
        }

        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        frmt = '%Y-%m-%d'

        self.fields['event_from'].input_formats = (frmt,)
        self.fields['event_to'].input_formats = (frmt,)
        self.fields['is_hidden'].widget = forms.HiddenInput()
        self.fields['colour'].widget = forms.HiddenInput()
