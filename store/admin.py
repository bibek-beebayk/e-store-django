
from django.contrib import admin, messages
from django.db.models.query import QuerySet
from django.http.request import HttpRequest
from . import models
from django.db.models import aggregates

# Register your models here.


class InventoryFilter(admin.SimpleListFilter):
    title = 'inventory'
    parameter_name = 'inventory'

    def lookups(self, request, model_admin):
        return [
            ('<10', 'Low')
        ]

    def queryset(self, request, queryset: QuerySet):
        if self.value() == '<10':
            return queryset.filter(inventory__lt=10)

admin.site.register(models.Promotion)

@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['id','title' ] # add a new list_item 'products_count'
    search_fields = ['title']

    # @admin.display(ordering='products_count')
    # def products_counts(self, collection):
    #     return collection.products_count

    # def get_queryset(self, request):
    #     return super().get_queryset(request).annotate(
    #         products_count= aggregates.Count('product')
    #     )


@admin.register(models.Product) # decorator to register a new model to the admin panel
class ProductAdmin(admin.ModelAdmin):
    autocomplete_fields = ['collection']
    prepopulated_fields = {
        'slug': ['title']
    }
    actions = ['clear_inventory']
    list_display = ['title', 'unit_price', 'inventory_status', 'collection_title'] # select the fields to display
    list_editable = ['unit_price'] # make the fields editable
    list_per_page = 20 # items displayed per page
    list_select_related = ['collection'] # preload the collection field, helps to reduce the number pd quieried
    list_filter = ['collection', 'last_update', InventoryFilter]

    # function to make related field 'collection_title' accessible
    def collection_title(self, product): 
        return product.collection.title

    # add a new computed field 'inventory_status' to the table
    @admin.display(ordering='inventory') # decorator to define the ordering of the field items
    def inventory_status(self, product):
        if product.inventory<10:
            return 'Low'
        return 'Ok'

    @admin.action(description='Clear inventory')
    def clear_inventory(self, request, queryset: QuerySet):
        updated_count = queryset.update(inventory=0)
        self.message_user(
            request,
            f'{updated_count} records were successfully updated',
            messages.SUCCESS
        )


@admin.register(models.Customer) 
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'membership']
    list_editable = ['membership']
    ordering = ['first_name', 'last_name']
    list_per_page = 10
    search_fields = ['first_name__istartswith', 'last_name__istartswith']

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