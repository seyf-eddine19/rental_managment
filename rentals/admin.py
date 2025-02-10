from django.contrib import admin
from .models import Building, Apartment, Tenant, ActiveTenant, RentalHistory

class ApartmentInline(admin.StackedInline):
    model = Apartment
    extra = 0

class ActiveTenantInline(admin.StackedInline):
    model = ActiveTenant
    extra = 0

class RentalHistoryInline(admin.TabularInline):
    model = RentalHistory
    extra = 0
    readonly_fields = [field.name for field in RentalHistory._meta.fields]  # Make all fields read-only
    can_delete = False  # Disable deletion
    show_change_link = False  # Optionally, you can add this to hide the "change" link for the inline
    show_add_button = False  # Hide the "Add another" link

class BuildingAdmin(admin.ModelAdmin):
    list_display = ("building_number", "address", "number_of_floors", "number_of_apartments")
    search_fields = ("building_number", "address")
    list_filter = ("number_of_floors",)
    inlines = [ApartmentInline]

class ApartmentAdmin(admin.ModelAdmin):
    list_display = ("apartment_number", "building", "num_of_rooms", "status", "floor_number")
    search_fields = ("apartment_number", "building__building_number", "electricity_meter_number", "water_meter_number")
    list_filter = ("status", "floor_number", "building")
    inlines = [ActiveTenantInline, RentalHistoryInline]

class TenantAdmin(admin.ModelAdmin):
    list_display = ("name", "phone_number", "id_number", "workplace")
    search_fields = ("name", "phone_number", "id_number", "workplace")
    list_filter = ("workplace",)
    inlines = [ActiveTenantInline, RentalHistoryInline]

class ActiveTenantAdmin(admin.ModelAdmin):
    list_display = ("tenant", "apartment", "contract_number", "contract_start_date", "contract_end_date", "rent_amount", "payment_status")
    search_fields = ("tenant__name", "apartment__apartment_number", "contract_number")
    list_filter = ("contract_start_date", "contract_end_date", "payment_status")

class RentalHistoryAdmin(admin.ModelAdmin):
    list_display = ("tenant", "apartment", "contract_number", "contract_start_date", "contract_end_date", "rent_amount", "payment_status")
    search_fields = ("tenant__name", "apartment__apartment_number", "contract_number")
    list_filter = ("contract_start_date", "contract_end_date", "payment_status")

admin.site.register(Building, BuildingAdmin)
admin.site.register(Apartment, ApartmentAdmin)
admin.site.register(Tenant, TenantAdmin)
admin.site.register(ActiveTenant)
admin.site.register(RentalHistory)

