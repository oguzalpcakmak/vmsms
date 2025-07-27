from django.urls import path
from . import views

app_name = 'vmsms'

# Public routes (accessible to everyone)
public_urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/customer/', views.register_customer, name='register_customer'),
    path('register/admin/', views.register_admin, name='register_admin'),  # First-time setup only
]

# Dashboard routes (require authentication)
dashboard_urlpatterns = [
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('receptionist/dashboard/', views.receptionist_dashboard, name='receptionist_dashboard'),
    path('mechanic/dashboard/', views.mechanic_dashboard, name='mechanic_dashboard'),
    path('inventory_manager/dashboard/', views.inventory_manager_dashboard, name='inventory_manager_dashboard'),
    path('customer/dashboard/', views.customer_dashboard, name='customer_dashboard'),
]

# Admin-only routes (require admin authentication)
admin_urlpatterns = [
    path('admin/register/admin/', views.register_admin_from_admin, name='register_admin_from_admin'),
    path('admin/register/receptionist/', views.register_receptionist, name='register_receptionist'),
    path('admin/register/mechanic/', views.register_mechanic, name='register_mechanic'),
    path('admin/register/inventory_manager/', views.register_inventory_manager, name='register_inventory_manager'),
    path('admin/users/', views.user_list, name='user_list'),
    path('admin/users/<str:user_type>/<int:user_id>/', views.user_detail, name='user_detail'),
    path('admin/users/<str:user_type>/<int:user_id>/edit/', views.user_edit, name='user_edit'),
    path('admin/users/<str:user_type>/<int:user_id>/delete/', views.user_delete, name='user_delete'),
]

# Application routes (require authentication)
app_urlpatterns = [
    path('appointments/', views.appointment_list, name='appointment_list'),
    path('appointments/create/', views.appointment_create, name='appointment_create'),
    path('appointments/<int:pk>/update/', views.appointment_update, name='appointment_update'),
    path('appointments/<int:pk>/delete/', views.appointment_delete, name='appointment_delete'),
    path('appointments/<int:pk>/', views.appointment_detail, name='appointment_detail'),
    path('appointments/<int:appointment_id>/approve-repair/', views.approve_repair, name='approve_repair'),
    path('tests/', views.test_list, name='test_list'),
    path('tests/create/', views.test_create, name='test_create'),
    path('tests/<int:pk>/update/', views.test_update, name='test_update'),
    path('tests/<int:pk>/delete/', views.test_delete, name='test_delete'),
    path('tests/<int:test_id>/update-result/', views.update_test_result, name='update_test_result'),
    path('tests/<int:test_id>/diagnose/', views.diagnose_test, name='diagnose_test'),
    path('tests/<int:test_id>/suggest-repair/', views.suggest_repair, name='suggest_repair'),
    path('testresults/<int:pk>/update/', views.testresult_update, name='testresult_update'),
    path('analytics/costs/', views.analytics_costs, name='analytics_costs'),
    path('analytics/stats/', views.analytics_stats, name='analytics_stats'),
    path('invoices/', views.invoice_list, name='invoice_list'),
    path('invoices/create/', views.invoice_create, name='invoice_create'),
    path('invoices/<int:invoice_id>/', views.invoice_detail, name='invoice_detail'),
    path('invoices/<int:invoice_id>/update/', views.invoice_update, name='invoice_update'),
    path('invoices/<int:invoice_id>/delete/', views.invoice_delete, name='invoice_delete'),
    path('invoices/<int:invoice_id>/pay/', views.invoice_pay, name='invoice_pay'),
    path('vehicles/', views.vehicle_list, name='vehicle_list'),
    path('vehicles/create/', views.vehicle_create, name='vehicle_create'),
    path('vehicles/<str:pk>/update/', views.vehicle_update, name='vehicle_update'),
    path('vehicles/<str:pk>/delete/', views.vehicle_delete, name='vehicle_delete'),
    path('vehicles/<str:pk>/', views.vehicle_detail, name='vehicle_detail'),
    path('api/vehicles/', views.vehicle_data, name='vehicle_data'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
]

# Combine all URL patterns
urlpatterns = public_urlpatterns + dashboard_urlpatterns + admin_urlpatterns + app_urlpatterns 