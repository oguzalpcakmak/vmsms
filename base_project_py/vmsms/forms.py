from django import forms
from .models import Admin, Receptionist, Mechanic, InventoryManager, Customer, Appointment, Test, TestResult, Invoices, Vehicle, Insurance
from django.core.exceptions import ValidationError
import datetime
import uuid

USER_TYPE_CHOICES = [
    ('customer', 'Customer'),
]

class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your password'}))

class AdminRegistrationForm(forms.ModelForm):
    surname = forms.CharField(max_length=255, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your surname'}))
    phone_number = forms.CharField(max_length=15, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your phone number'}))
    address = forms.CharField(max_length=255, required=False, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter your address'}))
    
    class Meta:
        model = Admin
        fields = ['username', 'password', 'name', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your username'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your password'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your first name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email address'}),
        }

class ReceptionistRegistrationForm(forms.ModelForm):
    surname = forms.CharField(max_length=255, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your surname'}))
    phone_number = forms.CharField(max_length=15, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your phone number'}))
    address = forms.CharField(max_length=255, required=False, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter your address'}))
    
    class Meta:
        model = Receptionist
        fields = ['username', 'password', 'name', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your username'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your password'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your first name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email address'}),
        }

class MechanicRegistrationForm(forms.ModelForm):
    surname = forms.CharField(max_length=255, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your surname'}))
    phone_number = forms.CharField(max_length=15, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your phone number'}))
    address = forms.CharField(max_length=255, required=False, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter your address'}))
    service_fee = forms.DecimalField(max_digits=10, decimal_places=2, required=False, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter service fee (optional)'}))
    specialization_code = forms.CharField(max_length=10, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter specialization code (optional)'}))
    
    class Meta:
        model = Mechanic
        fields = ['username', 'password', 'name', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your username'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your password'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your first name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email address'}),
        }

class InventoryManagerRegistrationForm(forms.ModelForm):
    surname = forms.CharField(max_length=255, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your surname'}))
    phone_number = forms.CharField(max_length=15, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your phone number'}))
    address = forms.CharField(max_length=255, required=False, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter your address'}))
    
    class Meta:
        model = InventoryManager
        fields = ['username', 'password', 'name', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your username'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your password'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your first name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email address'}),
        }

class CustomerRegistrationForm(forms.ModelForm):
    surname = forms.CharField(max_length=255, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your surname'}))
    phone_number = forms.CharField(max_length=15, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your phone number'}))
    address = forms.CharField(max_length=255, required=False, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter your address'}))
    
    class Meta:
        model = Customer
        fields = ['username', 'password', 'name', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your username'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your password'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your first name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email address'}),
        }

class AppointmentForm(forms.ModelForm):
    service_type = forms.ChoiceField(
        choices=[('repair', 'Repair'), ('test', 'Test')],
        label="Service Type",
        help_text="Choose whether this appointment is for a repair or a test"
    )
    
    # Static choices for repair types
    REPAIR_CHOICES = [
        ('oil_change', 'Oil Change and Filter Replacement'),
        ('brake_pads', 'Brake Pad Replacement'),
        ('battery', 'Battery Replacement'),
        ('engine_tuneup', 'Engine Tune-up'),
        ('tire_rotation', 'Tire Rotation and Balance'),
        ('air_filter', 'Air Filter Replacement'),
        ('spark_plugs', 'Spark Plug Replacement'),
        ('transmission', 'Transmission Service'),
        ('coolant', 'Cooling System Service'),
        ('brake_fluid', 'Brake Fluid Replacement'),
    ]
    
    # Static choices for test types
    TEST_CHOICES = [
        ('engine_performance', 'Engine Performance Test'),
        ('brake_system', 'Brake System Test'),
        ('electrical', 'Electrical System Test'),
        ('emission', 'Emission Test'),
        ('transmission', 'Transmission Test'),
        ('battery', 'Battery Test'),
        ('alignment', 'Wheel Alignment Test'),
        ('compression', 'Engine Compression Test'),
        ('cooling', 'Cooling System Test'),
        ('fuel_system', 'Fuel System Test'),
    ]
    
    repair_type = forms.ChoiceField(
        choices=REPAIR_CHOICES,
        required=False,
        label="Repair Type",
        help_text="Select the type of repair needed"
    )
    
    test_type = forms.ChoiceField(
        choices=TEST_CHOICES,
        required=False,
        label="Test Type",
        help_text="Select the type of test needed"
    )
    
    # Custom date and time fields
    appointment_date = forms.DateField(
        label="Appointment Date",
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control',
            'min': datetime.date.today().isoformat()
        })
    )
    
    appointment_time = forms.ChoiceField(
        label="Appointment Time",
        choices=[
            ('08:40', '08:40'),
            ('09:30', '09:30'),
            ('10:20', '10:20'),
            ('11:10', '11:10'),
            ('12:00', '12:00'),
            ('12:50', '12:50'),
            ('13:40', '13:40'),
            ('14:30', '14:30'),
            ('15:20', '15:20'),
            ('16:10', '16:10'),
            ('17:00', '17:00'),
        ],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    class Meta:
        model = Appointment
        fields = ['customer', 'vehicle', 'mechanic', 'service_type', 'test_completed', 'repair_approved']
        widgets = {
            'test_completed': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'repair_approved': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remove the original repair and test fields from the form
        if 'repair' in self.fields:
            del self.fields['repair']
        if 'test' in self.fields:
            del self.fields['test']
        
        # Make test_completed and repair_approved read-only for non-admin users
        user_type = kwargs.get('initial', {}).get('user_type', '')
        if user_type not in ['admin', 'mechanic']:
            self.fields['test_completed'].widget.attrs['readonly'] = True
            self.fields['repair_approved'].widget.attrs['readonly'] = True

    def clean(self):
        cleaned_data = super().clean()
        service_type = cleaned_data.get('service_type')
        repair_type = cleaned_data.get('repair_type')
        test_type = cleaned_data.get('test_type')
        appointment_date = cleaned_data.get('appointment_date')
        appointment_time = cleaned_data.get('appointment_time')
        mechanic = cleaned_data.get('mechanic')
        customer = cleaned_data.get('customer')
        test_completed = cleaned_data.get('test_completed', False)
        repair_approved = cleaned_data.get('repair_approved', False)
        
        # Combine date and time into datetime
        if appointment_date and appointment_time:
            try:
                time_obj = datetime.datetime.strptime(appointment_time, '%H:%M').time()
                combined_datetime = datetime.datetime.combine(appointment_date, time_obj)
                cleaned_data['appointment_time'] = combined_datetime
            except ValueError:
                raise ValidationError('Invalid time format.')
        
        # Validate service type selection
        if service_type == 'repair' and not repair_type:
            raise ValidationError('Please select a repair type when service type is "Repair".')
        elif service_type == 'test' and not test_type:
            raise ValidationError('Please select a test type when service type is "Test".')
        
        # Validate that repairs cannot be approved without completed tests
        if service_type == 'repair' and repair_approved and not test_completed:
            raise ValidationError('Repairs cannot be approved without completed tests. Please complete the test first.')
        
        # Check for double-booking
        if appointment_date and appointment_time and mechanic:
            combined_datetime = cleaned_data.get('appointment_time')
            if combined_datetime:
                qs = Appointment.objects.filter(appointment_time=combined_datetime, mechanic=mechanic)
                if self.instance.pk:
                    qs = qs.exclude(pk=self.instance.pk)
                if qs.exists():
                    raise ValidationError('This mechanic is already booked at the selected time.')
        
        # Filter vehicle choices based on selected customer
        if customer:
            self.fields['vehicle'].queryset = Vehicle.objects.filter(customer=customer)
        
        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        
        # Set the appointment_time from the combined date and time
        if self.cleaned_data.get('appointment_time'):
            instance.appointment_time = self.cleaned_data['appointment_time']
        
        # Generate appointment ID
        instance.appointment_id = f"APT-{uuid.uuid4().hex[:8].upper()}"
        
        # Create a default invoice for the appointment
        invoice = Invoices.objects.create(
            invoice_date=instance.appointment_time.date(),
            amount_due=0.00,
            payment_status='Pending',
        )
        instance.invoice = invoice
        
        if commit:
            instance.save()
        return instance

class TestForm(forms.ModelForm):
    class Meta:
        model = Test
        fields = ['test_name', 'normal_value', 'diagnosis', 'test_unit_price', 'test_result', 'component_name']

class TestResultForm(forms.ModelForm):
    class Meta:
        model = TestResult
        fields = ['value']
        widgets = {
            'value': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }

class TestUpdateForm(forms.ModelForm):
    class Meta:
        model = Test
        fields = ['test_name', 'normal_value', 'diagnosis', 'test_unit_price', 'component_name']
        widgets = {
            'test_name': forms.TextInput(attrs={'class': 'form-control'}),
            'normal_value': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'diagnosis': forms.TextInput(attrs={'class': 'form-control'}),
            'test_unit_price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'component_name': forms.TextInput(attrs={'class': 'form-control'}),
        }

class RepairApprovalForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['test_completed', 'repair_approved']
        widgets = {
            'test_completed': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'repair_approved': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        test_completed = cleaned_data.get('test_completed', False)
        repair_approved = cleaned_data.get('repair_approved', False)
        
        # Validate that repairs cannot be approved without completed tests
        if repair_approved and not test_completed:
            raise ValidationError('Repairs cannot be approved without completed tests. Please mark the test as completed first.')
        
        return cleaned_data

class InvoiceForm(forms.ModelForm):
    appointment = forms.ModelChoiceField(
        queryset=Appointment.objects.filter(invoice__isnull=True),
        label="Appointment",
        help_text="Select an appointment that doesn't have an invoice yet"
    )
    
    class Meta:
        model = Invoices
        fields = ['invoice_date', 'amount_due', 'payment_status', 'payment_date']
        widgets = {
            'invoice_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control',
                'value': datetime.date.today().isoformat()
            }),
            'amount_due': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter amount due',
                'step': '0.01',
                'min': '0',
                'readonly': 'readonly'
            }),
            'payment_status': forms.Select(attrs={
                'class': 'form-control'
            }),
            'payment_date': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'form-control'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set default values
        if not self.instance.pk:
            self.fields['invoice_date'].initial = datetime.date.today()
            self.fields['payment_status'].initial = 'Pending'
        
        # Calculate default amount based on appointment
        if 'appointment' in self.data:
            try:
                appointment_id = self.data.get('appointment')
                if appointment_id:
                    appointment = Appointment.objects.get(id=appointment_id)
                    # Calculate amount based on service type and tests
                    amount = 0.0
                    if appointment.service_type == 'test':
                        # Base test fee
                        amount = 50.0
                        # Add test costs if any
                        if appointment.test:
                            amount += float(appointment.test.test_unit_price or 0)
                    else:
                        # Base repair fee
                        amount = 100.0
                        # Add mechanic service fee if available
                        if appointment.mechanic and appointment.mechanic.service_fee:
                            amount += float(appointment.mechanic.service_fee)
                    
                    self.fields['amount_due'].initial = amount
            except Appointment.DoesNotExist:
                pass
    
    def clean(self):
        cleaned_data = super().clean()
        payment_status = cleaned_data.get('payment_status')
        payment_date = cleaned_data.get('payment_date')
        
        # If payment status is 'Paid', payment date should be set
        if payment_status == 'Paid' and not payment_date:
            cleaned_data['payment_date'] = datetime.datetime.now()
        
        return cleaned_data

class VehicleForm(forms.ModelForm):
    has_insurance = forms.BooleanField(required=False, label="Does this vehicle have insurance?")
    insurance_company = forms.CharField(max_length=45, required=False, label="Insurance Company")
    insurance_coverage = forms.DecimalField(max_digits=5, decimal_places=2, required=False, label="Coverage (%)")
    insurance_number = forms.IntegerField(required=False, label="Insurance Number", 
                                        min_value=-2147483648, max_value=2147483647,
                                        help_text="Enter a number between -2,147,483,648 and 2,147,483,647")

    class Meta:
        model = Vehicle
        fields = ['license_plate', 'model', 'year', 'vin_number']
        widgets = {
            'year': forms.NumberInput(attrs={'min': 1900, 'max': 2030}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Hide insurance fields by default in the form
        self.fields['insurance_company'].widget.attrs['class'] = 'insurance-field'
        self.fields['insurance_coverage'].widget.attrs['class'] = 'insurance-field'
        self.fields['insurance_number'].widget.attrs['class'] = 'insurance-field'

    def clean(self):
        cleaned_data = super().clean()
        has_insurance = cleaned_data.get('has_insurance')
        if has_insurance:
            if not cleaned_data.get('insurance_company') or cleaned_data.get('insurance_coverage') is None or cleaned_data.get('insurance_number') is None:
                raise ValidationError('Please provide all insurance details.')
        return cleaned_data

    def clean_insurance_number(self):
        insurance_number = self.cleaned_data.get('insurance_number')
        if insurance_number is not None:
            # Check if the number is within MySQL INT range
            if insurance_number < -2147483648 or insurance_number > 2147483647:
                raise ValidationError('Insurance number must be between -2,147,483,648 and 2,147,483,647.')
        return insurance_number

    def clean_license_plate(self):
        license_plate = self.cleaned_data['license_plate']
        # Check if license plate already exists
        if Vehicle.objects.filter(license_plate=license_plate).exclude(pk=self.instance.pk if self.instance else None).exists():
            raise ValidationError('A vehicle with this license plate already exists.')
        return license_plate

    def clean_vin_number(self):
        vin_number = self.cleaned_data['vin_number']
        if vin_number:
            # Check if VIN already exists
            if Vehicle.objects.filter(vin_number=vin_number).exclude(pk=self.instance.pk if self.instance else None).exists():
                raise ValidationError('A vehicle with this VIN number already exists.')
        return vin_number

    def save(self, commit=True, customer=None):
        instance = super().save(commit=False)
        has_insurance = self.cleaned_data.get('has_insurance')
        if has_insurance:
            from .models import Insurance
            insurance, created = Insurance.objects.get_or_create(
                insurance_number=self.cleaned_data['insurance_number'],
                defaults={
                    'company': self.cleaned_data['insurance_company'],
                    'coverage': self.cleaned_data['insurance_coverage'],
                }
            )
            instance.insurance = insurance
        else:
            instance.insurance = None
        if customer:
            instance.customer_id = customer
        if commit:
            instance.save()
        return instance

# User Profile Edit Forms
class AdminProfileForm(forms.ModelForm):
    surname = forms.CharField(max_length=255, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your surname'}))
    phone_number = forms.CharField(max_length=15, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your phone number'}))
    address = forms.CharField(max_length=255, required=False, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter your address'}))
    
    class Meta:
        model = Admin
        fields = ['name', 'email']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your first name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email address'}),
        }

class ReceptionistProfileForm(forms.ModelForm):
    surname = forms.CharField(max_length=255, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your surname'}))
    phone_number = forms.CharField(max_length=15, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your phone number'}))
    address = forms.CharField(max_length=255, required=False, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter your address'}))
    
    class Meta:
        model = Receptionist
        fields = ['name', 'email']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your first name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email address'}),
        }

class MechanicProfileForm(forms.ModelForm):
    surname = forms.CharField(max_length=255, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your surname'}))
    phone_number = forms.CharField(max_length=15, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your phone number'}))
    address = forms.CharField(max_length=255, required=False, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter your address'}))
    service_fee = forms.DecimalField(max_digits=10, decimal_places=2, required=False, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter service fee (optional)'}))
    specialization_code = forms.CharField(max_length=10, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter specialization code (optional)'}))
    
    class Meta:
        model = Mechanic
        fields = ['name', 'email']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your first name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email address'}),
        }

class InventoryManagerProfileForm(forms.ModelForm):
    surname = forms.CharField(max_length=255, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your surname'}))
    phone_number = forms.CharField(max_length=15, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your phone number'}))
    address = forms.CharField(max_length=255, required=False, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter your address'}))
    
    class Meta:
        model = InventoryManager
        fields = ['name', 'email']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your first name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email address'}),
        }

class CustomerProfileForm(forms.ModelForm):
    surname = forms.CharField(max_length=255, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your surname'}))
    phone_number = forms.CharField(max_length=15, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your phone number'}))
    address = forms.CharField(max_length=255, required=False, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter your address'}))
    
    class Meta:
        model = Customer
        fields = ['name', 'email']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your first name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email address'}),
        }

class TestCreateForm(forms.ModelForm):
    class Meta:
        model = Test
        fields = ['test_name', 'test_unit_price', 'component_name']
        widgets = {
            'test_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter test name'}),
            'test_unit_price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter unit price'}),
            'component_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter component name'}),
        }

class SuggestRepairForm(forms.Form):
    repair_name = forms.CharField(
        max_length=200,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter repair name (e.g., Brake Pad Replacement)'})
    )
    estimated_cost = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=True,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter estimated cost'})
    )
    required_parts = forms.CharField(
        max_length=500,
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'List required parts (e.g., Brake pads, Rotors, Brake fluid)'})
    )
    notes = forms.CharField(
        max_length=1000,
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Additional notes about the repair'})
    )

class DiagnoseTestForm(forms.ModelForm):
    diagnosis = forms.CharField(
        max_length=200, 
        required=True,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter diagnosis (e.g., Brake pads worn, Oil leak detected)'})
    )
    
    class Meta:
        model = TestResult
        fields = ['value']
        widgets = {
            'value': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter test result value'}),
        }

class ChangePasswordForm(forms.Form):
    current_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your current password'
        }),
        label="Current Password"
    )
    new_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your new password'
        }),
        label="New Password"
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm your new password'
        }),
        label="Confirm New Password"
    )

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')
        
        if new_password and confirm_password:
            if new_password != confirm_password:
                raise ValidationError("New passwords don't match.")
            
            if len(new_password) < 8:
                raise ValidationError("New password must be at least 8 characters long.")
        
        return cleaned_data 