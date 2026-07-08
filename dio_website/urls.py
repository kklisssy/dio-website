from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from wagtail import urls as wagtail_urls
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.documents import urls as wagtaildocs_urls
from base.views import consultation_request, confirm_subscribe, confirm_unsubscribe, new_subscribe

urlpatterns = [
    path("django-admin/", admin.site.urls),
    path("admin/", include(wagtailadmin_urls)),
    path("documents/", include(wagtaildocs_urls)),
    path("consultation_request/", consultation_request, name="consultation_request"),

    path("newsletter/subscribe/", new_subscribe, name="newsletter_subscribe"),
    path("newsletter/confirm/<uuid:token>/", confirm_subscribe, name="newsletter_confirm"),
    path("newsletter/unsubscribe/<uuid:token>/", confirm_unsubscribe, name="newsletter_unsubscribe"),

    path("", include(wagtail_urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
