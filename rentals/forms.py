from django import forms
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User, Group, Permission
from django_select2.forms import Select2Widget
from .models import Building, Apartment, Tenant, ActiveTenant


class UserForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput,
        required=True,
        label="كلمة المرور:"
    )

    class Meta:
        model = User
        fields = [
            'username', 'password', 'first_name', 'last_name', 'email',
            'is_superuser', 'is_active'
        ]
        labels = {
            'is_superuser': 'صلاحيات المدير:',
        }
        help_texts = {
            'username': '',
        }
        required = {
            'username': True,
            'password': True,
            'first_name': True,
            'last_name': True,
        }
        widgets = {
            'is_superuser': forms.CheckboxInput(attrs={'class': 'custom-checkbox'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'custom-checkbox'}),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        if self.cleaned_data['password']:
            user.password = make_password(self.cleaned_data['password'])

        if commit:
            user.save()
            self.save_m2m()  # حفظ العلاقات ManyToMany (المجموعات والأذونات)

            # ✅ إنشاء أو جلب المجموعة الافتراضية
            default_group, created = Group.objects.get_or_create(name="Users")

            # ✅ إضافة الأذونات الافتراضية
            default_permissions = [
                "view_activetenant",
                "view_apartment",
                "view_building",
                "view_rentalhistory",
                "view_tenant",
            ]

            for perm_codename in default_permissions:
                try:
                    permission = Permission.objects.get(codename=perm_codename, content_type__app_label="rentals")
                    default_group.permissions.add(permission)  # ✅ إضافة الأذونات إلى المجموعة
                except Permission.DoesNotExist:
                    pass  # تجنب الأخطاء في حالة عدم وجود الإذن

            # ✅ إضافة المستخدم إلى المجموعة
            user.groups.add(default_group)

        return user

class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']  # Add other fields as needed
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'first_name': 'الاسم الأول',
            'last_name': 'الاسم الأخير',
            'email': 'البريد الإلكتروني',
        }


class BuildingForm(forms.ModelForm):
    class Meta:
        model = Building
        fields = "__all__"
        can_delete=True
        widgets = {
            'number_of_apartments': forms.NumberInput(attrs={'readonly': 'readonly'}),  
        }

class ApartmentForm(forms.ModelForm):
    class Meta:
        model = Apartment
        fields = "__all__"
        can_delete=True
        widgets = {
            'number_of_apartments': forms.NumberInput(attrs={'readonly': 'readonly'}),  
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

class TenantForm(forms.ModelForm):
    class Meta:
        model = Tenant
        fields = "__all__"
        can_delete=True
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

class ActiveTenantForm(forms.ModelForm):
    tenant = forms.ModelChoiceField(queryset=Tenant.objects.all(), label="المستأجر")

    class Meta:
        model = ActiveTenant
        fields = [
            'tenant', 'contract_number', 'contract_start_date', 
            'contract_end_date', 'rent_amount', 'notes'
        ]
        widgets = {
            'contract_start_date': forms.DateInput(attrs={'type': 'date'}),
            'contract_end_date': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }


class BuildingFilterForm(forms.Form):
    building_number = forms.ChoiceField(
        required=False,
        widget=Select2Widget(attrs={"class": "select2", 'data-placeholder': 'اختر العمارة'}),
        label="العمارة"
    )
    search = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'type': 'text', 'placeholder': 'البحث'}),
        label="البحث"
    )
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        buildings = Building.objects.values_list('building_number', flat=True).distinct()
        self.fields['building_number'].choices = [(b, b) for b in buildings]

class ApartmentFilterForm(forms.Form):
    building = forms.ChoiceField(
        required=False,
        widget=Select2Widget(attrs={"class": "select2", 'data-placeholder': 'اختر العمارة'}),
        label="العمارة"
    )
    apartment = forms.ChoiceField(
        required=False,
        widget=Select2Widget(attrs={"class": "select2", 'data-placeholder': 'اختر الشقة'}),
        label="الشقة"
    )
    status = forms.ChoiceField(
        choices=[("", "الكل")] + Apartment.APARTMENT_STATUS_CHOICES,
        required=False,
        label=" الشقة",
        widget=forms.RadioSelect(attrs={"class": "custom-radio", 'placeholder': 'الحالة'})
    )
    search = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'type': 'text', 'placeholder': 'البحث'}),
        label="البحث"
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        buildings = Building.objects.values_list('building_number', flat=True).distinct()
        self.fields['building'].choices = [(b, b) for b in buildings]
        apartments = Apartment.objects.values_list('apartment_number', flat=True).distinct()
        self.fields['apartment'].choices = [(b, b) for b in apartments]

class TenantFilterForm(forms.Form):
    search = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'type': 'text', 'placeholder': 'البحث'}),
        label="البحث"
    )

class ActiveTenantFilterForm(forms.Form):
    apartment = forms.ChoiceField(
        required=False,
        widget=Select2Widget(attrs={"class": "select2", 'data-placeholder': 'اختر الشقة'}),
        label="الشقة"
    )
    tenant = forms.ChoiceField(
        required=False,
        widget=Select2Widget(attrs={"class": "select2", 'data-placeholder': 'اختر المستاجر'}),
        label="المستاجر"
    )
    search = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'type': 'text', 'placeholder': 'البحث'}),
        label="البحث"
    )
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        apartments = Apartment.objects.all().distinct()
        self.fields['apartment'].choices = [(b, b) for b in apartments]
        tenants = Tenant.objects.all().distinct()
        self.fields['tenant'].choices = [(b, b) for b in tenants]
