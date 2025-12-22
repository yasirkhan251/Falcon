from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("", service, name="service"),
    path("<slug:slug>/",service_subcategories , name="service_subcategories"),
    path("<slug:category_slug>/<str:name>/",service_product , name="service_products"),
    path("<slug:category_slug>/<str:name>/<str:model_name>", service_for , name="service_for"),
#    path('category/<slug:slug>/', category_detail, name='category_detail'),
# This name must match the 'category_detail' used in the template
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
    
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)