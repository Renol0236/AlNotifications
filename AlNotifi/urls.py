from django.urls import path, include
from .views import *

from rest_framework.routers import DefaultRouter

from django.conf import settings
from django.conf.urls.static import static


from .views import customhandler404

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView, name='logout'),
    path('profile/<int:id>/', ProfileView.as_view(), name='profile'),
    path('profile/update/', ProfileUpdateView.as_view(), name='profile_update'),
    path('oauth2/discord/login', discord_login, name='discord_oauth_login'),
    path('oauth2/discord/redirect', discord_login_redirect, name='discord_oauth_redirect'),
    path('api/create_notification/', NotificationsCreateView.as_view(), name='create_notification'),
    path('api/delete_notification/<int:id>/', NotificationsDeleteView.as_view(), name='delete_notification'),
    path('api/update_notification/<int:id>/', NotificationsUpdateView.as_view(), name='update_notification'),
]
handler404 = customhandler404
handler403 = customhandler403

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)