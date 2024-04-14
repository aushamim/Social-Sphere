from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static

from SocialSphere import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("app_home.urls")),
    path("user/", include("app_user.urls")),
    path("dashboard/", include("app_dashboard.urls")),
    path("post/", include("app_postdetails.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
