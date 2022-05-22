from django.urls import path, include,re_path
from users import urls_reset
from . import views

urlpatterns = [
    path('index/', views.index, name='index'),
    path('logout/', views.logout, name='logout'),
    path('login/', views.login, name='login'),
    path('add_resource/', views.add_resources, name='add_resource'),
    path('all_resources/', views.active_resources, name='active_resources'),
    path('delete/<int:id>', views.set_inactive, name='set_inactive'),
    path('edit/<int:id>', views.edit_resource, name='edit_resource'),
    path('password-reset/', include(urls_reset)),
    path('signup/<int:id>', views.signup, name='signup'),
    path('signup_regular/<int:id>', views.signup, name='signup_regular'),
    path('activate/<uidb64>/<token>/',views.activate, name='activate'),


]
