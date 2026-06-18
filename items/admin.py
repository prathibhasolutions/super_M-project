from django.contrib import admin
from .models import Item, profit, Members,Dealer
# Register your models here.



class ItemAdmin(admin.ModelAdmin):
  list_display = ("date_arrived", "product_name", "price", "quantity", "expiry_date")

admin.site.register(Item, ItemAdmin)
admin.site.register(profit)
admin.site.register(Members)
admin.site.register(Dealer)