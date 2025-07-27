from django.core.management.base import BaseCommand
from django.db import transaction
from vmsms.models import Admin, Receptionist, Mechanic, InventoryManager, Customer, Vehicle, Insurance, Appointment, Test, TestResult, Repair, Invoices, SpareParts, Supplier, Repair_has_SpareParts
from decimal import Decimal
import random
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = 'Generate comprehensive sample data for VMSMS including users, vehicles, appointments, tests, and invoices'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing data before generating new data',
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write('Clearing existing data...')
            self.clear_data()
        
        self.stdout.write('Generating comprehensive sample data...')
        
        with transaction.atomic():
            # Create users
            self.create_users()
            
            # Create vehicles and insurance
            self.create_vehicles_and_insurance()
            
            # Create appointments
            self.create_appointments()
            
            # Create tests and results
            self.create_tests_and_results()
            
            # Create repairs and spare parts
            self.create_repairs_and_spare_parts()
        
        self.stdout.write(self.style.SUCCESS('Successfully generated comprehensive sample data!'))
        self.stdout.write('Sample users created:')
        self.stdout.write('- admin (password: 1234)')
        self.stdout.write('- Mechanic_1 (password: 1234)')
        self.stdout.write('- Receptionist_1 (password: 1234)')
        self.stdout.write('- Inventory_Manager_1 (password: 1234)')
        self.stdout.write('- Customer_1 (password: 1234)')

    def clear_data(self):
        """Clear all existing data"""
        Invoices.objects.all().delete()
        Repair_has_SpareParts.objects.all().delete()
        Repair.objects.all().delete()
        TestResult.objects.all().delete()
        Test.objects.all().delete()
        Appointment.objects.all().delete()
        Vehicle.objects.all().delete()
        Insurance.objects.all().delete()
        SpareParts.objects.all().delete()
        Supplier.objects.all().delete()
        Customer.objects.all().delete()
        Mechanic.objects.all().delete()
        Receptionist.objects.all().delete()
        InventoryManager.objects.all().delete()
        Admin.objects.all().delete()

    def create_users(self):
        """Create sample users with specific format"""
        # Create admin
        admin = Admin.objects.create(
            username='admin',
            password='1234',
            name='John',
            surname='Doe',
            email='admin@vmsms.com',
            phone_number='555-0101',
            address='123 Admin St, City'
        )
        
        # Create additional admins with diverse names
        admin_first_names = ['Michael', 'Jennifer', 'Robert', 'Lisa', 'William', 'Patricia', 'David', 'Linda']
        admin_last_names = ['Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis', 'Rodriguez']
        
        for i in range(2, 6):
            Admin.objects.create(
                username=f'admin{i}',
                password='1234',
                name=random.choice(admin_first_names),
                surname=random.choice(admin_last_names),
                email=f'admin{i}@vmsms.com',
                phone_number=f'555-010{i}',
                address=f'{123+i} Admin St, City'
            )
        
        # Create mechanic
        mechanic = Mechanic.objects.create(
            username='Mechanic_1',
            password='1234',
            name='John',
            surname='Doe',
            email='mechanic1@vmsms.com',
            phone_number='555-0201',
            address='456 Mechanic Ave, City',
            specialization_code='ENG001'
        )
        
        # Create additional mechanics with diverse names
        mechanic_first_names = ['Alex', 'Bob', 'Charlie', 'Diana', 'Eve', 'Frank', 'Grace', 'Henry', 'Ivy', 'Jack', 'Kate', 'Liam', 'Maya', 'Noah', 'Olivia']
        mechanic_last_names = ['Anderson', 'Baker', 'Clark', 'Davis', 'Evans', 'Fisher', 'Green', 'Harris', 'Irwin', 'Jackson', 'King', 'Lewis', 'Moore', 'Nelson', 'Owen']
        specializations = ['ENG', 'BRAK', 'ELEC', 'TRAN', 'COOL', 'FUEL', 'SUSP', 'EXHA', 'ENG', 'BRAK', 'ELEC', 'TRAN', 'COOL', 'FUEL', 'SUSP']
        
        for i in range(2, 16):
            Mechanic.objects.create(
                username=f'Mechanic_{i}',
                password='1234',
                name=random.choice(mechanic_first_names),
                surname=random.choice(mechanic_last_names),
                email=f'mechanic{i}@vmsms.com',
                phone_number=f'555-02{i:02d}',
                address=f'{456+i} Mechanic Ave, City',
                specialization_code=random.choice(specializations)
            )
        
        # Create receptionist
        receptionist = Receptionist.objects.create(
            username='Receptionist_1',
            password='1234',
            name='John',
            surname='Doe',
            email='receptionist1@vmsms.com',
            phone_number='555-0301',
            address='789 Reception Blvd, City'
        )
        
        # Create additional receptionists with diverse names
        receptionist_first_names = ['Alice', 'Betty', 'Carol', 'Doris', 'Eva', 'Fiona', 'Gina', 'Helen', 'Iris', 'Judy']
        receptionist_last_names = ['Wilson', 'Taylor', 'Moore', 'Jackson', 'Martin', 'Lee', 'Perez', 'Thompson', 'White', 'Young']
        
        for i in range(2, 11):
            Receptionist.objects.create(
                username=f'Receptionist_{i}',
                password='1234',
                name=random.choice(receptionist_first_names),
                surname=random.choice(receptionist_last_names),
                email=f'receptionist{i}@vmsms.com',
                phone_number=f'555-03{i:02d}',
                address=f'{789+i} Reception Blvd, City'
            )
        
        # Create inventory manager
        inventory_manager = InventoryManager.objects.create(
            username='Inventory_Manager_1',
            password='1234',
            name='John',
            surname='Doe',
            email='inventory1@vmsms.com',
            phone_number='555-0401',
            address='321 Inventory Rd, City'
        )
        
        # Create additional inventory managers with diverse names
        inventory_first_names = ['Paul', 'Rachel', 'Steve', 'Tina', 'Victor', 'Wendy', 'Xavier', 'Yvonne']
        inventory_last_names = ['Adams', 'Baker', 'Cooper', 'Dixon', 'Edwards', 'Foster', 'Gordon', 'Hill']
        
        for i in range(2, 9):
            InventoryManager.objects.create(
                username=f'Inventory_Manager_{i}',
                password='1234',
                name=random.choice(inventory_first_names),
                surname=random.choice(inventory_last_names),
                email=f'inventory{i}@vmsms.com',
                phone_number=f'555-04{i:02d}',
                address=f'{321+i} Inventory Rd, City'
            )
        
        # Create customer
        customer = Customer.objects.create(
            username='Customer_1',
            password='1234',
            name='John',
            surname='Doe',
            email='customer1@vmsms.com',
            phone_number='555-0501',
            address='654 Customer Ln, City'
        )
        
        # Create additional customers with diverse names
        customer_first_names = ['John', 'Jane', 'Mike', 'Sarah', 'David', 'Lisa', 'Tom', 'Emma', 'Chris', 'Anna', 'Mark', 'Mary', 'James', 'Linda', 'Peter', 'Susan', 'Andrew', 'Karen', 'Daniel', 'Nancy', 'Matthew', 'Betty', 'Anthony', 'Helen', 'Kevin']
        customer_last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis', 'Rodriguez', 'Martinez', 'Hernandez', 'Lopez', 'Gonzalez', 'Wilson', 'Anderson', 'Thomas', 'Taylor', 'Moore', 'Jackson', 'Martin', 'Lee', 'Perez', 'Thompson', 'White', 'Harris']
        
        for i in range(2, 26):
            Customer.objects.create(
                username=f'Customer_{i}',
                password='1234',
                name=random.choice(customer_first_names),
                surname=random.choice(customer_last_names),
                email=f'customer{i}@vmsms.com',
                phone_number=f'555-05{i:02d}',
                address=f'{654+i} Customer Ln, City'
            )
        
        self.stdout.write('Created users successfully')

    def create_vehicles_and_insurance(self):
        """Create vehicles and insurance data"""
        customers = Customer.objects.all()
        
        # Create insurance companies
        insurance_companies = [
            'Allstate Insurance',
            'State Farm',
            'Geico',
            'Progressive',
            'Liberty Mutual',
            'Nationwide',
            'Farmers Insurance',
            'American Family'
        ]
        
        # Create diverse vehicle models
        vehicle_models = [
            'Toyota Camry', 'Honda Civic', 'Ford Focus', 'Nissan Altima', 'Chevrolet Malibu',
            'Hyundai Sonata', 'Kia Optima', 'Mazda 6', 'Subaru Legacy', 'Volkswagen Passat',
            'Toyota Corolla', 'Honda Accord', 'Ford Fusion', 'Nissan Sentra', 'Chevrolet Cruze',
            'Hyundai Elantra', 'Kia Forte', 'Mazda 3', 'Subaru Impreza', 'Volkswagen Jetta'
        ]
        
        # Create 50 vehicles with diverse data
        used_plates = set()
        for i in range(50):
            customer = random.choice(customers)
            
            # Generate unique license plate
            while True:
                plate = f'{random.choice(["ABC", "DEF", "GHI", "JKL", "MNO", "PQR", "STU", "VWX"])}{random.randint(100, 999)}'
                if plate not in used_plates:
                    used_plates.add(plate)
                    break
            
            # Create insurance first
            insurance = Insurance.objects.create(
                insurance_number=1000 + i,
                company=random.choice(insurance_companies),
                coverage=random.randint(20, 80)
            )
            
            # Create vehicle with insurance
            vehicle = Vehicle.objects.create(
                customer=customer,
                license_plate=plate,
                model=random.choice(vehicle_models),
                year=random.randint(2015, 2024),
                insurance=insurance
            )
        
        self.stdout.write('Created vehicles and insurance successfully')

    def create_appointments(self):
        """Create sample appointments"""
        customers = Customer.objects.all()
        mechanics = Mechanic.objects.all()
        vehicles = Vehicle.objects.all()
        
        service_types = ['repair', 'test']
        statuses = ['scheduled', 'in_progress', 'completed']
        
        for i in range(100):  # Create 100 appointments for more data
            customer = random.choice(customers)
            mechanic = random.choice(mechanics)
            vehicle = random.choice(vehicles)
            service_type = random.choice(service_types)
            status = random.choice(statuses)
            
            # Create appointment time (within last 30 days to next 30 days)
            days_offset = random.randint(-30, 30)
            appointment_time = datetime.now() + timedelta(days=days_offset)
            
            # Create invoice first
            amount = Decimal(random.randint(100, 500))
            invoice = Invoices.objects.create(
                invoice_date=appointment_time.date(),
                amount_due=amount,
                payment_status='pending' if status != 'completed' else random.choice(['pending', 'paid']),
                payment_date=appointment_time if status == 'completed' else None
            )
            
            appointment = Appointment.objects.create(
                appointment_id=f'APT{i+1:03d}',
                customer=customer,
                vehicle=vehicle,
                mechanic=mechanic,
                appointment_time=appointment_time,
                service_type=service_type,
                invoice=invoice
            )
        
        self.stdout.write('Created appointments and invoices successfully')

    def create_tests_and_results(self):
        """Create sample tests and test results"""
        appointments = Appointment.objects.filter(service_type='test')
        
        test_types = ['Engine Performance', 'Brake System', 'Electrical System', 'Emission Test', 'Safety Inspection']
        diagnoses = ['Normal', 'Warning', 'Critical']
        
        for appointment in appointments:
            # Create test result first
            actual_value = Decimal(random.randint(60, 140))
            test_result = TestResult.objects.create(
                value=actual_value
            )
            
            # Create test
            test = Test.objects.create(
                test_name=random.choice(test_types),
                test_unit_price=Decimal(random.randint(50, 200)),
                normal_value=Decimal(random.randint(80, 120)),
                diagnosis=random.choice(diagnoses),
                test_result=test_result,
                component_name=f'Component {random.randint(1, 10)}'
            )
            
            # Link test to appointment
            appointment.test = test
            appointment.save()
        
        self.stdout.write('Created tests and results successfully')

    def create_repairs_and_spare_parts(self):
        """Create sample repairs and spare parts"""
        appointments = Appointment.objects.filter(service_type='repair')
        mechanic = Mechanic.objects.first()
        vehicles = Vehicle.objects.all()
        
        # Create suppliers
        suppliers = []
        supplier_names = ['AutoParts Plus', 'CarCare Supplies', 'Mechanic Depot', 'Quality Parts Co']
        for name in supplier_names:
            supplier = Supplier.objects.create(
                name=name,
                contact_info=f'Contact: {name}, Phone: 555-{random.randint(1000, 9999)}'
            )
            suppliers.append(supplier)
        
        # Create spare parts
        spare_parts_data = [
            {'name': 'Oil Filter', 'unit_cost': 15.00},
            {'name': 'Brake Pads', 'unit_cost': 45.00},
            {'name': 'Air Filter', 'unit_cost': 25.00},
            {'name': 'Spark Plugs', 'unit_cost': 8.00},
            {'name': 'Battery', 'unit_cost': 120.00},
            {'name': 'Tire', 'unit_cost': 85.00},
            {'name': 'Alternator', 'unit_cost': 180.00},
            {'name': 'Starter Motor', 'unit_cost': 95.00},
        ]
        
        spare_parts = []
        for part_data in spare_parts_data:
            part = SpareParts.objects.create(
                name=part_data['name'],
                unit_cost=Decimal(part_data['unit_cost']),
                quantity_in_stock=random.randint(10, 100)
            )
            spare_parts.append(part)
        
        # Create repairs
        for appointment in appointments:
            vehicle = random.choice(vehicles)
            insurance = vehicle.insurance
            
            repair = Repair.objects.create(
                repair_code=f'REP{appointment.appointment_id}',
                mechanic=mechanic,
                vehicle=vehicle,
                vehicle_insurance=insurance,
                repair_date=appointment.appointment_time.date(),
                repair_cost=Decimal(random.randint(200, 800)),
                repair_name=f'Repair for {vehicle.license_plate}'
            )
            
            # Link repair to appointment
            appointment.repair = repair
            appointment.save()
            
            # Add spare parts to repair
            num_parts = random.randint(1, 3)
            selected_parts = random.sample(spare_parts, min(num_parts, len(spare_parts)))
            
            for part in selected_parts:
                Repair_has_SpareParts.objects.create(
                    repair=repair,
                    spare_part=part
                )
        
        self.stdout.write('Created repairs and spare parts successfully') 