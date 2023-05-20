from django.contrib import admin
from django.urls import include,path
from django.conf import settings
from django.conf.urls.static import static
# from django.conf.urls import handler404


urlpatterns = [
    
    path('receipt/', include('receipt.urls')),

    path('admin/',admin.site.urls),
    

]

if settings.DEBUG:
    urlpatterns+=static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)


# handler404 = 'demo.views.error_404'
