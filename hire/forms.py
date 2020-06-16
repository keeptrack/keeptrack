from django import forms
from .models import HireRequest


# Use HTML5 <input type='date'>
class DateInput(forms.DateInput):
    input_type = 'date'


class HireForm(forms.ModelForm):
    class Meta:
        model = HireRequest
        fields = '__all__'
        exclude = ['approved', 'rejected', 'for_csp', 'discounted_price', 'is_hidden', 'colour']
        labels = {'cid': 'CID'}
        widgets = {'hire_from': DateInput, 'hire_to': DateInput}

    def clean(self):
        cleaned_data = super().clean()
        hire_from = cleaned_data.get('hire_from')
        hire_to = cleaned_data.get('hire_to')

        if hire_from and hire_to:
            if hire_from > hire_to:
                msg = forms.ValidationError("Select a valid date range.")
                self.add_error('hire_from', msg)
                self.add_error('hire_to', msg)
