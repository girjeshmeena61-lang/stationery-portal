from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.db.models import F
from django.http import HttpResponse
from openpyxl import Workbook

from .forms import RequisitionForm
from .models import Requisition, Inventory


@login_required
from django.contrib import messages

@login_required
def create_requisition(request):
    if request.method == 'POST':
        form = RequisitionForm(request.POST)

        if form.is_valid():

            requisition = form.save(commit=False)

            inventory = requisition.item
            qty = requisition.requested_qty

            # Quantity must be greater than zero
            if qty <= 0:
                messages.error(request, "Quantity must be greater than zero.")
                return render(request, 'requisition_form.html', {'form': form})

            # No stock available
            if inventory.available_qty == 0:
                messages.error(request, f"{inventory.item_name} is currently out of stock.")
                return render(request, 'requisition_form.html', {'form': form})

            # Requested quantity exceeds stock
            if qty > inventory.available_qty:
                messages.error(
                    request,
                    f"Requested quantity ({qty}) exceeds available stock ({inventory.available_qty})."
                )
                return render(request, 'requisition_form.html', {'form': form})

            # Minimum stock check
            remaining_stock = inventory.available_qty - qty

            if remaining_stock < inventory.minimum_qty:
                messages.warning(
                    request,
                    f"Request cannot be submitted. Remaining stock will become {remaining_stock}, which is below the minimum stock level ({inventory.minimum_qty})."
                )
                return render(request, 'requisition_form.html', {'form': form})

            requisition.requested_by = request.user.username
            requisition.save()

            messages.success(request, "Request submitted successfully.")

            return render(
                request,
                'requisition_form.html',
                {
                    'form': RequisitionForm(),
                    'success': True
                }
            )

    else:
        form = RequisitionForm()

    return render(
        request,
        'requisition_form.html',
        {
            'form': form
        }
    )