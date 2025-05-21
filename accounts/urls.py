from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
    path("login/",views.login_user, name="login"),
    path("profile/",views.profile_user, name="profile"),
    path("register/",views.register_user, name="register"),
    path("logout/",views.logout_user, name="logout"),
    
]

#urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
