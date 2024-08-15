from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from inventory_app.views import SignUpView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('inventory_app.urls')),
    path('accounts/signup/', SignUpView.as_view(), name='signup'),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
]