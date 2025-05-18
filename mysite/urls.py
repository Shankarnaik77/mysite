"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django_distill import distill_path

def get_index():
    # This function only returns once as there is only one index page
    return [{}]

urlpatterns = [
    # Add both with and without trailing slash to avoid 301 redirects
    distill_path('',
        TemplateView.as_view(template_name='mysite/index.html'),
        name='home',
        distill_func=get_index,
        distill_file='index.html'
    ),
    distill_path('/',
        TemplateView.as_view(template_name='mysite/index.html'),
        name='home_slash',
        distill_func=get_index,
        distill_file='index.html'
    ),
    path("myapp/", include("myapp.urls")),
    path("admin/", admin.site.urls),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
