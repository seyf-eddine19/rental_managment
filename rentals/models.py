from django.db import models 


class Building(models.Model):
    building_number = models.CharField(max_length=3, unique=True, verbose_name="رقم العمارة")
    address = models.CharField(max_length=255, blank=True, verbose_name="عنوان العمارة")
    number_of_floors = models.IntegerField(verbose_name="عدد الطوابق", default=1)
    number_of_apartments = models.IntegerField(verbose_name="عدد الشقق", default=0)

    class Meta:
        verbose_name = "العمارة"
        verbose_name_plural = "العمارات"

    def __str__(self):
        return self.building_number


class Apartment(models.Model):
    APARTMENT_STATUS_CHOICES = [
        ('شاغرة', 'شاغرة'),
        ('مأهولة', 'مأهولة'),
    ]

    building = models.ForeignKey(Building, on_delete=models.CASCADE, related_name='apartments', verbose_name="العمارة")
    apartment_number = models.CharField(max_length=50, verbose_name="رقم الشقة")
    num_of_rooms = models.IntegerField(verbose_name="عدد الغرف")
    electricity_meter_number = models.CharField(max_length=50, verbose_name="رقم عداد الكهرباء")
    water_meter_number = models.CharField(max_length=50, verbose_name="رقم عداد الماء")
    status = models.CharField(max_length=8, choices=APARTMENT_STATUS_CHOICES, default='شاغرة', verbose_name="الحالة")
    floor_number = models.IntegerField(verbose_name="رقم الطابق", default=1)

    class Meta:
        verbose_name = "الشقة"
        verbose_name_plural = "الشقق"
    
    def save(self, *args, **kwargs):
        if not self.pk: 
            self.building.number_of_apartments += 1
            self.building.save()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.building.number_of_apartments += 1
        self.building.save()
        super().delete(*args, **kwargs)
        
    def __str__(self):
        return f"{self.building.building_number}|{self.apartment_number}"


class Tenant(models.Model):
    name = models.CharField(max_length=100, verbose_name="اسم المستاجر")
    phone_number = models.CharField(max_length=15, unique=True, verbose_name="رقم الهاتف")
    id_number = models.CharField(max_length=20, unique=True, verbose_name="رقم الهوية")
    workplace = models.CharField(max_length=100, blank=True, verbose_name="جهة العمل")
    notes = models.TextField(verbose_name="ملاحظات", blank=True)

    class Meta:
        verbose_name = "المستاجر"
        verbose_name_plural = "المستاجرين"

    def __str__(self):
        return self.name


class ActiveTenant(models.Model):
    apartment = models.OneToOneField(Apartment, on_delete=models.CASCADE, related_name="active_tenant", verbose_name="الشقة")
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name="active_apartment", verbose_name="المستاجر")
    contract_number = models.CharField(max_length=50, unique=True, verbose_name="رقم العقد")
    contract_start_date = models.DateField(verbose_name="تاريخ بداية العقد")
    contract_end_date = models.DateField(verbose_name="تاريخ انتهاء العقد")
    rent_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="مبلغ الإيجار شهري")
    notes = models.TextField(verbose_name="ملاحظات", blank=True)

    class Meta:
        verbose_name = "الايجار"
        verbose_name_plural = "الايجارات"

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)

        if is_new:
            RentalHistory.objects.create(
                active_tenant=self,
                apartment=self.apartment,
                tenant=self.tenant,
                contract_number=self.contract_number,
                contract_start_date=self.contract_start_date,
                contract_end_date=self.contract_end_date,
                rent_amount=self.rent_amount,
                notes=self.notes
            )
        else:
            rental_history = RentalHistory.objects.filter(active_tenant=self).first()
            if rental_history:
                rental_history.apartment = self.apartment
                rental_history.tenant = self.tenant
                rental_history.contract_number = self.contract_number
                rental_history.contract_start_date = self.contract_start_date
                rental_history.contract_end_date = self.contract_end_date
                rental_history.rent_amount = self.rent_amount
                rental_history.notes = self.notes
                rental_history.save()

        self.apartment.status = 'مأهولة'  # Set apartment status to "Occupied"
        self.apartment.save()
        
    def delete(self, *args, **kwargs):
        self.apartment.status = 'شاغرة'  # Set apartment status to "Vacant"
        self.apartment.save()
        super().delete(*args, **kwargs)

    def __str__(self):
        return f"{self.tenant.name} - {self.apartment.apartment_number}"


class RentalHistory(models.Model):
    active_tenant = models.ForeignKey(ActiveTenant, on_delete=models.SET_NULL, related_name="history", null=True, blank=True, verbose_name="العقد الحالي")
    apartment = models.ForeignKey(Apartment, on_delete=models.SET_NULL, related_name="rental_history", null=True, blank=True, verbose_name="الشقة")
    tenant = models.ForeignKey(Tenant, on_delete=models.SET_NULL, related_name="apartment_rental_history", null=True, blank=True, verbose_name="المستاجر")
    contract_number = models.CharField(max_length=50, unique=True, verbose_name="رقم العقد")
    contract_start_date = models.DateField(verbose_name="تاريخ بداية العقد")
    contract_end_date = models.DateField(verbose_name="تاريخ انتهاء العقد")
    rent_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="مبلغ الإيجار شهري")
    notes = models.TextField(verbose_name="ملاحظات", blank=True)

    class Meta:
        verbose_name = "سجل الايجار"
        verbose_name_plural = "سجل الايجارات"

    def __str__(self):
        return f"{self.tenant.name} - {self.apartment.apartment_number} ({self.contract_start_date} to {self.contract_end_date})"
