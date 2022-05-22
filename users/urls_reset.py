from django.urls import path, re_path
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    re_path(r'^(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', auth_views.PasswordResetConfirmView.as_view(),
            name='password_reset_confirm'),
    path('password_reset_confirm/', auth_views. PasswordResetCompleteView.as_view(), name='password_reset_complete')
]
