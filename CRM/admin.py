from django.contrib import admin
from django.utils.html import format_html

# Register your models here.
from .models import User, Invoice, Customer, Client

from django.forms import BaseInlineFormSet

class LimitModelFormset(BaseInlineFormSet): #Limits Last3InvoicesInline to only show the most recent 3 invoices
    """ Base Inline formset to limit inline Model query results. """
    def __init__(self, *args, **kwargs):
        super(LimitModelFormset, self).__init__(*args, **kwargs)
        self.queryset = Invoice.objects.order_by('-invoice_date')[:3]

class Last3InvoicesInline(admin.TabularInline): #Inline model that shows only the most recent 3 invoices
    model = Invoice
    extra = 0
    can_delete = False
    
    formset = LimitModelFormset

class InvoicesInline(admin.TabularInline): #Inline model that shows the relevant users invoices
    model = Invoice
    extra = 0
    can_delete = False
    ordering = ['-invoice_date']


class UserAdmin(admin.ModelAdmin): #User model view
    
    list_display = ('username', 'email', 'total_invoiced_last_12_months', 'invoice_details')
    list_filter = ['invoicedOver1000']
    
    inlines = [Last3InvoicesInline, InvoicesInline]
    
    def invoice_details(self, obj): #provides a link that leads to the users detail page
        link = "<a href=http://localhost:8000/CRM/users/" + str(obj.username) + ">View</a>"
        return format_html(link)

class InvoiceAdmin(admin.ModelAdmin): #Invoice model view cannot delete
    
    list_display = ('__str__',)
    
    list_filter = ['user']
    
    def has_delete_permission(self, request, obj=None):
        return False

class CustomerAdmin(admin.ModelAdmin): #Customer model view cannot add
    
    list_display = ('__str__', 'has_unpaid_invoices')
    
    def has_add_permission(self, request, obj=None):
        return False
    
class ClientAdmin(admin.ModelAdmin): #Client model view
    
    list_display = ('__str__',)
    
admin.site.register(User, UserAdmin)
admin.site.register(Invoice, InvoiceAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Client, ClientAdmin)