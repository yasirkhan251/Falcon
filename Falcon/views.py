from django.shortcuts import render
from Admin.models import *

# Create your views here.

def index(request):
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
    return render(request, 'Falcon/index.html',context)
def about(request):
    return render(request, 'Falcon/about.html')

def contact(request):
    return render(request, 'Falcon/contact.html')
def team(request):
    return render(request, 'Falcon/team.html')
def pricing(request):
    return render(request, 'Falcon/pricing.html')
def privacy(request):
    return render(request, 'Falcon/privacy.html')
def terms(request):
    return render(request, 'Falcon/terms.html')
def maintenance(request):
    return render(request, 'Falcon/maintenance.html')
def comingsoon(request):
    return render(request, 'Falcon/coming-soon.html')
def search(request):
    return render(request, 'Falcon/search.html')
def blog(request):
    return render(request, 'Falcon/blog.html')
def error(request):
    return render(request, 'Falcon/404.html')
def faq(request):
    return render(request, 'Falcon/faq.html')
def service1(request):
    return render(request, 'Falcon/service1.html')




def elements(request):
    return render(request, 'elements.html')     



def appointment(request):
    return render(request, 'appointment.html')
def department(request):
    return render(request, 'department.html')
def departmentsingle(request):
    return render(request, 'department-single.html')
def doctor(request):
    return render(request, 'doctor.html')
def doctorsingle(request):
    return render(request, 'doctor-single.html')

def gallery(request):
    return render(request, 'gallery.html')
def testimonial(request):
    return render(request, 'testimonial.html')


