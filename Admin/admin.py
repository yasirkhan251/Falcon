from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.utils.html import format_html
from .models import Category, SubCategory, Product


# ============================================================
# CATEGORY ADMIN
# ============================================================
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('thumbnail', 'name', 'sku', 'model_code', 'created_at', 'updated_at')
    readonly_fields = ('sku', 'model_code', 'thumbnail')
    search_fields = ('name', 'sku', 'model_code')
    ordering = ('name',)
    list_per_page = 20

    def thumbnail(self, obj):
        """Show image preview in admin list."""
        if obj.image:
            return format_html(f'<img src="{obj.image.url}" width="60" height="60" style="object-fit:cover; border-radius:8px;" />')
        return "—"
    thumbnail.short_description = "Image Preview"


# ============================================================
# SUBCATEGORY ADMIN
# ============================================================
@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('thumbnail', 'name', 'category', 'sku', 'model_code', 'is_active', 'created_at')
    list_filter = ('category', 'is_active')
    search_fields = ('name', 'sku', 'model_code', 'category__name')
    readonly_fields = ('sku', 'model_code', 'thumbnail')
    ordering = ('category__name', 'name')
    list_per_page = 25

    def thumbnail(self, obj):
        """Show image preview in admin."""
        if obj.image:
            return format_html(f'<img src="{obj.image.url}" width="60" height="60" style="object-fit:cover; border-radius:8px;" />')
        return "—"
    thumbnail.short_description = "Image Preview"


# ============================================================
# PRODUCT ADMIN
# ============================================================
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'thumbnail', 'brand', 'model_name', 'category', 'subcategory',
        'sku', 'model_code', 'price', 'stock', 'is_active'
    )
    list_filter = ('brand', 'category', 'subcategory', 'is_active')
    search_fields = ('brand', 'model_name', 'sku', 'model_code', 'subcategory__name', 'category__name')
    readonly_fields = ('sku', 'model_code', 'thumbnail')
    ordering = ('brand', 'model_name')
    list_editable = ('price', 'stock', 'is_active')
    list_per_page = 30

    fieldsets = (
        ('Product Info', {
            'fields': (
                'brand', 'model_name', 'variant', 'description', 'price', 'stock', 'is_active'
            )
        }),
        ('Relations', {
            'fields': ('category', 'subcategory')
        }),
        ('Identifiers', {
            'fields': ('sku', 'model_code')
        }),
        ('Image', {
            'fields': ('image', 'thumbnail')
        }),
    )

    def thumbnail(self, obj):
        """Show product image preview in admin."""
        if obj.image:
            return format_html(f'<img src="{obj.image.url}" width="70" height="70" style="object-fit:cover; border-radius:8px;" />')
        return "—"
    thumbnail.short_description = "Image Preview"
