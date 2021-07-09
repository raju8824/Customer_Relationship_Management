"""crm URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.conf.urls.static import static
from lead.views import home, Signupviews
from django.conf import settings
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home.as_view(), name='home'),
    path('login/', LoginView.as_view(), name='login'),
    path('signup/', Signupviews.as_view(), name='signup'),

    path('logout/', LogoutView.as_view(), name='logout'),
    path('reset-password/', PasswordResetView.as_view(), name='reset-password'),
    path('password_reset_complete/', PasswordResetCompleteView.as_view(),
         name='password_reset_complete'),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(),
         name='password-reset-confirm'),
    path('password_reset_done/', PasswordResetDoneView.as_view(),
         name='password_reset_done'),
    path('lead/', include('lead.urls', namespace='lead')),
    path('agent/', include('agent.urls', namespace='agent')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          documetn_root=settings.STATIC_ROOT)
