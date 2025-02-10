import os
import django
import random
from datetime import timedelta, date

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "rental_managment.settings")  # Replace with your project name
django.setup()

from rentals.models import Building, Apartment, Tenant, ActiveTenant, RentalHistory  # Replace 'myapp' with your actual app name

# Generate random dates
def random_date(start_year=2020, end_year=2024):
    start = date(start_year, 1, 1)
    end = date(end_year, 12, 31)
    delta = end - start
    return start + timedelta(days=random.randint(0, delta.days))

# Create Buildings
def create_buildings(n=3):
    buildings = []
    for i in range(1, n + 1):
        building = Building.objects.create(
            building_number=f"B-{i}",
            address=f"Street {i}, City XYZ",
            number_of_floors=random.randint(1, 5),
            number_of_apartments=random.randint(2, 10)
        )
        buildings.append(building)
    return buildings

# Create Apartments
def create_apartments(buildings, n=5):
    apartments = []
    for building in buildings:
        for i in range(1, n + 1):
            apartment = Apartment.objects.create(
                building=building,
                apartment_number=f"A-{i}",
                num_of_rooms=random.randint(1, 4),
                electricity_meter_number=f"EM-{random.randint(1000, 9999)}",
                water_meter_number=f"WM-{random.randint(1000, 9999)}",
                status=random.choice(["شاغرة", "مأهولة"]),
                floor_number=random.randint(1, building.number_of_floors)
            )
            apartments.append(apartment)
    return apartments

# Create Tenants
def create_tenants(n=5):
    tenants = []
    for i in range(1, n + 1):
        tenant = Tenant.objects.create(
            name=f"Tenant {i}",
            phone_number=f"0555{random.randint(100000, 999999)}",
            id_number=f"ID-{random.randint(1000, 9999)}",
            workplace=f"Company {random.randint(1, 10)}",
            additional_notes=f"Note {i}"
        )
        tenants.append(tenant)
    return tenants

# Create Active Tenants
def create_active_tenants(apartments, tenants):
    for apartment, tenant in zip(apartments, tenants):
        start_date = random_date()
        end_date = start_date + timedelta(days=random.randint(365, 730))
        ActiveTenant.objects.create(
            apartment=apartment,
            tenant=tenant,
            contract_number=f"C-{random.randint(1000, 9999)}",
            contract_start_date=start_date,
            contract_end_date=end_date,
            rent_amount=random.randint(2000, 6000),
            payment_status=random.choice(["Paid", "Unpaid", "Partial"]),
            deposit=random.randint(1000, 5000),
            notes="No additional notes"
        )

# Create Rental History
def create_rental_history(tenants, apartments):
    for tenant, apartment in zip(tenants, apartments):
        start_date = random_date(2015, 2019)
        end_date = start_date + timedelta(days=random.randint(365, 730))
        RentalHistory.objects.create(
            tenant=tenant,
            apartment=apartment,
            contract_number=f"H-{random.randint(1000, 9999)}",
            contract_start_date=start_date,
            contract_end_date=end_date,
            rent_amount=random.randint(2000, 6000),
            payment_status=random.choice(["Paid", "Unpaid", "Partial"]),
            deposit=random.randint(1000, 5000),
            additional_notes="No additional notes"
        )

# Run data population
def populate_database():
    print("Creating buildings...")
    buildings = create_buildings(3)
    
    print("Creating apartments...")
    apartments = create_apartments(buildings, 5)
    
    print("Creating tenants...")
    tenants = create_tenants(5)
    
    print("Creating active tenants...")
    create_active_tenants(apartments, tenants)
    
    print("Creating rental history...")
    create_rental_history(tenants, apartments)
    
    print("Database populated successfully!")

if __name__ == "__main__":
    populate_database()
