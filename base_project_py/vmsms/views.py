from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse
from django.http import JsonResponse
from .forms import (
    LoginForm, AdminRegistrationForm, ReceptionistRegistrationForm, MechanicRegistrationForm,
    InventoryManagerRegistrationForm, CustomerRegistrationForm, AppointmentForm, TestForm, TestResultForm, InvoiceForm, VehicleForm, TestUpdateForm, RepairApprovalForm,
    AdminProfileForm, ReceptionistProfileForm, MechanicProfileForm, InventoryManagerProfileForm, CustomerProfileForm, TestCreateForm, DiagnoseTestForm, SuggestRepairForm, ChangePasswordForm
)
from .backends import VMSMSBackend
from django.http import HttpResponse
from .models import Appointment, Mechanic, Vehicle, Customer, Test, TestResult, Repair, MechanicSchedule, Admin, Receptionist, InventoryManager, Invoices
from django.db.models import Sum, F, FloatField, ExpressionWrapper, Q, Count
import matplotlib.pyplot as plt
import io
import base64
import datetime
from decimal import Decimal

# Create your views here.

# Login view

def login_view(request):
    # Check if user is already logged in
    if request.session.get('user_id'):
        user_type = request.session.get('user_type')
        return redirect(f'vmsms:{user_type}_dashboard')
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            # Try to authenticate with each user type
            backend = VMSMSBackend()
            user_types = ['admin', 'receptionist', 'mechanic', 'inventory_manager', 'customer']
            user = None
            user_type = None
            
            for ut in user_types:
                user = backend.authenticate(request, username=username, password=password, user_type=ut)
                if user:
                    user_type = ut
                    break
            
            if user:
                # Set session
                request.session['user_id'] = user.id
                request.session['user_type'] = user_type
                request.session['username'] = user.username
                # Redirect to dashboard
                return redirect(reverse(f'vmsms:{user_type}_dashboard'))
            else:
                messages.error(request, 'Invalid username or password')
    else:
        form = LoginForm()
    return render(request, 'vmsms/login.html', {'form': form})

# Example dashboards (to be implemented)
def admin_dashboard(request):
    return render(request, 'vmsms/admin_dashboard.html')
def receptionist_dashboard(request):
    return render(request, 'vmsms/receptionist_dashboard.html')
def mechanic_dashboard(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('vmsms:login')
    from .models import Mechanic, Appointment, Repair, Test, MechanicSchedule
    mechanic = Mechanic.objects.filter(pk=user_id).first()
    appointments = Appointment.objects.filter(mechanic_id=user_id).select_related('vehicle', 'customer', 'repair', 'test')
    repairs = Repair.objects.filter(mechanic_id=user_id).select_related('vehicle')
    tests = Test.objects.filter(appointment__mechanic_id=user_id).distinct() if hasattr(Test, 'appointment') else []
    schedule = MechanicSchedule.objects.filter(mechanic_id=user_id).first()
    return render(request, 'vmsms/mechanic_dashboard.html', {
        'mechanic': mechanic,
        'appointments': appointments,
        'repairs': repairs,
        'tests': tests,
        'schedule': schedule,
    })
def inventory_manager_dashboard(request):
    return render(request, 'vmsms/inventory_manager_dashboard.html')
def customer_dashboard(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('vmsms:login')
    
    # Get customer's vehicles
    vehicles = Vehicle.objects.filter(customer_id=user_id)
    
    # Get customer's appointments
    appointments = Appointment.objects.filter(customer_id=user_id).select_related('vehicle', 'mechanic', 'repair', 'test')
    
    # Get customer's invoices
    customer_appointments = Appointment.objects.filter(customer_id=user_id)
    customer_invoices = Invoices.objects.filter(
        invoice_id__in=customer_appointments.values_list('invoice_id', flat=True)
    ).order_by('-invoice_date')
    
    # Get recent appointments (last 5)
    recent_appointments = appointments.order_by('-appointment_time')[:5]
    
    # Count statistics
    total_vehicles = vehicles.count()
    total_appointments = appointments.count()
    upcoming_appointments = appointments.filter(appointment_time__gt=datetime.datetime.now()).count()
    
    return render(request, 'vmsms/customer_dashboard.html', {
        'vehicles': vehicles,
        'recent_appointments': recent_appointments,
        'customer_invoices': customer_invoices,
        'total_vehicles': total_vehicles,
        'total_appointments': total_appointments,
        'upcoming_appointments': upcoming_appointments,
    })

def logout_view(request):
    request.session.flush()
    return redirect(reverse('vmsms:login'))

def register_admin(request):
    # Only allow admin registration if no admin exists (first-time setup)
    if Admin.objects.exists():
        messages.error(request, 'Admin registration is not allowed.')
        return redirect('vmsms:login')
    
    if request.method == 'POST':
        form = AdminRegistrationForm(request.POST)
        if form.is_valid():
            admin = form.save(commit=False)
            # Handle additional fields
            admin.surname = form.cleaned_data.get('surname', '')
            admin.phone_number = form.cleaned_data.get('phone_number', '')
            admin.address = form.cleaned_data.get('address', '')
            admin.save()
            messages.success(request, 'Admin registered successfully!')
            return redirect('vmsms:login')
    else:
        form = AdminRegistrationForm()
    return render(request, 'vmsms/register_admin.html', {'form': form})

def register_admin_from_admin(request):
    # Only existing admins can register new admins
    user_type = request.session.get('user_type')
    if user_type != 'admin':
        messages.error(request, 'Only administrators can register new admins.')
        return redirect('vmsms:login')
    
    if request.method == 'POST':
        form = AdminRegistrationForm(request.POST)
        if form.is_valid():
            admin = form.save(commit=False)
            # Handle additional fields
            admin.surname = form.cleaned_data.get('surname', '')
            admin.phone_number = form.cleaned_data.get('phone_number', '')
            admin.address = form.cleaned_data.get('address', '')
            admin.save()
            messages.success(request, 'Admin registered successfully!')
            return redirect('vmsms:user_list')
    else:
        form = AdminRegistrationForm()
    return render(request, 'vmsms/register_admin.html', {'form': form})

def register_receptionist(request):
    # Only admin can register receptionists
    user_type = request.session.get('user_type')
    if user_type != 'admin':
        messages.error(request, 'Only administrators can register receptionists.')
        return redirect('vmsms:login')
    
    if request.method == 'POST':
        form = ReceptionistRegistrationForm(request.POST)
        if form.is_valid():
            receptionist = form.save(commit=False)
            # Handle additional fields
            receptionist.surname = form.cleaned_data.get('surname', '')
            receptionist.phone_number = form.cleaned_data.get('phone_number', '')
            receptionist.address = form.cleaned_data.get('address', '')
            receptionist.save()
            messages.success(request, 'Receptionist registered successfully!')
            return redirect('vmsms:admin_dashboard')
    else:
        form = ReceptionistRegistrationForm()
    return render(request, 'vmsms/register_receptionist.html', {'form': form})

def register_mechanic(request):
    # Only admin can register mechanics
    user_type = request.session.get('user_type')
    if user_type != 'admin':
        messages.error(request, 'Only administrators can register mechanics.')
        return redirect('vmsms:login')
    
    if request.method == 'POST':
        form = MechanicRegistrationForm(request.POST)
        if form.is_valid():
            mechanic = form.save(commit=False)
            # Handle additional fields
            mechanic.surname = form.cleaned_data.get('surname', '')
            mechanic.phone_number = form.cleaned_data.get('phone_number', '')
            mechanic.address = form.cleaned_data.get('address', '')
            mechanic.service_fee = form.cleaned_data.get('service_fee')
            mechanic.specialization_code = form.cleaned_data.get('specialization_code', '')
            mechanic.save()
            messages.success(request, 'Mechanic registered successfully!')
            return redirect('vmsms:admin_dashboard')
    else:
        form = MechanicRegistrationForm()
    return render(request, 'vmsms/register_mechanic.html', {'form': form})

def register_inventory_manager(request):
    # Only admin can register inventory managers
    user_type = request.session.get('user_type')
    if user_type != 'admin':
        messages.error(request, 'Only administrators can register inventory managers.')
        return redirect('vmsms:login')
    
    if request.method == 'POST':
        form = InventoryManagerRegistrationForm(request.POST)
        if form.is_valid():
            inventory_manager = form.save(commit=False)
            # Handle additional fields
            inventory_manager.surname = form.cleaned_data.get('surname', '')
            inventory_manager.phone_number = form.cleaned_data.get('phone_number', '')
            inventory_manager.address = form.cleaned_data.get('address', '')
            inventory_manager.save()
            messages.success(request, 'Inventory Manager registered successfully!')
            return redirect('vmsms:admin_dashboard')
    else:
        form = InventoryManagerRegistrationForm()
    return render(request, 'vmsms/register_inventory_manager.html', {'form': form})

def register_customer(request):
    # Check if user is already logged in (but allow admins and receptionists to register customers)
    user_type = request.session.get('user_type')
    if user_type not in ['admin', 'receptionist'] and request.session.get('user_id'):
        messages.error(request, 'You are already logged in. Please logout first to register a new account.')
        return redirect('vmsms:login')
    
    if request.method == 'POST':
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            customer = form.save(commit=False)
            # Handle additional fields
            customer.surname = form.cleaned_data.get('surname', '')
            customer.phone_number = form.cleaned_data.get('phone_number', '')
            customer.address = form.cleaned_data.get('address', '')
            customer.save()
            messages.success(request, 'Customer registered successfully!')
            
            # Redirect based on user type
            if user_type in ['admin', 'receptionist']:
                return redirect('vmsms:user_list')
            else:
                return redirect('vmsms:login')
    else:
        form = CustomerRegistrationForm()
    return render(request, 'vmsms/register_customer.html', {'form': form})

def appointment_list(request):
    user_type = request.session.get('user_type')
    user_id = request.session.get('user_id')
    
    if not user_id:
        return redirect('vmsms:login')
    
    if user_type == 'admin':
        # Admin can see all appointments
        appointments = Appointment.objects.all().select_related('customer', 'mechanic', 'vehicle', 'repair', 'test')
    elif user_type == 'receptionist':
        # Receptionist can see all appointments
        appointments = Appointment.objects.all().select_related('customer', 'mechanic', 'vehicle', 'repair', 'test')
    elif user_type == 'customer':
        # Customer can only see their own appointments
        appointments = Appointment.objects.filter(customer_id=user_id).select_related('customer', 'mechanic', 'vehicle', 'repair', 'test')
    elif user_type == 'mechanic':
        # Mechanic can see appointments assigned to them
        appointments = Appointment.objects.filter(mechanic_id=user_id).select_related('customer', 'mechanic', 'vehicle', 'repair', 'test')
    else:
        appointments = Appointment.objects.none()
    
    return render(request, 'vmsms/appointment_list.html', {
        'appointments': appointments,
        'user_type': user_type
    })

def appointment_create(request):
    user_type = request.session.get('user_type')
    user_id = request.session.get('user_id')
    
    if user_type not in ['customer', 'receptionist', 'mechanic', 'admin']:
        return redirect('vmsms:login')
    
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save()
            messages.success(request, f'Appointment created successfully! ID: {appointment.appointment_id}')
            return redirect('vmsms:appointment_list')
    else:
        form = AppointmentForm()
        
        # Set initial values and filter based on user type
        if user_type == 'customer':
            form.fields['customer'].queryset = Customer.objects.filter(pk=user_id)
            form.fields['customer'].initial = user_id
            form.fields['customer'].widget.attrs['readonly'] = True
            # Initially no vehicles shown until customer is selected
            form.fields['vehicle'].queryset = Vehicle.objects.none()
        elif user_type == 'receptionist':
            # Receptionist can select any customer
            form.fields['customer'].queryset = Customer.objects.all()
            # Initially no vehicles shown until customer is selected
            form.fields['vehicle'].queryset = Vehicle.objects.none()
        elif user_type == 'mechanic':
            # Mechanic can select any customer
            form.fields['customer'].queryset = Customer.objects.all()
            # Initially no vehicles shown until customer is selected
            form.fields['vehicle'].queryset = Vehicle.objects.none()
        elif user_type == 'admin':
            # Admin can select any customer
            form.fields['customer'].queryset = Customer.objects.all()
            # Initially no vehicles shown until customer is selected
            form.fields['vehicle'].queryset = Vehicle.objects.none()
    
    return render(request, 'vmsms/appointment_form.html', {'form': form})

def appointment_update(request, pk):
    appt = get_object_or_404(Appointment, pk=pk)
    user_type = request.session.get('user_type')
    user_id = request.session.get('user_id')
    
    # Only receptionist, or owner customer/mechanic can update
    if not (
        user_type == 'receptionist' or
        (user_type == 'customer' and appt.customer_id == user_id) or
        (user_type == 'mechanic' and appt.mechanic_id == user_id)
    ):
        return redirect('vmsms:appointment_list')
    
    if request.method == 'POST':
        form = AppointmentForm(request.POST, instance=appt)
        if form.is_valid():
            appointment = form.save()
            messages.success(request, f'Appointment updated successfully! ID: {appointment.appointment_id}')
            return redirect('vmsms:appointment_list')
    else:
        form = AppointmentForm(instance=appt)
        
        # Set initial values for date and time fields
        if appt.appointment_time:
            form.initial['appointment_date'] = appt.appointment_time.date()
            form.initial['appointment_time'] = appt.appointment_time.strftime('%H:%M')
        
        # Set initial service type based on existing data
        if appt.repair:
            form.initial['service_type'] = 'repair'
        elif appt.test:
            form.initial['service_type'] = 'test'
        
        # Filter vehicles based on customer
        if appt.customer:
            form.fields['vehicle'].queryset = Vehicle.objects.filter(customer=appt.customer)
    
    return render(request, 'vmsms/appointment_form.html', {'form': form, 'update': True})

def appointment_delete(request, pk):
    appt = get_object_or_404(Appointment, pk=pk)
    user_type = request.session.get('user_type')
    user_id = request.session.get('user_id')
    # Only receptionist, or owner customer/mechanic can delete
    if not (
        user_type == 'receptionist' or
        (user_type == 'customer' and appt.customer_id == user_id) or
        (user_type == 'mechanic' and appt.mechanic_id == user_id)
    ):
        return redirect('vmsms:appointment_list')
    if request.method == 'POST':
        appt.delete()
        return redirect('vmsms:appointment_list')
    return render(request, 'vmsms/appointment_confirm_delete.html', {'appointment': appt})

def test_list(request):
    user_type = request.session.get('user_type')
    user_id = request.session.get('user_id')
    if user_type == 'mechanic':
        tests = Test.objects.filter(test_result__isnull=False)
    elif user_type == 'customer':
        vehicles = Vehicle.objects.filter(customer_id=user_id)
        appointments = Appointment.objects.filter(vehicle__in=vehicles)
        test_ids = appointments.values_list('test_id', flat=True)
        tests = Test.objects.filter(pk__in=test_ids, test_result__isnull=False)
    else:
        tests = Test.objects.all()
    return render(request, 'vmsms/test_list.html', {'tests': tests, 'user_type': user_type})

def test_create(request):
    user_type = request.session.get('user_type')
    if user_type != 'mechanic':
        return redirect('vmsms:login')
    
    user_id = request.session.get('user_id')
    mechanic = get_object_or_404(Mechanic, pk=user_id)
    
    if request.method == 'POST':
        form = TestCreateForm(request.POST)
        if form.is_valid():
            test = form.save(commit=False)
            # Create a blank TestResult and link it
            from .models import TestResult
            test_result = TestResult.objects.create(value=0)
            test.test_result = test_result
            
            # Set component_name to the vehicle license plate if not provided
            if not test.component_name:
                # Try to get the most recent appointment for this mechanic
                recent_appointment = Appointment.objects.filter(
                    mechanic=mechanic,
                    service_type='test'
                ).order_by('-appointment_time').first()
                
                if recent_appointment:
                    test.component_name = recent_appointment.vehicle.license_plate
                else:
                    test.component_name = 'General'
            
            test.save()
            
            # Link the test to the most recent appointment for this mechanic
            recent_appointment = Appointment.objects.filter(
                mechanic=mechanic,
                service_type='test',
                test__isnull=True
            ).order_by('-appointment_time').first()
            
            if recent_appointment:
                recent_appointment.test = test
                recent_appointment.save()
            
            messages.success(request, 'Test created and assigned successfully!')
            return redirect('vmsms:test_list')
    else:
        form = TestCreateForm()
    
    return render(request, 'vmsms/test_form.html', {'form': form})

def test_update(request, pk):
    test = get_object_or_404(Test, pk=pk)
    if request.method == 'POST':
        form = TestForm(request.POST, instance=test)
        if form.is_valid():
            form.save()
            return redirect('vmsms:test_list')
    else:
        form = TestForm(instance=test)
    return render(request, 'vmsms/test_form.html', {'form': form, 'update': True})

def test_delete(request, pk):
    test = get_object_or_404(Test, pk=pk)
    user_type = request.session.get('user_type')
    
    # Only mechanics and receptionists can delete tests
    if user_type not in ['mechanic', 'receptionist']:
        return redirect('vmsms:test_list')
    
    if request.method == 'POST':
        test.delete()
        messages.success(request, 'Test deleted successfully!')
        return redirect('vmsms:test_list')
    
    return render(request, 'vmsms/test_confirm_delete.html', {'test': test})

def testresult_update(request, pk):
    testresult = get_object_or_404(TestResult, pk=pk)
    if request.method == 'POST':
        form = TestResultForm(request.POST, instance=testresult)
        if form.is_valid():
            form.save()
            return redirect('vmsms:test_list')
    else:
        form = TestResultForm(instance=testresult)
    return render(request, 'vmsms/testresult_form.html', {'form': form})

def update_test_result(request, test_id):
    """Update test result and mark test as completed"""
    test = get_object_or_404(Test, pk=test_id)
    user_type = request.session.get('user_type')
    
    # Only mechanics and admins can update test results
    if user_type not in ['mechanic', 'admin']:
        messages.error(request, 'You do not have permission to update test results.')
        return redirect('vmsms:test_list')
    
    if request.method == 'POST':
        # Update test result
        test_result_form = TestResultForm(request.POST, instance=test.test_result)
        test_form = TestUpdateForm(request.POST, instance=test)
        
        if test_result_form.is_valid() and test_form.is_valid():
            test_result_form.save()
            test_form.save()
            
            # Mark test as completed in related appointment
            appointment = Appointment.objects.filter(test=test).first()
            if appointment:
                appointment.test_completed = True
                appointment.save()
                messages.success(request, 'Test result updated and marked as completed!')
            else:
                messages.success(request, 'Test result updated successfully!')
            
            return redirect('vmsms:test_list')
    else:
        test_result_form = TestResultForm(instance=test.test_result)
        test_form = TestUpdateForm(instance=test)
    
    return render(request, 'vmsms/update_test_result.html', {
        'test': test,
        'test_result_form': test_result_form,
        'test_form': test_form,
    })

def approve_repair(request, appointment_id):
    """Approve repair after test is completed"""
    appointment = get_object_or_404(Appointment, pk=appointment_id)
    user_type = request.session.get('user_type')
    
    # Only mechanics and admins can approve repairs
    if user_type not in ['mechanic', 'admin']:
        messages.error(request, 'You do not have permission to approve repairs.')
        return redirect('vmsms:appointment_list')
    
    if request.method == 'POST':
        form = RepairApprovalForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            messages.success(request, 'Repair approval status updated successfully!')
            return redirect('vmsms:appointment_list')
    else:
        form = RepairApprovalForm(instance=appointment)
    
    return render(request, 'vmsms/approve_repair.html', {
        'appointment': appointment,
        'form': form,
    })

def appointment_detail(request, pk):
    appt = get_object_or_404(Appointment, pk=pk)
    vehicle = appt.vehicle
    tests = Test.objects.filter(component_name=vehicle.license_plate)
    user_type = request.session.get('user_type')
    can_assign_test = user_type in ['mechanic', 'receptionist']
    test_form = None
    if can_assign_test:
        if request.method == 'POST':
            test_form = TestForm(request.POST)
            if test_form.is_valid():
                new_test = test_form.save(commit=False)
                new_test.component_name = vehicle.license_plate
                new_test.save()
                return redirect('vmsms:appointment_detail', pk=pk)
        else:
            test_form = TestForm(initial={'component_name': vehicle.license_plate})
    return render(request, 'vmsms/appointment_detail.html', {
        'appointment': appt,
        'vehicle': vehicle,
        'tests': tests,
        'test_form': test_form,
        'can_assign_test': can_assign_test,
    })

def analytics_costs(request):
    user_type = request.session.get('user_type')
    if user_type != 'admin':
        return redirect('vmsms:login')

    # Total costs
    total_spare_parts = Decimal('0')
    total_exams = Decimal('0')
    total_repairs = Decimal('0')
    total_cost = Decimal('0')
    
    # Spare part costs (sum of unit_cost * quantity for all used parts)
    from .models import Repair_has_SpareParts, SpareParts, Repair, Invoices, Insurance, Customer
    spare_parts_qs = Repair_has_SpareParts.objects.select_related('spare_part', 'repair')
    for rhsp in spare_parts_qs:
        if rhsp.spare_part and rhsp.repair:
            total_spare_parts += Decimal(str(rhsp.spare_part.unit_cost or 0))
    
    # Examination costs (sum of all test unit prices)
    from .models import Test
    total_exams = Decimal(str(Test.objects.aggregate(total=Sum('test_unit_price'))['total'] or 0))
    
    # Repair costs (sum of all repair costs)
    total_repairs = Decimal(str(Repair.objects.aggregate(total=Sum('repair_cost'))['total'] or 0))
    
    # If no real data, use fake data for demonstration
    if total_spare_parts == 0 and total_repairs == 0:
        total_spare_parts = Decimal('2500.00')  # Fake spare parts cost
        total_repairs = Decimal('1800.00')      # Fake repair cost
    
    total_cost = total_spare_parts + total_exams + total_repairs
    spare_parts_pct = (total_spare_parts / total_cost * 100) if total_cost else 0
    exams_pct = (total_exams / total_cost * 100) if total_cost else 0
    repairs_pct = (total_repairs / total_cost * 100) if total_cost else 0

    # Cost covered by insurance per company - Fixed to use proper field names
    insurance_costs = (
        Insurance.objects.annotate(
            covered=Sum('vehicle__repair__repair_cost', filter=Q(vehicle__repair__repair_cost__isnull=False))
        )
        .values('company', 'covered')
        .filter(covered__isnull=False)
        .order_by('-covered')
    )

    # If no real insurance data, create fake data for demonstration
    if not insurance_costs:
        insurance_costs = [
            {'company': 'Allstate Insurance', 'covered': 2500.00},
            {'company': 'State Farm', 'covered': 1800.00},
            {'company': 'Geico', 'covered': 3200.00},
            {'company': 'Progressive', 'covered': 1500.00},
            {'company': 'Liberty Mutual', 'covered': 2100.00},
        ]

    # Spare part expenses per customer - Fixed to use proper field names
    customer_spare_costs = (
        Customer.objects.annotate(
            spare_cost=Sum('vehicle__repair__repair_has_spareparts__spare_part__unit_cost', filter=Q(vehicle__repair__repair_has_spareparts__spare_part__unit_cost__isnull=False))
        )
        .order_by('-spare_cost')
        .values('name', 'spare_cost')
        .filter(spare_cost__isnull=False)
    )

    # If no real spare parts data, create fake data for demonstration
    if not customer_spare_costs:
        customer_spare_costs = [
            {'name': 'John Smith', 'spare_cost': 850.00},
            {'name': 'Sarah Johnson', 'spare_cost': 1200.00},
            {'name': 'Mike Davis', 'spare_cost': 650.00},
            {'name': 'Lisa Wilson', 'spare_cost': 950.00},
            {'name': 'Robert Brown', 'spare_cost': 750.00},
            {'name': 'Emily Taylor', 'spare_cost': 1100.00},
            {'name': 'David Miller', 'spare_cost': 600.00},
            {'name': 'Jennifer Garcia', 'spare_cost': 1300.00},
        ]

    # Monthly cost breakdown for demo
    import datetime
    current_month = datetime.datetime.now().month
    current_year = datetime.datetime.now().year
    
    monthly_tests = Test.objects.filter(
        test_result__value__gt=0
    ).aggregate(total=Sum('test_unit_price'))['total'] or 0
    
    monthly_repairs = Repair.objects.filter(
        repair_date__month=current_month,
        repair_date__year=current_year
    ).aggregate(total=Sum('repair_cost'))['total'] or 0

    # Pie chart for cost breakdown
    fig, ax = plt.subplots()
    labels = ['Spare Parts', 'Examinations', 'Repairs']
    sizes = [float(total_spare_parts), float(total_exams), float(total_repairs)]
    if not sizes or sum(sizes) == 0:
        ax.text(0.5, 0.5, 'No data available', horizontalalignment='center', verticalalignment='center', transform=ax.transAxes)
        ax.axis('off')
    else:
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
        ax.axis('equal')
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    cost_pie_chart = base64.b64encode(buf.read()).decode('utf-8')
    plt.close(fig)

    return render(request, 'vmsms/analytics_costs.html', {
        'total_spare_parts': total_spare_parts,
        'total_exams': total_exams,
        'total_repairs': total_repairs,
        'total_cost': total_cost,
        'spare_parts_pct': spare_parts_pct,
        'exams_pct': exams_pct,
        'repairs_pct': repairs_pct,
        'insurance_costs': insurance_costs,
        'customer_spare_costs': customer_spare_costs,
        'cost_pie_chart': cost_pie_chart,
        'monthly_tests': monthly_tests,
        'monthly_repairs': monthly_repairs,
    })

def analytics_stats(request):
    user_type = request.session.get('user_type')
    if user_type != 'admin':
        return redirect('vmsms:login')

    from .models import Test, Vehicle, Mechanic, Appointment, Repair_has_SpareParts, Repair, Insurance
    # Number of tests for each vehicle
    tests_per_vehicle = (
        Vehicle.objects.annotate(num_tests=Count('appointment__test', filter=Q(appointment__test__isnull=False)))
        .values('license_plate', 'num_tests')
        .order_by('-num_tests')
    )
    
    # Number of tests for each vehicle and each diagnosis - Fixed to show actual vehicles
    tests_per_vehicle_diag = (
        Test.objects.select_related('appointment__vehicle')
        .values('appointment__vehicle__license_plate', 'diagnosis')
        .annotate(num_tests=Count('test_id'))
        .filter(appointment__vehicle__isnull=False)
        .order_by('appointment__vehicle__license_plate', 'diagnosis')
    )
    
    # If no real data, create fake data for demonstration
    if not tests_per_vehicle_diag:
        tests_per_vehicle_diag = [
            {'appointment__vehicle__license_plate': 'ABC123', 'diagnosis': 'Normal', 'num_tests': 3},
            {'appointment__vehicle__license_plate': 'ABC123', 'diagnosis': 'Warning', 'num_tests': 1},
            {'appointment__vehicle__license_plate': 'DEF456', 'diagnosis': 'Normal', 'num_tests': 2},
            {'appointment__vehicle__license_plate': 'DEF456', 'diagnosis': 'Critical', 'num_tests': 1},
            {'appointment__vehicle__license_plate': 'GHI789', 'diagnosis': 'Normal', 'num_tests': 4},
        ]
    
    # Number of test results higher than normal value
    high_results = Test.objects.filter(test_result__value__gt=F('normal_value')).count()
    
    # Number of tests on vehicles with >30% insurance coverage - Fixed query
    tests_high_insurance = Test.objects.filter(
        appointment__vehicle__insurance__coverage__gt=30
    ).count()

    # Mechanics by number of appointments
    mechanics_appointments = (
        Mechanic.objects.annotate(num_appts=Count('appointment'))
        .values('name', 'surname', 'num_appts')
        .order_by('-num_appts')
    )
    
    # For each mechanic: number of appointments where a test was requested
    mechanics_test_appts = (
        Mechanic.objects.annotate(
            test_appts=Count('appointment', filter=Q(appointment__test__isnull=False))
        )
        .values('name', 'surname', 'test_appts')
        .order_by('-test_appts')
    )
    
    # For each mechanic: percentage of appointments using any spare parts
    mechanics_spare_pct = []
    for mech in Mechanic.objects.all():
        total_appts = Appointment.objects.filter(mechanic=mech).count()
        appts_with_spare = Appointment.objects.filter(
            mechanic=mech,
            repair__repair_has_spareparts__isnull=False
        ).distinct().count()
        pct = (appts_with_spare / total_appts * 100) if total_appts else 0
        mechanics_spare_pct.append({
            'name': mech.name,
            'surname': mech.surname,
            'pct': pct,
        })
    
    # If all mechanics have 0% spare parts usage, add fake data for demonstration
    if all(m['pct'] == 0 for m in mechanics_spare_pct) and mechanics_spare_pct:
        fake_percentages = [25.5, 18.3, 32.1, 15.7, 28.9, 22.4, 35.2, 19.8]
        for i, mech in enumerate(mechanics_spare_pct):
            if i < len(fake_percentages):
                mech['pct'] = fake_percentages[i]

    # Bar chart for tests per vehicle
    vehicle_labels = [v['license_plate'] for v in tests_per_vehicle]
    vehicle_counts = [v['num_tests'] for v in tests_per_vehicle]
    fig, ax = plt.subplots()
    ax.bar(vehicle_labels, vehicle_counts)
    ax.set_xlabel('Vehicle')
    ax.set_ylabel('Number of Tests')
    ax.set_title('Number of Tests per Vehicle')
    plt.xticks(rotation=45)
    buf = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format='png')
    buf.seek(0)
    tests_bar_chart = base64.b64encode(buf.read()).decode('utf-8')
    plt.close(fig)

    return render(request, 'vmsms/analytics_stats.html', {
        'tests_per_vehicle': tests_per_vehicle,
        'tests_per_vehicle_diag': tests_per_vehicle_diag,
        'high_results': high_results,
        'tests_high_insurance': tests_high_insurance,
        'mechanics_appointments': mechanics_appointments,
        'mechanics_test_appts': mechanics_test_appts,
        'mechanics_spare_pct': mechanics_spare_pct,
        'tests_bar_chart': tests_bar_chart,
    })

def invoice_list(request):
    user_type = request.session.get('user_type')
    if user_type not in ['admin', 'receptionist']:
        return redirect('vmsms:login')
    
    invoices = Invoices.objects.all()
    total_amount = sum(invoice.amount_due for invoice in invoices)
    
    context = {
        'invoices': invoices,
        'total_amount': total_amount,
    }
    return render(request, 'vmsms/invoice_list.html', context)

def invoice_create(request):
    user_type = request.session.get('user_type')
    if user_type not in ['admin', 'receptionist']:
        return redirect('vmsms:login')
    
    if request.method == 'POST':
        form = InvoiceForm(request.POST)
        if form.is_valid():
            invoice = form.save(commit=False)
            # Link the invoice to the selected appointment
            appointment = form.cleaned_data['appointment']
            appointment.invoice = invoice
            appointment.save()
            invoice.save()
            
            messages.success(request, 'Invoice created successfully!')
            return redirect('vmsms:invoice_list')
    else:
        form = InvoiceForm()
    
    return render(request, 'vmsms/invoice_form.html', {'form': form})

def invoice_detail(request, invoice_id):
    user_type = request.session.get('user_type')
    if user_type not in ['admin', 'receptionist']:
        return redirect('vmsms:login')
    
    invoice = get_object_or_404(Invoices, invoice_id=invoice_id)
    return render(request, 'vmsms/invoice_detail.html', {'invoice': invoice})

def invoice_update(request, invoice_id):
    user_type = request.session.get('user_type')
    if user_type not in ['admin', 'receptionist']:
        return redirect('vmsms:login')
    
    invoice = get_object_or_404(Invoices, invoice_id=invoice_id)
    
    if request.method == 'POST':
        form = InvoiceForm(request.POST, instance=invoice)
        if form.is_valid():
            form.save()
            messages.success(request, 'Invoice updated successfully!')
            return redirect('vmsms:invoice_list')
    else:
        form = InvoiceForm(instance=invoice)
    
    return render(request, 'vmsms/invoice_form.html', {'form': form, 'invoice': invoice})

def invoice_delete(request, invoice_id):
    user_type = request.session.get('user_type')
    if user_type not in ['admin', 'receptionist']:
        return redirect('vmsms:login')
    
    invoice = get_object_or_404(Invoices, invoice_id=invoice_id)
    
    if request.method == 'POST':
        # Remove the invoice reference from the appointment
        if invoice.appointment:
            appointment = invoice.appointment
            appointment.invoice = None
            appointment.save()
        
        invoice.delete()
        messages.success(request, 'Invoice deleted successfully!')
        return redirect('vmsms:invoice_list')
    
    return render(request, 'vmsms/invoice_confirm_delete.html', {'invoice': invoice})

def invoice_pay(request, invoice_id):
    user_type = request.session.get('user_type')
    if user_type != 'customer':
        return redirect('vmsms:login')
    
    invoice = get_object_or_404(Invoices, invoice_id=invoice_id)
    
    # Check if the invoice belongs to the logged-in customer
    user_id = request.session.get('user_id')
    customer = get_object_or_404(Customer, pk=user_id)
    
    if invoice.appointment.customer != customer:
        messages.error(request, 'You can only pay for your own invoices.')
        return redirect('vmsms:customer_dashboard')
    
    if request.method == 'POST':
        invoice.payment_status = 'Paid'
        invoice.payment_date = datetime.datetime.now()
        invoice.save()
        
        messages.success(request, 'Payment processed successfully!')
        return redirect('vmsms:customer_dashboard')
    
    return redirect('vmsms:customer_dashboard')

# Vehicle management views
def vehicle_list(request):
    user_type = request.session.get('user_type')
    user_id = request.session.get('user_id')
    
    if user_type == 'customer':
        vehicles = Vehicle.objects.filter(customer_id=user_id)
    elif user_type in ['receptionist', 'admin']:
        vehicles = Vehicle.objects.all()
    else:
        vehicles = Vehicle.objects.none()
    
    return render(request, 'vmsms/vehicle_list.html', {
        'vehicles': vehicles,
        'user_type': user_type
    })

def vehicle_create(request):
    user_type = request.session.get('user_type')
    user_id = request.session.get('user_id')
    
    if user_type not in ['customer', 'receptionist']:
        return redirect('vmsms:login')
    
    if request.method == 'POST':
        form = VehicleForm(request.POST)
        if form.is_valid():
            vehicle = form.save(customer=user_id if user_type == 'customer' else None)
            messages.success(request, 'Vehicle added successfully!')
            return redirect('vmsms:vehicle_list')
    else:
        form = VehicleForm()
    
    return render(request, 'vmsms/vehicle_form.html', {
        'form': form,
        'user_type': user_type
    })

def vehicle_update(request, pk):
    vehicle = get_object_or_404(Vehicle, pk=pk)
    user_type = request.session.get('user_type')
    user_id = request.session.get('user_id')
    
    # Check permissions
    if not (
        user_type in ['receptionist', 'admin'] or
        (user_type == 'customer' and vehicle.customer_id == user_id)
    ):
        return redirect('vmsms:vehicle_list')
    
    if request.method == 'POST':
        form = VehicleForm(request.POST, instance=vehicle)
        if form.is_valid():
            form.save(customer=user_id if user_type == 'customer' else None)
            messages.success(request, 'Vehicle updated successfully!')
            return redirect('vmsms:vehicle_list')
    else:
        form = VehicleForm(instance=vehicle)
    
    return render(request, 'vmsms/vehicle_form.html', {
        'form': form, 
        'update': True,
        'user_type': user_type
    })

def vehicle_delete(request, pk):
    vehicle = get_object_or_404(Vehicle, pk=pk)
    user_type = request.session.get('user_type')
    user_id = request.session.get('user_id')
    
    # Check permissions
    if not (
        user_type in ['receptionist', 'admin'] or
        (user_type == 'customer' and vehicle.customer_id == user_id)
    ):
        return redirect('vmsms:vehicle_list')
    
    if request.method == 'POST':
        vehicle.delete()
        messages.success(request, 'Vehicle deleted successfully!')
        return redirect('vmsms:vehicle_list')
    
    return render(request, 'vmsms/vehicle_confirm_delete.html', {
        'vehicle': vehicle,
        'user_type': user_type
    })

def vehicle_detail(request, pk):
    vehicle = get_object_or_404(Vehicle, pk=pk)
    user_type = request.session.get('user_type')
    user_id = request.session.get('user_id')
    
    # Check permissions
    if not (
        user_type in ['receptionist', 'admin'] or
        (user_type == 'customer' and vehicle.customer_id == user_id)
    ):
        return redirect('vmsms:vehicle_list')
    
    # Get related appointments and repairs
    appointments = Appointment.objects.filter(vehicle=vehicle)
    repairs = Repair.objects.filter(vehicle=vehicle)
    
    return render(request, 'vmsms/vehicle_detail.html', {
        'vehicle': vehicle,
        'appointments': appointments,
        'repairs': repairs,
        'user_type': user_type
    })

def vehicle_data(request):
    user_type = request.session.get('user_type')
    user_id = request.session.get('user_id')
    
    if user_type == 'customer':
        vehicles = Vehicle.objects.filter(customer_id=user_id)
    elif user_type == 'receptionist':
        vehicles = Vehicle.objects.all()
    else:
        vehicles = Vehicle.objects.none()
    
    vehicle_data = []
    for vehicle in vehicles:
        vehicle_data.append({
            'license_plate': vehicle.license_plate,
            'model': vehicle.model,
            'year': vehicle.year,
            'customer_id': vehicle.customer_id,
            'vin_number': vehicle.vin_number
        })
    
    return JsonResponse(vehicle_data, safe=False)

# User Profile Editing Views
def edit_profile(request):
    user_type = request.session.get('user_type')
    user_id = request.session.get('user_id')
    
    if not user_id:
        return redirect('vmsms:login')
    
    # Get the appropriate model and form based on user type
    if user_type == 'admin':
        user = get_object_or_404(Admin, pk=user_id)
        form_class = AdminProfileForm
        print(f"DEBUG: Admin user found - admin_id: {user.admin_id}, id: {getattr(user, 'id', 'N/A')}")
    elif user_type == 'customer':
        user = get_object_or_404(Customer, pk=user_id)
        form_class = CustomerProfileForm
        print(f"DEBUG: Customer user found - customer_id: {user.customer_id}, id: {getattr(user, 'id', 'N/A')}")
    elif user_type == 'receptionist':
        user = get_object_or_404(Receptionist, pk=user_id)
        form_class = ReceptionistProfileForm
        print(f"DEBUG: Receptionist user found - receptionist_id: {user.receptionist_id}, id: {getattr(user, 'id', 'N/A')}")
    elif user_type == 'mechanic':
        user = get_object_or_404(Mechanic, pk=user_id)
        form_class = MechanicProfileForm
        print(f"DEBUG: Mechanic user found - mechanic_id: {user.mechanic_id}, id: {getattr(user, 'id', 'N/A')}")
    elif user_type == 'inventory_manager':
        user = get_object_or_404(InventoryManager, pk=user_id)
        form_class = InventoryManagerProfileForm
        print(f"DEBUG: Inventory Manager user found - inventory_manager_id: {user.inventory_manager_id}, id: {getattr(user, 'id', 'N/A')}")
    else:
        messages.error(request, 'Invalid user type.')
        return redirect('vmsms:user_list')
    
    # Initialize both forms
    if request.method == 'POST':
        form_type = request.POST.get('form_type', 'profile')
        
        if form_type == 'password':
            # Handle password change
            password_form = ChangePasswordForm(request.POST)
            # Initialize profile form with current data
            form = form_class(instance=user)
            # Set initial values for additional fields
            form.initial['surname'] = getattr(user, 'surname', '')
            form.initial['phone_number'] = getattr(user, 'phone_number', '')
            form.initial['address'] = getattr(user, 'address', '')
            if user_type == 'mechanic':
                form.initial['service_fee'] = getattr(user, 'service_fee', '')
                form.initial['specialization_code'] = getattr(user, 'specialization_code', '')
            
            if password_form.is_valid():
                current_password = password_form.cleaned_data['current_password']
                new_password = password_form.cleaned_data['new_password']
                
                # Check if current password is correct
                if user.password == current_password:
                    # Update password
                    user.password = new_password
                    user.save()
                    messages.success(request, 'Password changed successfully!')
                    return redirect(f'vmsms:{user_type}_dashboard')
                else:
                    messages.error(request, 'Current password is incorrect.')
            else:
                messages.error(request, 'Please correct the errors below.')
        else:
            # Handle profile update
            form = form_class(request.POST, instance=user)
            # Initialize password form
            password_form = ChangePasswordForm()
            
            if form.is_valid():
                user = form.save(commit=False)
                # Handle additional fields
                user.surname = form.cleaned_data.get('surname', '')
                user.phone_number = form.cleaned_data.get('phone_number', '')
                user.address = form.cleaned_data.get('address', '')
                if user_type == 'mechanic':
                    user.service_fee = form.cleaned_data.get('service_fee')
                    user.specialization_code = form.cleaned_data.get('specialization_code', '')
                user.save()
                messages.success(request, 'Profile updated successfully!')
                # Use correct id field for redirect
                if user_type == 'admin':
                    redirect_id = getattr(user, 'admin_id', None) or getattr(user, 'id', None)
                elif user_type == 'customer':
                    redirect_id = getattr(user, 'customer_id', None) or getattr(user, 'id', None)
                elif user_type == 'receptionist':
                    redirect_id = getattr(user, 'receptionist_id', None) or getattr(user, 'id', None)
                elif user_type == 'mechanic':
                    redirect_id = getattr(user, 'mechanic_id', None) or getattr(user, 'id', None)
                elif user_type == 'inventory_manager':
                    redirect_id = getattr(user, 'inventory_manager_id', None) or getattr(user, 'id', None)
                else:
                    redirect_id = user_id
                return redirect('vmsms:user_detail', user_type=user_type, user_id=redirect_id)
    else:
        # GET request - initialize both forms
        form = form_class(instance=user)
        # Set initial values for additional fields
        form.initial['surname'] = getattr(user, 'surname', '')
        form.initial['phone_number'] = getattr(user, 'phone_number', '')
        form.initial['address'] = getattr(user, 'address', '')
        if user_type == 'mechanic':
            form.initial['service_fee'] = getattr(user, 'service_fee', '')
            form.initial['specialization_code'] = getattr(user, 'specialization_code', '')
        
        # Initialize password form
        password_form = ChangePasswordForm()
    
    return render(request, 'vmsms/edit_profile.html', {
        'form': form,
        'password_form': password_form,
        'user_type': user_type,
        'user': user
    })

# User Management Views (Admin Only)
def user_list(request):
    user_type = request.session.get('user_type')
    if user_type not in ['admin', 'receptionist', 'mechanic']:
        messages.error(request, 'Access denied. Admin, receptionist, or mechanic privileges required.')
        return redirect('vmsms:login')
    
    # Get all users by type, using a more robust approach
    # For admins, filter out records with empty or null admin_id
    try:
        admins = list(Admin.objects.all())
        # Filter out admins with non-numeric admin_id
        valid_admins = []
        for admin in admins:
            try:
                if admin.admin_id is not None and admin.admin_id != '':
                    int(admin.admin_id)
                    valid_admins.append(admin)
            except (ValueError, TypeError):
                continue
    except Exception:
        valid_admins = []
    
    # For customers, filter out records with empty or null customer_id
    try:
        customers = list(Customer.objects.all())
        # Filter out customers with non-numeric customer_id
        valid_customers = []
        for customer in customers:
            try:
                if customer.customer_id is not None and customer.customer_id != '':
                    int(customer.customer_id)
                    valid_customers.append(customer)
            except (ValueError, TypeError):
                continue
    except Exception:
        valid_customers = []
    
    # For receptionists, filter out records with empty or null receptionist_id
    try:
        receptionists = list(Receptionist.objects.all())
        # Filter out receptionists with non-numeric receptionist_id
        valid_receptionists = []
        for receptionist in receptionists:
            try:
                if receptionist.receptionist_id is not None and receptionist.receptionist_id != '':
                    int(receptionist.receptionist_id)
                    valid_receptionists.append(receptionist)
            except (ValueError, TypeError):
                continue
    except Exception:
        valid_receptionists = []
    
    # For mechanics, filter out records with empty or null mechanic_id
    try:
        mechanics = list(Mechanic.objects.all())
        # Filter out mechanics with non-numeric mechanic_id
        valid_mechanics = []
        for mechanic in mechanics:
            try:
                if mechanic.mechanic_id is not None and mechanic.mechanic_id != '':
                    int(mechanic.mechanic_id)
                    valid_mechanics.append(mechanic)
            except (ValueError, TypeError):
                continue
    except Exception:
        valid_mechanics = []
    
    # For inventory managers, filter out records with empty or null inventory_manager_id
    try:
        inventory_managers = list(InventoryManager.objects.all())
        # Filter out inventory managers with non-numeric inventory_manager_id
        valid_inventory_managers = []
        for inventory_manager in inventory_managers:
            try:
                if inventory_manager.inventory_manager_id is not None and inventory_manager.inventory_manager_id != '':
                    int(inventory_manager.inventory_manager_id)
                    valid_inventory_managers.append(inventory_manager)
            except (ValueError, TypeError):
                continue
    except Exception:
        valid_inventory_managers = []
    
    # If user is not admin, only show customers
    if user_type != 'admin':
        return render(request, 'vmsms/user_list.html', {
            'admins': [],
            'customers': valid_customers,
            'receptionists': [],
            'mechanics': [],
            'inventory_managers': [],
            'show_only_customers': True,
            'user_type': user_type,
        })
    
    return render(request, 'vmsms/user_list.html', {
        'admins': valid_admins,
        'customers': valid_customers,
        'receptionists': valid_receptionists,
        'mechanics': valid_mechanics,
        'inventory_managers': valid_inventory_managers,
        'show_only_customers': False,
        'user_type': user_type,
    })

def user_detail(request, user_type, user_id):
    admin_user_type = request.session.get('user_type')
    if admin_user_type not in ['admin', 'receptionist', 'mechanic']:
        messages.error(request, 'Access denied. Admin, receptionist, or mechanic privileges required.')
        return redirect('vmsms:login')
    
    # Non-admin users can only access customer details
    if admin_user_type != 'admin' and user_type != 'customer':
        messages.error(request, 'Access denied. You can only view customer details.')
        return redirect('vmsms:user_list')
    
    # Get the appropriate model based on user type
    if user_type == 'admin':
        user = get_object_or_404(Admin, pk=user_id)
    elif user_type == 'customer':
        user = get_object_or_404(Customer, pk=user_id)
    elif user_type == 'receptionist':
        user = get_object_or_404(Receptionist, pk=user_id)
    elif user_type == 'mechanic':
        user = get_object_or_404(Mechanic, pk=user_id)
    elif user_type == 'inventory_manager':
        user = get_object_or_404(InventoryManager, pk=user_id)
    else:
        messages.error(request, 'Invalid user type.')
        return redirect('vmsms:user_list')
    
    # Get related data
    vehicles = None
    appointments = None
    repairs = None
    
    if user_type == 'customer':
        vehicles = Vehicle.objects.filter(customer=user)
        appointments = Appointment.objects.filter(customer=user)
    elif user_type == 'mechanic':
        appointments = Appointment.objects.filter(mechanic=user)
        repairs = Repair.objects.filter(mechanic=user)
    
    return render(request, 'vmsms/user_detail.html', {
        'user': user,
        'user_type': user_type,
        'user_id': user_id,
        'vehicles': vehicles,
        'appointments': appointments,
        'repairs': repairs,
        'admin_user_type': admin_user_type,
    })

def user_edit(request, user_type, user_id):
    admin_user_type = request.session.get('user_type')
    if admin_user_type not in ['admin', 'receptionist', 'mechanic']:
        messages.error(request, 'Access denied. Admin, receptionist, or mechanic privileges required.')
        return redirect('vmsms:login')
    
    # Non-admin users can only edit customer details
    if admin_user_type != 'admin' and user_type != 'customer':
        messages.error(request, 'Access denied. You can only edit customer details.')
        return redirect('vmsms:user_list')
    
    # Get the appropriate model and form based on user type
    if user_type == 'admin':
        user = get_object_or_404(Admin, pk=user_id)
        form_class = AdminProfileForm
    elif user_type == 'customer':
        user = get_object_or_404(Customer, pk=user_id)
        form_class = CustomerProfileForm
    elif user_type == 'receptionist':
        user = get_object_or_404(Receptionist, pk=user_id)
        form_class = ReceptionistProfileForm
    elif user_type == 'mechanic':
        user = get_object_or_404(Mechanic, pk=user_id)
        form_class = MechanicProfileForm
    elif user_type == 'inventory_manager':
        user = get_object_or_404(InventoryManager, pk=user_id)
        form_class = InventoryManagerProfileForm
    else:
        messages.error(request, 'Invalid user type.')
        return redirect('vmsms:user_list')
    
    if request.method == 'POST':
        form = form_class(request.POST, instance=user)
        if form.is_valid():
            user = form.save(commit=False)
            # Handle additional fields
            user.surname = form.cleaned_data.get('surname', '')
            user.phone_number = form.cleaned_data.get('phone_number', '')
            user.address = form.cleaned_data.get('address', '')
            if user_type == 'mechanic':
                user.service_fee = form.cleaned_data.get('service_fee')
                user.specialization_code = form.cleaned_data.get('specialization_code', '')
            user.save()
            messages.success(request, f'{user_type.title()} profile updated successfully!')
            # Use correct id field for redirect
            if user_type == 'admin':
                redirect_id = getattr(user, 'admin_id', None) or getattr(user, 'id', None)
            elif user_type == 'customer':
                redirect_id = getattr(user, 'customer_id', None) or getattr(user, 'id', None)
            elif user_type == 'receptionist':
                redirect_id = getattr(user, 'receptionist_id', None) or getattr(user, 'id', None)
            elif user_type == 'mechanic':
                redirect_id = getattr(user, 'mechanic_id', None) or getattr(user, 'id', None)
            elif user_type == 'inventory_manager':
                redirect_id = getattr(user, 'inventory_manager_id', None) or getattr(user, 'id', None)
            else:
                redirect_id = user_id
            return redirect('vmsms:user_detail', user_type=user_type, user_id=redirect_id)
    else:
        form = form_class(instance=user)
        # Set initial values for additional fields
        form.initial['surname'] = getattr(user, 'surname', '')
        form.initial['phone_number'] = getattr(user, 'phone_number', '')
        form.initial['address'] = getattr(user, 'address', '')
        if user_type == 'mechanic':
            form.initial['service_fee'] = getattr(user, 'service_fee', '')
            form.initial['specialization_code'] = getattr(user, 'specialization_code', '')
    
    return render(request, 'vmsms/user_edit.html', {
        'form': form,
        'user': user,
        'user_type': user_type,
        'user_id': user_id,
        'admin_user_type': admin_user_type,
    })

def user_delete(request, user_type, user_id):
    admin_user_type = request.session.get('user_type')
    if admin_user_type not in ['admin', 'receptionist', 'mechanic']:
        messages.error(request, 'Access denied. Admin, receptionist, or mechanic privileges required.')
        return redirect('vmsms:login')
    
    # Non-admin users can only delete customer accounts
    if admin_user_type != 'admin' and user_type != 'customer':
        messages.error(request, 'Access denied. You can only delete customer accounts.')
        return redirect('vmsms:user_list')
    
    # Get the appropriate model based on user type
    if user_type == 'admin':
        user = get_object_or_404(Admin, pk=user_id)
    elif user_type == 'customer':
        user = get_object_or_404(Customer, pk=user_id)
    elif user_type == 'receptionist':
        user = get_object_or_404(Receptionist, pk=user_id)
    elif user_type == 'mechanic':
        user = get_object_or_404(Mechanic, pk=user_id)
    elif user_type == 'inventory_manager':
        user = get_object_or_404(InventoryManager, pk=user_id)
    else:
        messages.error(request, 'Invalid user type.')
        return redirect('vmsms:user_list')
    
    if request.method == 'POST':
        # Delete the user
        user.delete()
        messages.success(request, f'{user_type.title()} deleted successfully!')
        return redirect('vmsms:user_list')
    
    return render(request, 'vmsms/user_confirm_delete.html', {
        'user': user,
        'user_type': user_type,
        'user_id': user_id,
        'admin_user_type': admin_user_type,
    })

def diagnose_test(request, test_id):
    """Diagnose test - update test result and diagnosis"""
    test = get_object_or_404(Test, pk=test_id)
    user_type = request.session.get('user_type')
    user_id = request.session.get('user_id')
    
    # Only mechanics can diagnose tests, and only their own tests
    if user_type != 'mechanic':
        messages.error(request, 'Only mechanics can diagnose tests.')
        return redirect('vmsms:test_list')
    
    # Check if this test is assigned to this mechanic
    appointment = Appointment.objects.filter(test=test, mechanic_id=user_id).first()
    if not appointment:
        messages.error(request, 'You can only diagnose tests assigned to you.')
        return redirect('vmsms:test_list')
    
    if request.method == 'POST':
        form = DiagnoseTestForm(request.POST, instance=test.test_result)
        if form.is_valid():
            # Update test result
            test_result = form.save()
            
            # Update test diagnosis
            test.diagnosis = form.cleaned_data['diagnosis']
            test.save()
            
            # Mark test as completed in appointment
            appointment.test_completed = True
            appointment.save()
            
            messages.success(request, 'Test diagnosed successfully!')
            return redirect('vmsms:test_list')
    else:
        form = DiagnoseTestForm(instance=test.test_result)
        form.initial['diagnosis'] = test.diagnosis or ''
    
    return render(request, 'vmsms/diagnose_test.html', {
        'form': form,
        'test': test,
        'appointment': appointment,
    })

def suggest_repair(request, test_id):
    """Suggest repair based on test diagnosis"""
    test = get_object_or_404(Test, pk=test_id)
    user_type = request.session.get('user_type')
    user_id = request.session.get('user_id')
    
    # Only mechanics can suggest repairs, and only for their own tests
    if user_type != 'mechanic':
        messages.error(request, 'Only mechanics can suggest repairs.')
        return redirect('vmsms:test_list')
    
    # Check if this test is assigned to this mechanic and has a diagnosis
    appointment = Appointment.objects.filter(test=test, mechanic_id=user_id).first()
    if not appointment:
        messages.error(request, 'You can only suggest repairs for tests assigned to you.')
        return redirect('vmsms:test_list')
    
    if not test.diagnosis:
        messages.error(request, 'Test must be diagnosed before suggesting a repair.')
        return redirect('vmsms:diagnose_test', test_id=test_id)
    
    if request.method == 'POST':
        form = SuggestRepairForm(request.POST)
        if form.is_valid():
            # Create a new repair appointment
            from .models import Repair, Invoices
            import datetime
            
            # Create invoice for the repair
            invoice = Invoices.objects.create(
                invoice_date=datetime.date.today(),
                amount_due=form.cleaned_data['estimated_cost'],
                payment_status='Pending'
            )
            
            # Create repair record
            repair = Repair.objects.create(
                repair_code=f"REP_{test_id}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}",
                mechanic_id=user_id,
                vehicle=appointment.vehicle,
                vehicle_insurance=appointment.vehicle.insurance,
                repair_name=form.cleaned_data['repair_name'],
                repair_date=datetime.date.today(),
                repair_cost=form.cleaned_data['estimated_cost']
            )
            
            # Create new repair appointment
            repair_appointment = Appointment.objects.create(
                appointment_id=f"REP_{test_id}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}",
                appointment_time=appointment.appointment_time + datetime.timedelta(hours=1),  # Schedule 1 hour after test
                vehicle=appointment.vehicle,
                mechanic_id=user_id,
                repair=repair,
                invoice=invoice,
                customer=appointment.customer,
                service_type='repair'
            )
            
            messages.success(request, f'Repair suggested successfully! Repair appointment created with ID: {repair_appointment.appointment_id}')
            return redirect('vmsms:appointment_list')
    else:
        form = SuggestRepairForm()
    
    return render(request, 'vmsms/suggest_repair.html', {
        'form': form,
        'test': test,
        'appointment': appointment,
    })
