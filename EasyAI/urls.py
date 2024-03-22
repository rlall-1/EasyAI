"""EasyAI URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path, include
from data_upload_app import views
from data_preproc_app import views as dpre

from . import settings
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home),
    path('faq.html', views.faq),
    path('aboutme.html', views.aboutme),
    path('data_preproc_app/', include('data_preproc_app.urls')),
    path('model_generated_app/', include('model_generated_app.urls')),
    path('sentiment_analysis_app/', include('sentiment_analysis_app.urls')),
    path('unsupervised_learning_app/', include('unsupervised_learning_app.urls')),
    path('api/', include('api.urls')),



]

# urlpatterns += staticfiles_urlpatterns()
# urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

