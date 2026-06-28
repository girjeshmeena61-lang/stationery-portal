from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import F
from django.http import HttpResponse
from openpyxl import Workbook

from .forms import RequisitionForm
from .models import Requisition, Inventory


@login_required
def create_requisition(request):
    if request.method == 'POST':
        form = RequisitionForm(request.POST)

        if form.is_valid():
            requisition = form.save(commit=False)
            requisition.requested_by = request.user.username
            requisition.save()

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


@login_required
def view_requests(request):
    requests = Requisition.objects.filter(
        requested_by=request.user.username
    )

    status = request.GET.get('status')
    department = request.GET.get('department')

    if status:
        requests = requests.filter(status=status)

    if department:
        requests = requests.filter(department=department)

    requests = requests.order_by('-created_at')

    return render(
        request,
        'request_status.html',
        {
            'requests': requests
        }
    )


@login_required
def dashboard(request):
    total_requests = Requisition.objects.count()

    pending_requests = Requisition.objects.filter(
        status='Pending'
    ).count()

    approved_requests = Requisition.objects.filter(
        status='Approved'
    ).count()

    rejected_requests = Requisition.objects.filter(
        status='Rejected'
    ).count()

    low_stock_items = Inventory.objects.filter(
        available_qty__lte=F('minimum_qty')
    )

    low_stock_count = low_stock_items.count()

    return render(
        request,
        'dashboard.html',
        {
            'total_requests': total_requests,
            'pending_requests': pending_requests,
            'approved_requests': approved_requests,
            'rejected_requests': rejected_requests,
            'low_stock_items': low_stock_items,
            'low_stock_count': low_stock_count,
        }
    )


@login_required
def export_excel(request):
    workbook = Workbook()
    worksheet = workbook.active
    worksheet.title = "Stationery Requests"

    worksheet.append([
        'Department',
        'Employee',
        'Item',
        'Requested Quantity',
        'Approved Quantity',
        'Status',
        'Request Date'
    ])

    requisitions = Requisition.objects.all().order_by('-created_at')

    for req in requisitions:
        worksheet.append([
            req.department,
            req.requested_by,
            req.item.item_name,
            req.requested_qty,
            req.approved_qty,
            req.status,
            req.created_at.strftime('%d-%m-%Y %H:%M')
        ])

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

    response[
        'Content-Disposition'
    ] = 'attachment; filename=stationery_report.xlsx'

    workbook.save(response)

    return response