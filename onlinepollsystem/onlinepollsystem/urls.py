"""
URL configuration for onlinepollsystem project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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

urlpatterns = [
    path('api/admin/', admin.site.urls),
    path('api/v1/auth/', include('users.auth_urls')),
    path('api/v1/users/', include('users.urls')),
    path('api/v1/polls/', include('polls.urls')),
    path('api/v1/options/', include('polls.option_urls')),
    path('api/v1/votes/', include('votes.urls')),
    path('api/v1/token/', include('users.token_urls')),

    path('api/docs/', include('onlinepollsystem.swagger_urls')),
]
