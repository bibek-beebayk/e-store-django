from django.contrib import admin
from . import models

# Register your models here.

admin.site.register(models.Promotion)
admin.site.register(models.Collection)

@admin.register(models.Product) # decorator to register a new model to the admin panel
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'unit_price', 'inventory_status', 'collection_title'] # select the fields to display
    list_editable = ['unit_price'] # make the fields editable
    list_per_page = 20 # items displayed per page
    list_select_related = ['collection'] # preload the collection field, helps to reduce the number pd quieried

    # function to make related field 'collection_title' accessible
    def collection_title(self, product): 
        return product.collection.title

    # add a new computed field 'inventory_status' to the table
    @admin.display(ordering='inventory') # decorator to define the ordering of the field items
    def inventory_status(self, product):
        if product.inventory<10:
            return 'Low'
        return 'Ok'

@admin.register(models.Customer) 
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'membership']
    list_editable = ['membership']
    ordering = ['first_name', 'last_name']
    list_per_page = 10

@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['placed_at', 'payment_status', 'customer']
    list_editable = ['payment_status']
    ordering = ['-placed_at']
    list_per_page = 20
    list_select_related = ['customer']

    def customer(self, Customer):
        return Customer.first_name
    



admin.site.register(models.OrderItem)
admin.site.register(models.Address)
admin.site.register(models.Cart)
admin.site.register(models.CartItem)