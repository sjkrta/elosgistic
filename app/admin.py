from django.contrib import admin
from .models import Account, Address, Carousel, Category, Product, ProductImage, Review, Order, OrderItem, Coupon
from django.contrib.auth.admin import UserAdmin

# Register your models here.
admin.site.register(Address)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(Review)
admin.site.register(Carousel)
admin.site.register(Coupon)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user_id','total_price','delivery_choice','paid_status')
    ordering = ('paid_status',)

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('product_id','price','quantity','created_at')
    readonly_fields = ('created_at',)

@admin.register(Account)
class AccountAdmin(UserAdmin):
    list_display = ('email', 'username', 'date_joined',
                    'last_login', 'is_admin', 'is_staff', 'is_superuser')
    search_fields = ('email', 'username')
    readonly_fields = ('id', 'date_joined', 'last_login')
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

