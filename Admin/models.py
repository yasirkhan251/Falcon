
# Create your models here.
from django.db import models
from django.utils.text import slugify


# ============================================================
# CATEGORY MODEL
# ============================================================
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    model_code = models.CharField(max_length=100, blank=True, null=True, help_text="Internal manufacturer/vendor code")
    sku = models.CharField(max_length=50, unique=True, editable=False)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)
    slug = models.SlugField(max_length=150, unique=True, blank=True)
    display_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']

    def save(self, *args, **kwargs):
        # Generate slug automatically
        if not self.slug:
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)

        # Generate SKU after ID exists
        if not self.sku:
            short_name = ''.join(e for e in self.name if e.isalnum())[:3].upper()
            self.sku = f"FTW-CAT-{short_name}"
            super().save(update_fields=['sku'])

        # Auto-create a default model code if empty
        if not self.model_code:
            self.model_code = f"MDL-{short_name}-{self.id}"
            super().save(update_fields=['model_code'])

    def __str__(self):
        return f"{self.name} ({self.sku})"


# ============================================================
# SUBCATEGORY MODEL
# ============================================================
class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    model_code = models.CharField(max_length=100, blank=True, null=True, help_text="Internal manufacturer/vendor code")
    sku = models.CharField(max_length=60, unique=True, editable=False)
    image = models.ImageField(upload_to='subcategories/', blank=True, null=True)
    slug = models.SlugField(max_length=150, unique=True, blank=True)
    is_active = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Subcategories"
        unique_together = ('category', 'name')
        ordering = ['category__name', 'display_order', 'name']

    def save(self, *args, **kwargs):
        # Generate slug automatically
        if not self.slug:
            self.slug = slugify(f"{self.category.name}-{self.name}")

        super().save(*args, **kwargs)

        # Generate SKU after save (needs ID)
        if not self.sku:
            cat_code = ''.join(e for e in self.category.name if e.isalnum())[:3].upper()
            sub_code = ''.join(e for e in self.name if e.isalnum())[:3].upper()
            self.sku = f"FTW-SUB-{cat_code}-{sub_code}"
            super().save(update_fields=['sku'])

        # Auto-create model_code if not provided
        if not self.model_code:
            cat_code = ''.join(e for e in self.category.name if e.isalnum())[:3].upper()
            sub_code = ''.join(e for e in self.name if e.isalnum())[:3].upper()
            self.model_code = f"MDL-{cat_code}-{sub_code}-{self.id}"
            super().save(update_fields=['model_code'])

    def __str__(self):
        return f"{self.category.name} → {self.name} ({self.sku})"


# ============================================================
# PRODUCT MODEL
# ============================================================
class Product(models.Model):
    BRAND_CHOICES = [
        ('APL', 'Apple'),
        ('SMG', 'Samsung'),
        ('DEL', 'Dell'),
        ('HP', 'HP'),
        ('OPP', 'Oppo'),
        ('XMI', 'Xiaomi'),
        ('HIK', 'HikVision'),
    ]

    company_code = "FTW"  # Falcon Tech World prefix

    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    brand = models.CharField(max_length=3, choices=BRAND_CHOICES)
    model_name = models.CharField(max_length=100)
    variant = models.CharField(max_length=50, blank=True, null=True)  # e.g., Color/Size
    description = models.TextField(blank=True, null=True)
    model_code = models.CharField(max_length=100, blank=True, null=True, help_text="Internal manufacturer/vendor code")
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    stock = models.PositiveIntegerField(default=0, blank=True, null=True)
    sku = models.CharField(max_length=50, unique=False, editable=False)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Products"
        ordering = ['brand', 'model_name']

    def save(self, *args, **kwargs):
        # Auto-generate SKU if not present
        model_code = ''.join(e for e in self.model_name if e.isalnum())[:4].upper()
        if not self.sku:
            cat_code = ''.join(e for e in self.category.name if e.isalnum())[:3].upper()
            brand_code = self.brand.upper()
            
            variant_code = (self.variant or '')[:3].upper()
            self.sku = f"{self.company_code}-{cat_code}-{brand_code}-{model_code}-{variant_code}".strip('-')

    
        # Auto-generate model_code if missing
        if not self.model_code:
            self.model_code = f"MDL-{self.brand}-{model_code}-{self.id or ''}"

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.brand} {self.model_name} ({self.sku})"



