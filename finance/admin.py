# finance/admin.py
from django.contrib import admin
from .models import Account, Category, Transaction

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'balance')
    search_fields = ('name', 'owner__username')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'owner')
    search_fields = ('name', 'owner__username')

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('date', 'account', 'category', 'amount', 'owner')
    search_fields = ('description', 'owner__username')
    list_filter = ('date', 'category')
