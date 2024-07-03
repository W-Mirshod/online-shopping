from django.contrib import admin

from shopping.models import Category, Product, Comment, Order


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    fields = ('name', 'description', 'price', 'discount', 'rating', 'quantity', 'is_available', 'image', 'category')
    list_display = ('name', 'is_available', 'slug', 'price', 'quantity', 'rating')
    list_filter = ('name', 'price', 'quantity')
    search_fields = ('name', 'description')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    fields = ('title',)
    list_display = ('title', 'slug', 'id')
    search_fields = ('title', 'slug')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'message', 'email', 'is_accessible', 'product', 'created_at')
    search_fields = ('name', 'email')
    list_filter = ('name', 'email', 'is_accessible', 'product')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'address', 'quantity', 'product', 'created_at')
    search_fields = ('name', 'email')
    list_filter = ('name', 'email', 'product', 'created_at')
