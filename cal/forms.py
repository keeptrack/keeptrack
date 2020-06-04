from django.forms import ModelForm, DateInput
from hire.models import HireRequest


class EventForm(ModelForm):
    class Meta:
        model = HireRequest
        # datetime-local is a HTML5 input type, format to make date time show on fields
        widgets = {
            'hire_from': DateInput(attrs={'type': 'date'}, format='%Y-%m-%dT'),
            'hire_to': DateInput(attrs={'type': 'date'}, format='%Y-%m-%dT'),
        }
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        # input_formats parses HTML5 datetime-local input to datetime field
        self.fields['hire_from'].input_formats = ('%Y-%m-%dT',)
        self.fields['hire_to'].input_formats = ('%Y-%m-%dT',)
