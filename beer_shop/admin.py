from django.contrib import admin
from .models import Beer, Review, Order, Category

@admin.register(Beer)
class BeerAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand', 'price', 'stock', 'alcohol_content', 'category')
    list_filter = ('brand', 'category')
    search_fields = ('name', 'brand')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'beer', 'rating', 'created_at')
    list_filter = ('rating',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'status', 'order_date', 'total_price')
    list_filter = ('status', 'order_date')
    search_fields = ('user__username',)
