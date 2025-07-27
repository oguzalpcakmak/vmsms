from django.db import models
from django.contrib.auth.models import AbstractUser

# User models
class Admin(models.Model):
    admin_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)
    name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.name} {self.surname or ''} (Admin)"

class Receptionist(models.Model):
    receptionist_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)
    name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.name} {self.surname or ''} (Receptionist)"

class Mechanic(models.Model):
    mechanic_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)
    name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    service_fee = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    specialization_code = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return f"{self.name} {self.surname or ''} (Mechanic)"

class InventoryManager(models.Model):
    inventory_manager_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)
    name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.name} {self.surname or ''} (Inventory Manager)"

class Customer(models.Model):
    customer_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)
    name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.name} {self.surname or ''} (Customer)"

# Core entities
class Insurance(models.Model):
    insurance_number = models.IntegerField(primary_key=True)
    coverage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    company = models.CharField(max_length=45, null=True, blank=True)

    def __str__(self):
        return f"{self.company} - {self.insurance_number}"

class Specialization(models.Model):
    specialization_code = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=120, null=True, blank=True)

class Vehicle(models.Model):
    license_plate = models.CharField(max_length=10, primary_key=True)
    model = models.CharField(max_length=100, null=True, blank=True)
    year = models.IntegerField(null=True, blank=True)
    vin_number = models.CharField(max_length=50, unique=True, null=True, blank=True)
    insurance = models.ForeignKey(Insurance, on_delete=models.PROTECT, null=True, blank=True)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.license_plate} - {self.model}"

class MechanicSchedule(models.Model):
    mechanic = models.OneToOneField(Mechanic, on_delete=models.CASCADE, primary_key=True)
    date = models.DateField(null=True, blank=True)
    time = models.TimeField(null=True, blank=True)
    availability = models.CharField(max_length=45, null=True, blank=True)

# More models to be added for Appointment, Repair, Test, etc.

class Repair(models.Model):
    repair_code = models.CharField(max_length=45)
    mechanic = models.ForeignKey('Mechanic', on_delete=models.CASCADE)
    vehicle = models.ForeignKey('Vehicle', to_field='license_plate', on_delete=models.CASCADE)
    vehicle_insurance = models.ForeignKey('Insurance', on_delete=models.CASCADE)
    repair_name = models.CharField(max_length=120, null=True, blank=True)
    repair_date = models.DateField(null=True, blank=True)
    repair_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"{self.repair_code} - {self.repair_name}"

    class Meta:
        unique_together = ('repair_code', 'mechanic', 'vehicle', 'vehicle_insurance')

class Invoices(models.Model):
    invoice_id = models.AutoField(primary_key=True)
    invoice_date = models.DateField(null=True, blank=True)
    amount_due = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    payment_status = models.CharField(max_length=10, choices=[('Paid','Paid'),('Pending','Pending'),('Overdue','Overdue')], null=True, blank=True)
    payment_date = models.DateTimeField(null=True, blank=True)

class TestResult(models.Model):
    test_result_id = models.AutoField(primary_key=True)
    value = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

class Test(models.Model):
    test_id = models.AutoField(primary_key=True)
    test_name = models.CharField(max_length=200, null=True, blank=True)
    normal_value = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    diagnosis = models.CharField(max_length=45, null=True, blank=True)
    test_unit_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    test_result = models.ForeignKey(TestResult, on_delete=models.CASCADE)
    component_name = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return f"{self.test_name} ({self.component_name})"

class Appointment(models.Model):
    appointment_id = models.CharField(max_length=45)
    appointment_time = models.DateTimeField()
    vehicle = models.ForeignKey('Vehicle', to_field='license_plate', on_delete=models.CASCADE)
    mechanic = models.ForeignKey('Mechanic', on_delete=models.CASCADE)
    repair = models.ForeignKey('Repair', on_delete=models.CASCADE, null=True, blank=True)
    invoice = models.ForeignKey('Invoices', on_delete=models.CASCADE)
    test = models.ForeignKey('Test', on_delete=models.CASCADE, null=True, blank=True)
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE)
    service_type = models.CharField(max_length=10, choices=[('repair', 'Repair'), ('test', 'Test')], default='repair')
    test_completed = models.BooleanField(default=False)
    repair_approved = models.BooleanField(default=False)

    class Meta:
        unique_together = ('vehicle', 'mechanic', 'invoice', 'appointment_id', 'customer')

class SpareParts(models.Model):
    spare_part_id = models.AutoField(primary_key=True)
    quantity_in_stock = models.IntegerField(null=True, blank=True)
    name = models.CharField(max_length=120, null=True, blank=True)
    unit_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

class Supplier(models.Model):
    supplier_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    contact_info = models.TextField(null=True, blank=True)

class Vehicle_has_Mechanic(models.Model):
    vehicle = models.ForeignKey('Vehicle', to_field='license_plate', on_delete=models.CASCADE)
    mechanic = models.ForeignKey('Mechanic', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('vehicle', 'mechanic')

class SparePart_has_Supplier(models.Model):
    spare_part = models.ForeignKey('SpareParts', on_delete=models.CASCADE)
    supplier = models.ForeignKey('Supplier', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('spare_part', 'supplier')

class Repair_has_SpareParts(models.Model):
    repair = models.ForeignKey('Repair', on_delete=models.CASCADE)
    spare_part = models.ForeignKey('SpareParts', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('repair', 'spare_part')

class VehicleComponent(models.Model):
    component_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200, null=True, blank=True)

class Component_has_Test(models.Model):
    component = models.ForeignKey('VehicleComponent', on_delete=models.CASCADE)
    test = models.ForeignKey('Test', on_delete=models.CASCADE)
    test_result = models.ForeignKey('TestResult', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('component', 'test', 'test_result')
