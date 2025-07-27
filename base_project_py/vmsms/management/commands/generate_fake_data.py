from django.core.management.base import BaseCommand
from django.db import transaction
from vmsms.models import *
import random
import datetime
from decimal import Decimal

class Command(BaseCommand):
    help = 'Generate comprehensive fake data for VMSMS demo and analytics'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing data before generating new data',
        )
        parser.add_argument(
            '--customers',
            type=int,
            default=20,
            help='Number of customers to generate',
        )
        parser.add_argument(
            '--mechanics',
            type=int,
            default=8,
            help='Number of mechanics to generate',
        )
        parser.add_argument(
            '--receptionists',
            type=int,
            default=3,
            help='Number of receptionists to generate',
        )
        parser.add_argument(
            '--vehicles',
            type=int,
            default=50,
            help='Number of vehicles to generate',
        )
        parser.add_argument(
            '--appointments',
            type=int,
            default=100,
            help='Number of appointments to generate',
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write('Clearing existing data...')
            self.clear_data()
        
        self.stdout.write('Generating fake data...')
        
        # Generate data in order of dependencies
        customers = self.generate_customers(options['customers'])
        mechanics = self.generate_mechanics(options['mechanics'])
        receptionists = self.generate_receptionists(options['receptionists'])
        vehicles = self.generate_vehicles(options['vehicles'], customers)
        insurances = self.generate_insurances()
        spare_parts = self.generate_spare_parts()
        suppliers = self.generate_suppliers()
        tests = self.generate_tests()
        appointments = self.generate_appointments(options['appointments'], vehicles, mechanics, customers, tests)
        repairs = self.generate_repairs(appointments, spare_parts)
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully generated:\n'
                f'- {len(customers)} customers\n'
                f'- {len(mechanics)} mechanics\n'
                f'- {len(receptionists)} receptionists\n'
                f'- {len(vehicles)} vehicles\n'
                f'- {len(insurances)} insurance policies\n'
                f'- {len(spare_parts)} spare parts\n'
                f'- {len(suppliers)} suppliers\n'
                f'- {len(tests)} tests\n'
                f'- {len(appointments)} appointments\n'
                f'- {len(repairs)} repairs'
            )
        )

    def clear_data(self):
        """Clear all existing data"""
        models_to_clear = [
            Repair_has_SpareParts, SparePart_has_Supplier, Vehicle_has_Mechanic,
            Component_has_Test, Appointment, Repair, Test, TestResult,
            Vehicle, Insurance, Customer, Mechanic, Receptionist, InventoryManager,
            Invoices, SpareParts, Supplier, VehicleComponent
        ]
        
        for model in models_to_clear:
            model.objects.all().delete()

    def generate_customers(self, count):
        """Generate fake customers"""
        customers = []
        first_names = ['John', 'Jane', 'Mike', 'Sarah', 'David', 'Lisa', 'Tom', 'Emma', 'Chris', 'Anna']
        last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis', 'Rodriguez', 'Martinez']
        
        for i in range(count):
            customer = Customer.objects.create(
                username=f'customer{i+1}',
                password='password123',
                name=random.choice(first_names),
                surname=random.choice(last_names),
                email=f'customer{i+1}@example.com',
                phone_number=f'+1-555-{random.randint(100, 999)}-{random.randint(1000, 9999)}',
                address=f'{random.randint(100, 9999)} {random.choice(["Main St", "Oak Ave", "Pine Rd", "Elm St"])}, City {i+1}'
            )
            customers.append(customer)
        
        return customers

    def generate_mechanics(self, count):
        """Generate fake mechanics"""
        mechanics = []
        first_names = ['Alex', 'Bob', 'Charlie', 'Diana', 'Eve', 'Frank', 'Grace', 'Henry']
        last_names = ['Anderson', 'Baker', 'Clark', 'Davis', 'Evans', 'Fisher', 'Green', 'Harris']
        specializations = ['ENG', 'BRAK', 'ELEC', 'TRAN', 'COOL', 'FUEL', 'SUSP', 'EXHA']
        
        for i in range(count):
            mechanic = Mechanic.objects.create(
                username=f'mechanic{i+1}',
                password='password123',
                name=random.choice(first_names),
                surname=random.choice(last_names),
                email=f'mechanic{i+1}@vmsms.com',
                phone_number=f'+1-555-{random.randint(100, 999)}-{random.randint(1000, 9999)}',
                address=f'{random.randint(100, 9999)} {random.choice(["Garage St", "Workshop Ave", "Service Rd"])}, City {i+1}',
                service_fee=Decimal(random.randint(50, 150)),
                specialization_code=random.choice(specializations)
            )
            mechanics.append(mechanic)
        
        return mechanics

    def generate_receptionists(self, count):
        """Generate fake receptionists"""
        receptionists = []
        first_names = ['Alice', 'Betty', 'Carol', 'Doris', 'Eva', 'Fiona', 'Gina', 'Helen']
        last_names = ['Wilson', 'Taylor', 'Moore', 'Jackson', 'Martin', 'Lee', 'Perez', 'Thompson']
        
        for i in range(count):
            receptionist = Receptionist.objects.create(
                username=f'receptionist{i+1}',
                password='password123',
                name=random.choice(first_names),
                surname=random.choice(last_names),
                email=f'receptionist{i+1}@vmsms.com',
                phone_number=f'+1-555-{random.randint(100, 999)}-{random.randint(1000, 9999)}',
                address=f'{random.randint(100, 9999)} {random.choice(["Office St", "Reception Ave", "Front Rd"])}, City {i+1}'
            )
            receptionists.append(receptionist)
        
        return receptionists

    def generate_vehicles(self, count, customers):
        """Generate fake vehicles with unique license plates"""
        vehicles = []
        models = ['Toyota Camry', 'Honda Civic', 'Ford Focus', 'Nissan Altima', 'Chevrolet Malibu', 
                 'Hyundai Sonata', 'Kia Optima', 'Mazda 6', 'Subaru Legacy', 'Volkswagen Passat']
        years = list(range(2015, 2024))
        used_plates = set()
        
        for i in range(count):
            customer = random.choice(customers)
            # Generate a unique license plate
            while True:
                plate = f'{random.choice(["ABC", "DEF", "GHI", "JKL"])}{random.randint(100, 999)}'
                if plate not in used_plates:
                    used_plates.add(plate)
                    break
            vehicle = Vehicle.objects.create(
                license_plate=plate,
                model=random.choice(models),
                year=random.choice(years),
                vin_number=f'1HGBH41JXMN{random.randint(100000, 999999)}',
                customer=customer
            )
            vehicles.append(vehicle)
        
        return vehicles

    def generate_insurances(self):
        """Generate fake insurance policies"""
        insurances = []
        companies = ['State Farm', 'Allstate', 'Geico', 'Progressive', 'Liberty Mutual', 'Farmers', 'Nationwide']
        
        for i in range(30):
            insurance = Insurance.objects.create(
                insurance_number=random.randint(100000, 999999),
                coverage=Decimal(random.randint(20, 80)),
                company=random.choice(companies)
            )
            insurances.append(insurance)
        
        # Assign insurance to some vehicles
        vehicles = Vehicle.objects.all()
        for vehicle in vehicles[:25]:  # 50% of vehicles have insurance
            vehicle.insurance = random.choice(insurances)
            vehicle.save()
        
        return insurances

    def generate_spare_parts(self):
        """Generate fake spare parts"""
        spare_parts = []
        parts_data = [
            ('Brake Pads', 45.99), ('Oil Filter', 12.99), ('Air Filter', 18.99),
            ('Spark Plugs', 8.99), ('Battery', 89.99), ('Tire', 125.99),
            ('Windshield Wipers', 15.99), ('Headlight Bulb', 22.99),
            ('Brake Rotor', 65.99), ('Timing Belt', 35.99), ('Water Pump', 55.99),
            ('Alternator', 120.99), ('Starter Motor', 95.99), ('Fuel Pump', 85.99),
            ('Radiator', 150.99), ('Muffler', 75.99), ('Catalytic Converter', 180.99)
        ]
        
        for name, cost in parts_data:
            spare_part = SpareParts.objects.create(
                name=name,
                quantity_in_stock=random.randint(5, 50),
                unit_cost=Decimal(str(cost))
            )
            spare_parts.append(spare_part)
        
        return spare_parts

    def generate_suppliers(self):
        """Generate fake suppliers"""
        suppliers = []
        supplier_names = ['AutoZone', 'NAPA Auto Parts', 'O\'Reilly Auto Parts', 'Advance Auto Parts',
                         'CarQuest', 'Pep Boys', 'AutoNation', 'CarMax', 'Enterprise', 'Hertz']
        
        for name in supplier_names:
            supplier = Supplier.objects.create(
                name=name,
                contact_info=f'Phone: +1-555-{random.randint(100, 999)}-{random.randint(1000, 9999)}\nEmail: contact@{name.lower().replace(" ", "").replace("\'", "")}.com'
            )
            suppliers.append(supplier)
        
        return suppliers

    def generate_tests(self):
        """Generate fake tests with results"""
        tests = []
        test_names = [
            'Engine Performance Test', 'Brake System Test', 'Electrical System Test',
            'Emission Test', 'Transmission Test', 'Battery Test', 'Wheel Alignment Test',
            'Engine Compression Test', 'Cooling System Test', 'Fuel System Test'
        ]
        components = ['Engine', 'Brakes', 'Electrical', 'Exhaust', 'Transmission', 'Battery', 'Suspension', 'Engine', 'Cooling', 'Fuel']
        
        for i in range(80):
            # Create test result first
            test_result = TestResult.objects.create(
                value=Decimal(random.randint(50, 200))
            )
            
            test = Test.objects.create(
                test_name=random.choice(test_names),
                normal_value=Decimal(random.randint(80, 150)),
                diagnosis=random.choice([
                    'Normal operation', 'Minor wear detected', 'Replacement recommended',
                    'Maintenance required', 'Performance degraded', 'Component failure',
                    'Regular wear', 'Optimal condition', 'Service needed', 'Good condition'
                ]),
                test_unit_price=Decimal(random.randint(25, 100)),
                test_result=test_result,
                component_name=random.choice(components)
            )
            tests.append(test)
        
        return tests

    def generate_appointments(self, count, vehicles, mechanics, customers, tests):
        """Generate fake appointments"""
        appointments = []
        start_date = datetime.date.today() - datetime.timedelta(days=60)
        
        for i in range(count):
            # Random date within last 60 days
            random_days = random.randint(0, 60)
            appointment_date = start_date + datetime.timedelta(days=random_days)
            
            # Random time between 8 AM and 6 PM
            hour = random.randint(8, 18)
            minute = random.choice([0, 30])
            appointment_time = datetime.datetime.combine(
                appointment_date,
                datetime.time(hour, minute)
            )
            
            vehicle = random.choice(vehicles)
            mechanic = random.choice(mechanics)
            customer = vehicle.customer
            service_type = random.choice(['test', 'repair'])
            
            # Create invoice
            invoice = Invoices.objects.create(
                invoice_date=appointment_date,
                amount_due=Decimal(random.randint(50, 500)),
                payment_status=random.choice(['Paid', 'Pending', 'Overdue']),
                payment_date=appointment_date + datetime.timedelta(days=random.randint(0, 30)) if random.choice([True, False]) else None
            )
            
            appointment = Appointment.objects.create(
                appointment_id=f'APT{random.randint(10000, 99999)}',
                appointment_time=appointment_time,
                vehicle=vehicle,
                mechanic=mechanic,
                invoice=invoice,
                customer=customer,
                service_type=service_type,
                test_completed=random.choice([True, False]),
                repair_approved=random.choice([True, False])
            )
            
            # Assign test to some appointments
            if service_type == 'test' and random.choice([True, False]):
                test = random.choice(tests)
                appointment.test = test
                appointment.save()
            
            appointments.append(appointment)
        
        return appointments

    def generate_repairs(self, appointments, spare_parts):
        """Generate fake repairs"""
        repairs = []
        repair_names = [
            'Oil Change and Filter Replacement', 'Brake Pad Replacement', 'Battery Replacement',
            'Engine Tune-up', 'Tire Rotation and Balance', 'Air Filter Replacement',
            'Spark Plug Replacement', 'Transmission Service', 'Cooling System Service',
            'Brake Fluid Replacement', 'Timing Belt Replacement', 'Water Pump Replacement'
        ]
        
        for appointment in appointments:
            # Only create a repair if the vehicle has insurance
            if appointment.service_type == 'repair' and appointment.vehicle.insurance and random.choice([True, False]):
                repair = Repair.objects.create(
                    repair_code=f'REP{random.randint(10000, 99999)}',
                    mechanic=appointment.mechanic,
                    vehicle=appointment.vehicle,
                    vehicle_insurance=appointment.vehicle.insurance,
                    repair_name=random.choice(repair_names),
                    repair_date=appointment.appointment_time.date(),
                    repair_cost=Decimal(random.randint(100, 800))
                )
                
                # Link repair to appointment
                appointment.repair = repair
                appointment.save()
                
                # Add spare parts to some repairs
                if random.choice([True, False]):
                    num_parts = random.randint(1, 3)
                    selected_parts = random.sample(list(spare_parts), min(num_parts, len(spare_parts)))
                    
                    for part in selected_parts:
                        Repair_has_SpareParts.objects.create(
                            repair=repair,
                            spare_part=part
                        )
                
                repairs.append(repair)
        
        return repairs 