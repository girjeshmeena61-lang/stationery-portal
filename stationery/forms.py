from django import forms
from .models import Requisition


class RequisitionForm(forms.ModelForm):

    class Meta:
        model = Requisition
        fields = ['department', 'item', 'requested_qty', 'reason']

    def clean_requested_qty(self):
        requested_qty = self.cleaned_data.get('requested_qty')
        item = self.cleaned_data.get('item')

        # Quantity must be greater than zero
        if requested_qty is None or requested_qty <= 0:
            raise forms.ValidationError(
                "Quantity must be greater than zero."
            )

        # Item must be selected
        if not item:
            return requested_qty

        # Item completely out of stock
        if item.available_qty == 0:
            raise forms.ValidationError(
                f"{item.item_name} is currently out of stock."
            )

        # Requested quantity exceeds available stock
        if requested_qty > item.available_qty:
            raise forms.ValidationError(
                f"Requested quantity ({requested_qty}) exceeds available stock ({item.available_qty})."
            )

        # Check minimum stock
        remaining_stock = item.available_qty - requested_qty

        if remaining_stock < item.minimum_qty:
            raise forms.ValidationError(
                f"Request cannot be submitted because only {remaining_stock} items would remain, which is below the minimum stock level ({item.minimum_qty}). Maximum you can request is {item.available_qty - item.minimum_qty}."
            )

        return requested_qty