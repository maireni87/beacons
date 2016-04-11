from django.conf.urls import url, include, patterns
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = patterns ('',
    url(r'^$', 'profiles.views.home', name='home'),
    url(r'^about/$', 'profiles.views.about', name='about'),
    url(r'^profile/$', 'profiles.views.profile', name='profile'),
    url(r'^contact/$', 'contact.views.contact', name='contact'),
    url(r'^checkout/$', 'checkout.views.checkout', name='checkout'),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
   urlpatterns += static(settings.STATIC_URL,document_root = settings.STATIC_ROOT)
   urlpatterns += static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)