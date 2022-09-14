from django.forms import ModelForm
from .models import ShippingDetails


class ShippingDetailsForm(ModelForm):
    class Meta:
        model = ShippingDetails
        fields = '__all__'