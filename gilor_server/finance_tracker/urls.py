# finance_tracker/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'familymembers', views.FamilyMemberViewSet)
router.register(r'accounts', views.AccountViewSet)
router.register(r'categories', views.TransactionCategoryViewSet)
router.register(r'transactions', views.TransactionViewSet)
router.register(r'budgets', views.BudgetViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('me/', views.MyFamilyMemberView.as_view(), name='me'),
    path('register/', views.UserRegistrationView.as_view(), name='api_register'), # API endpoint for registration
    # Custom report endpoints
    path('reports/balance_by_kid/<int:member_id>/', views.get_balance_by_kid, name='balance_by_kid'),
    path('reports/transaction_history/<int:member_id>/', views.get_transaction_history_by_kid, name='transaction_history_by_kid'),
    # finance_tracker/urls.py
    path('dashboard.html', views.dashboard_view, name='dashboard'), 
    path('login.html', views.login_view, name='login'), 
    path('register.html', views.register_view, name='register_html'),
    
]
