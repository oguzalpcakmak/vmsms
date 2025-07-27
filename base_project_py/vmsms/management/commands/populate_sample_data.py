from django.core.management.base import BaseCommand
from django.db import transaction
from vmsms.models import (
    Customer, Mechanic, Vehicle, Insurance, Repair, Test, TestResult,
    Specialization, Invoices
)
from decimal import Decimal
import datetime

class Command(BaseCommand):
    help = 'Populate the database with sample data for repairs and tests'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample data...')
        
        with transaction.atomic():
            # Create specializations
            spec1, created = Specialization.objects.get_or_create(
                specialization_code='ENG',
                defaults={'name': 'Engine Specialist'}
            )
            spec2, created = Specialization.objects.get_or_create(
                specialization_code='BRAKE',
                defaults={'name': 'Brake System Specialist'}
            )
            spec3, created = Specialization.objects.get_or_create(
                specialization_code='ELEC',
                defaults={'name': 'Electrical System Specialist'}
            )
            
            # Create a sample customer
            customer, created = Customer.objects.get_or_create(
                username='sample_customer',
                defaults={
                    'password': 'password123',
                    'name': 'John Doe',
                    'phone_number': '555-0123',
                    'email': 'john.doe@example.com',
                    'address': '123 Main St, City'
                }
            )
            
            # Create a sample insurance
            insurance, created = Insurance.objects.get_or_create(
                insurance_number=12345,
                defaults={
                    'coverage': Decimal('85.00'),
                    'company': 'SafeDrive Insurance'
                }
            )
            
            # Create a sample vehicle
            vehicle, created = Vehicle.objects.get_or_create(
                license_plate='ABC123',
                defaults={
                    'model': 'Toyota Camry',
                    'year': 2020,
                    'vin_number': '1HGBH41JXMN109186',
                    'insurance': insurance,
                    'customer': customer
                }
            )
            
            # Create sample mechanics
            mechanic1, created = Mechanic.objects.get_or_create(
                username='mechanic1',
                defaults={
                    'password': 'password123',
                    'name': 'Mike',
                    'surname': 'Johnson',
                    'phone_number': '555-0101',
                    'service_fee': Decimal('75.00'),
                    'specialization_code': spec1.specialization_code
                }
            )
            
            mechanic2, created = Mechanic.objects.get_or_create(
                username='mechanic2',
                defaults={
                    'password': 'password123',
                    'name': 'Sarah',
                    'surname': 'Wilson',
                    'phone_number': '555-0102',
                    'service_fee': Decimal('80.00'),
                    'specialization_code': spec2.specialization_code
                }
            )
            
            mechanic3, created = Mechanic.objects.get_or_create(
                username='mechanic3',
                defaults={
                    'password': 'password123',
                    'name': 'David',
                    'surname': 'Brown',
                    'phone_number': '555-0103',
                    'service_fee': Decimal('70.00'),
                    'specialization_code': spec3.specialization_code
                }
            )
            
            # Create sample invoice
            invoice, created = Invoices.objects.get_or_create(
                invoice_id=1001,
                defaults={
                    'invoice_date': datetime.date.today(),
                    'amount_due': Decimal('150.00'),
                    'payment_status': 'Pending',
                    'payment_date': None
                }
            )
            
            # Create sample test results
            test_result1, created = TestResult.objects.get_or_create(
                test_result_id=1,
                defaults={'value': Decimal('95.5')}
            )
            
            test_result2, created = TestResult.objects.get_or_create(
                test_result_id=2,
                defaults={'value': Decimal('88.2')}
            )
            
            test_result3, created = TestResult.objects.get_or_create(
                test_result_id=3,
                defaults={'value': Decimal('92.1')}
            )
            
            test_result4, created = TestResult.objects.get_or_create(
                test_result_id=4,
                defaults={'value': Decimal('87.8')}
            )
            
            test_result5, created = TestResult.objects.get_or_create(
                test_result_id=5,
                defaults={'value': Decimal('94.3')}
            )
            
            # Create sample repairs
            repair1, created = Repair.objects.get_or_create(
                repair_code='R001',
                mechanic=mechanic1,
                vehicle=vehicle,
                vehicle_insurance=insurance,
                defaults={
                    'repair_name': 'Oil Change and Filter Replacement',
                    'repair_date': datetime.date.today(),
                    'repair_cost': Decimal('45.00')
                }
            )
            
            repair2, created = Repair.objects.get_or_create(
                repair_code='R002',
                mechanic=mechanic2,
                vehicle=vehicle,
                vehicle_insurance=insurance,
                defaults={
                    'repair_name': 'Brake Pad Replacement',
                    'repair_date': datetime.date.today(),
                    'repair_cost': Decimal('120.00')
                }
            )
            
            repair3, created = Repair.objects.get_or_create(
                repair_code='R003',
                mechanic=mechanic3,
                vehicle=vehicle,
                vehicle_insurance=insurance,
                defaults={
                    'repair_name': 'Battery Replacement',
                    'repair_date': datetime.date.today(),
                    'repair_cost': Decimal('85.00')
                }
            )
            
            repair4, created = Repair.objects.get_or_create(
                repair_code='R004',
                mechanic=mechanic1,
                vehicle=vehicle,
                vehicle_insurance=insurance,
                defaults={
                    'repair_name': 'Engine Tune-up',
                    'repair_date': datetime.date.today(),
                    'repair_cost': Decimal('200.00')
                }
            )
            
            repair5, created = Repair.objects.get_or_create(
                repair_code='R005',
                mechanic=mechanic2,
                vehicle=vehicle,
                vehicle_insurance=insurance,
                defaults={
                    'repair_name': 'Tire Rotation and Balance',
                    'repair_date': datetime.date.today(),
                    'repair_cost': Decimal('60.00')
                }
            )
            
            # Create sample tests
            test1, created = Test.objects.get_or_create(
                test_id=1,
                defaults={
                    'test_name': 'Engine Performance Test',
                    'normal_value': Decimal('90.0'),
                    'diagnosis': 'Engine running efficiently',
                    'test_unit_price': Decimal('50.00'),
                    'test_result': test_result1,
                    'component_name': 'Engine'
                }
            )
            
            test2, created = Test.objects.get_or_create(
                test_id=2,
                defaults={
                    'test_name': 'Brake System Test',
                    'normal_value': Decimal('85.0'),
                    'diagnosis': 'Brake system functioning properly',
                    'test_unit_price': Decimal('40.00'),
                    'test_result': test_result2,
                    'component_name': 'Brake System'
                }
            )
            
            test3, created = Test.objects.get_or_create(
                test_id=3,
                defaults={
                    'test_name': 'Electrical System Test',
                    'normal_value': Decimal('92.0'),
                    'diagnosis': 'Electrical system in good condition',
                    'test_unit_price': Decimal('35.00'),
                    'test_result': test_result3,
                    'component_name': 'Electrical System'
                }
            )
            
            test4, created = Test.objects.get_or_create(
                test_id=4,
                defaults={
                    'test_name': 'Emission Test',
                    'normal_value': Decimal('88.0'),
                    'diagnosis': 'Emissions within acceptable limits',
                    'test_unit_price': Decimal('45.00'),
                    'test_result': test_result4,
                    'component_name': 'Exhaust System'
                }
            )
            
            test5, created = Test.objects.get_or_create(
                test_id=5,
                defaults={
                    'test_name': 'Transmission Test',
                    'normal_value': Decimal('95.0'),
                    'diagnosis': 'Transmission operating smoothly',
                    'test_unit_price': Decimal('55.00'),
                    'test_result': test_result5,
                    'component_name': 'Transmission'
                }
            )
            
        self.stdout.write(
            self.style.SUCCESS('Successfully created sample data!')
        )
        self.stdout.write('Created:')
        self.stdout.write('- 3 Specializations')
        self.stdout.write('- 1 Customer')
        self.stdout.write('- 1 Insurance')
        self.stdout.write('- 1 Vehicle')
        self.stdout.write('- 3 Mechanics')
        self.stdout.write('- 1 Invoice')
        self.stdout.write('- 5 Test Results')
        self.stdout.write('- 5 Repairs')
        self.stdout.write('- 5 Tests') 