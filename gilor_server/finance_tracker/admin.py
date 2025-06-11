# finance_tracker/admin.py
from django.contrib import admin
from .models import FamilyMember, Account, TransactionCategory, Transaction, Budget

@admin.register(FamilyMember)
class FamilyMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'user',)
    search_fields = ('name', 'user__username',)

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('member', 'account_name', 'balance_current', 'currency',)
    list_filter = ('member', 'currency',)
    search_fields = ('account_name',)
    raw_id_fields = ('member',) # Useful for large numbers of members

@admin.register(TransactionCategory)
class TransactionCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'type',)
    list_filter = ('type',)
    search_fields = ('name',)

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('date', 'account', 'category', 'amount', 'type', 'description',)
    list_filter = ('account__member', 'type', 'category', 'date',)
    search_fields = ('description',)
    raw_id_fields = ('account', 'category',)
    date_hierarchy = 'date'

@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ('member', 'category', 'amount_monthly', 'start_date', 'end_date',)
    list_filter = ('member', 'category', 'start_date',)
    raw_id_fields = ('member', 'category',)