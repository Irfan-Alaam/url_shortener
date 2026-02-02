from django.urls import path, include
from django.views.generic import RedirectView
from django.contrib import admin
from django.contrib.auth import views as auth_views
from shortener.views import signup_view,login_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/',login_view,name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('signup/', signup_view, name='signup'),
    path('', RedirectView.as_view(url='/my-urls/')),
    path('', include('shortener.urls')),
]
