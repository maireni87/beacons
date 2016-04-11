from django.conf.urls import url, include, patterns
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from app.views import *


urlpatterns = patterns ('',
    url(r'^$', 'profiles.views.home', name='home'),
    url(r'^about/$', 'profiles.views.about', name='about'),
    url(r'^profile/$', 'profiles.views.profile', name='profile'),
    url(r'^contact/$', 'contact.views.contact', name='contact'),
    url(r'^checkout/$', 'checkout.views.checkout', name='checkout'),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^/?$', AppLandingView.as_view()),
    url(r'^explore/?$', AppLandingView.as_view()),
    url(r'^properties/?([0-9]+)?$', PropertiesView.as_view()),
    url(r'^propertyMetas/?([0-9]+)?$', PropertyMetasView.as_view()),
    url(r'^propertyStatuses/?([0-9]+)?$', PropertyStatusView.as_view()),
    url(r'^propertyMeta/?$', PropertyMetaView.as_view()),
    
)

if settings.DEBUG:
   urlpatterns += static(settings.STATIC_URL,document_root = settings.STATIC_ROOT)
   urlpatterns += static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)