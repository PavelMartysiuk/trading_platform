from users.models import User, WatchList, Item, Inventory, Currency, Offer, Trade

from django.contrib import admin


class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'balance']
    list_display_link = ['first_name', ]


class WatchListAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'item']
    list_display_links = ['id', ]


class ItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'code', 'name', 'logo',
                    'is_active', 'actual_price',
                    'currency', 'details']
    list_display_links = ['name', 'logo', 'id']


class InventoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'item', 'quantity', 'user']
    list_display_links = ['id']


class CurrencyAdmin(admin.ModelAdmin):
    list_display = ['id', 'code', 'name']
    list_display_links = ['id']


class OfferAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'item', 'entry_quantity', 'item', 'order_type']
    list_display_links = ['id']


class TradeAdmin(admin.ModelAdmin):
    list_display = ['id', 'item', 'seller', 'buyer',
                    'quantity', 'unit_price',
                    'buyer_offer', 'seller_offer', ]
    list_display_links = ['id']


admin.site.register(User, UserAdmin)
admin.site.register(WatchList, WatchListAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(Currency, CurrencyAdmin)
admin.site.register(Inventory, InventoryAdmin)
admin.site.register(Offer, OfferAdmin)
admin.site.register(Trade, TradeAdmin)
