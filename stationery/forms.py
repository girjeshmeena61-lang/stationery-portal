from django import forms
from .models import Requisition

class RequisitionForm(forms.ModelForm):
    class Meta:
        model = Requisition
        fields = ['department', 'item', 'requested_qty', 'reason']

    def clean_requested_qty(self):
        requested_qty = self.cleaned_data['requested_qty']
        item = self.cleaned_data.get('item')

        if item:
            max_allowed = item.available_qty - item.minimum_qty

            if requested_qty > max_allowed:
                raise forms.ValidationError(
    "Requested quantity exceeds available stock."
)

        return requested_qty