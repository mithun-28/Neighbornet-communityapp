from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from neighbornet import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/', views.signup_view, name='signup'),
    path('', views.login_view, name='login'),
    path('group/', views.group_page_view, name='group_page'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('service_page/', views.service_page_view, name='service_page'),
    path('sell_page/', views.sell_page_view, name='sell_page'),
    path('business_page/', views.business_page_view, name='business_page'),
]

from django.conf import settings
from django.conf.urls.static import static
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)