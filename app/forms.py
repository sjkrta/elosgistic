from django.forms import ModelForm, DateInput
from .models import ShippingDetails, SupportQuery

class DateInput(DateInput):
    input_type = 'date'

class ShippingDetailsForm(ModelForm):
    class Meta:
        model = ShippingDetails
        fields = '__all__'
        widgets = {
            'date': DateInput()
        }

class SupportQueryForm(ModelForm):
    class Meta:
        model = SupportQuery
        fields = '__all__'