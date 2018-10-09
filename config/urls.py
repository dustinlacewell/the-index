from django.conf import settings
from django.urls import include, path, re_path
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView
from django.views import defaults as default_views

from wagtail.core import urls as wagtail_urls
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.documents import urls as wagtaildocs_urls
from wagtail.images.views.serve import ServeView

from search import views as search_views

from wagtail_feeds.feeds import (
    BasicFeed, BasicJsonFeed, ExtendedFeed, ExtendedJsonFeed
)

urlpatterns = [
    # path("", TemplateView.as_view(template_name="pages/home.html"), name="home"),
    path(
        "about/",
        TemplateView.as_view(template_name="pages/about.html"),
        name="about",
    ),
    # Django Admin, use {% url 'admin:index' %}
    path(settings.ADMIN_URL, admin.site.urls),
    # User management
    path(
        "users/",
        include("the_index.users.urls", namespace="users"),
    ),
    path("accounts/", include("allauth.urls")),

    # Wagtail
    re_path(r'^edit/', include(wagtailadmin_urls)),
    re_path(r'^search/$', search_views.search, name='search'),
    re_path(r'^documents/', include(wagtaildocs_urls)),
    re_path(r'^news/feed/basic$', BasicFeed(), name='basic_feed'),
    re_path(r'^news/feed/extended$', ExtendedFeed(), name='extended_feed'),
    re_path(r'^news/feed/basic.json$', BasicJsonFeed(), name='basic_json_feed'),
    re_path(r'^news/feed/extended.json$', ExtendedJsonFeed(), name='extended_json_feed'),

    re_path(
        r'^images/([^/]*)/(\d*)/([^/]*)/[^/]*$',
        ServeView.as_view(), name='wagtailimages_serve'
    ),

    re_path(r'^pages/', include(wagtail_urls)),

    # Optional URL for including your own vanilla Django urls/views
    # re_path(r'', include('myapp.urls')),

    # For anything not caught by a more specific rule above, hand over to
    # Wagtail's serving mechanism
    re_path("", include(wagtail_urls)),

] + static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
)

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
