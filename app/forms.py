from django.forms import ModelForm, DateInput
from .models import ShippingDetails

class DateInput(DateInput):
    input_type = 'date'

class ShippingDetailsForm(ModelForm):
    class Meta:
        model = ShippingDetails
        fields = '__all__'
        widgets = {
            'date': DateInput()
        }