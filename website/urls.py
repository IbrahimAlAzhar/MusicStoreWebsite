"""website URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static
from django.conf.urls import include,url

urlpatterns = [
    path('admin/', admin.site.urls),
    path('music/', include('music.urls')),
]
if settings.DEBUG:  # when DEBUG mode is on then you add to in urlpatterns,debug mode is on in developing mode,when your project is production mode then you have to off this mode
    # this MEDIA_URL add to urlpatterns because of we add media in settings to upload files
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)