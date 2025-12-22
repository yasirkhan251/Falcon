from django.shortcuts import render
from Admin.models import Category,SubCategory
from .models import *
# Create your views here.
def service(request):
    # 1. Define the desired order by category name
    # Ensure these names exactly match the 'name' field in your Category model
    desired_order = [
        "MOBILE", 
        "LAPTOP", 
        "TABLET", 
        "PC / DESKTOP", 
        "CCTV" 
    ]
    
    # 2. Fetch all categories
    all_categories = Category.objects.all()
    
    # 3. Create a dictionary mapping name to its desired index (0, 1, 2, 3, 4...)
    order_mapping = {name: index for index, name in enumerate(desired_order)}
    
    # 4. Sort the QuerySet (converted to a list) using the custom mapping
    # This ensures categories not in the list (if any) are added to the end.
    sorted_categories = sorted(
        all_categories,
        key=lambda category: order_mapping.get(category.name.upper(), len(desired_order))
    )
    
    # 5. Pass the correctly sorted list to the template
    context = {'categories': sorted_categories}
    return render(request, 'service/service.html',context)


def service_subcategories(request,slug):

    all_categories = Category.objects.filter(slug=slug).first()
    subcategories = all_categories.subcategories.all() if all_categories else []


    context = {'categories': subcategories,
               'allcat' : all_categories}
    return render(request, 'service/service_subcategories.html',context)



def service_product(request, category_slug, name):
    subcategory = SubCategory.objects.filter(name=name).first()
    products = subcategory.product_set.all() if subcategory else []
    Categorys = Category.objects.filter(slug=category_slug).first()
    
    context = {
        'products': products,
        'category': Categorys,
        'subcategory': subcategory,
    }
    return render(request, 'service/service_products.html', context)





# def service_for(request, category_slug, name ,model_name):
#    category = Category.objects.filter(slug=category_slug).first()
#    subcategory = SubCategory.objects.filter(name=name).first()
#    products = Product.objects.filter(model_name=model_name) 
   
   
#    service_cat = ServiceCategory.objects.all()
#    SP =  ServiceProduct.objects.filter(products = products )
#    print(products)
     
    
#    return render(request, 'service/service_for.html', {'products': SP})  


def service_for(request, category_slug, name, model_name):

    # Get category
    category = Category.objects.filter(slug=category_slug).first()

    # Get subcategory
    subcategory = SubCategory.objects.filter(
        name__iexact=name,
        category=category
    ).first()

    # Get products (all variants)
    products = Product.objects.filter(
        model_name__iexact=model_name,
        subcategory=subcategory
    )

    # Get all service products for this model
    SP = ServiceProduct.objects.filter(
        Product__in=products
    ).distinct()

    # ⭐ Get all ServiceCategory objects for this model
    service_categories = ServiceCategory.objects.filter(
        serviceproduct__Product__in=products
    ).distinct()

    return render(request, 'service/service_for.html', {
        'products': SP,
        'product_list': products,
        'service_categories': service_categories,
        'category': category,
        'subcategory': subcategory,
    })
    
    
    
    