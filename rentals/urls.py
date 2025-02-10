from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('', views.index, name='index'),

    # Building URLs
    path('buildings/', views.BuildingListView.as_view(), name='building_list'),
    path('buildings/create/', views.BuildingFormView.as_view(), name='building_create'),
    path('buildings/<int:pk>/', views.BuildingDetailView.as_view(), name='building_detail'),
    path('buildings/<int:pk>/update/', views.BuildingFormView.as_view(), name='building_update'),
    path('buildings/<int:pk>/delete/', views.BuildingDeleteView.as_view(), name='building_delete'),
    
    # Apartment URLs
    path('apartments/', views.ApartmentListView.as_view(), name='apartment_list'),
    path('apartments/create/', views.ApartmentFormView.as_view(), name='apartment_create'),
    path('apartments/<int:pk>/', views.ApartmentDetailView.as_view(), name='apartment_detail'),
    path('apartment/<int:pk>/set_vacant/', views.ApartmentDetailView.as_view(), name='apartment_set_vacant'),
    path('apartments/<int:pk>/update/', views.ApartmentFormView.as_view(), name='apartment_update'),
    path('apartments/<int:pk>/delete/', views.ApartmentDeleteView.as_view(), name='apartment_delete'),

    # Tenant URLs
    path('tenants/', views.TenantListView.as_view(), name='tenant_list'),
    path('tenants/create/', views.TenantFormView.as_view(), name='tenant_create'),
    path('tenants/<int:pk>/', views.TenantDetailView.as_view(), name='tenant_detail'),
    path('tenants/<int:pk>/update/', views.TenantFormView.as_view(), name='tenant_update'),
    path('tenants/<int:pk>/delete/', views.TenantDeleteView.as_view(), name='tenant_delete'),

    # Active Tenant URLs
    path('active_tenant/', views.ActiveTenantListView.as_view(), name='active_tenant_list'),
    path('apartment/<int:apartment_id>/manage-tenant/create/', views.ActiveTenantFormView.as_view(), name='active_tenant_create'),
    path('apartment/<int:apartment_id>/manage-tenant/<int:pk>/update/', views.ActiveTenantFormView.as_view(), name='active_tenant_update'),
    
    # User URLs
    path('users/', views.UserListView.as_view(), name='user_list'),
    path('users/create/', views.UserFormView.as_view(), name='user_create'),
    path('users/<int:pk>/update/', views.UserFormView.as_view(), name='user_update'),
    path('users/<int:pk>/delete/', views.UserDeleteView.as_view(), name='user_delete'),
]