from django.conf.urls import url, include, patterns
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from beaconapp import settings
from shopping_cart import views

urlpatterns = patterns ('',
    url(r'^$', 'profiles.views.home', name='home'),
    url(r'^about/$', 'profiles.views.about', name='about'),
    url(r'^profile/$', 'profiles.views.profile', name='profile'),
    url(r'^contact/$', 'contact.views.contact', name='contact'),
    url(r'^checkout/$', 'checkout.views.checkout', name='checkout'),
    url(r'^add_to_cart/', views.add_to_cart, name='add_to_cart'),
    url(r'^view_cart/', views.view_cart, name='view_cart'),
    url(r'^inline_add_to_cart/', views.inline_add_to_cart, name='inline_add_to_cart'),
    url(r'^previous_orders/', views.previous_orders, name='previous_orders'),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
   urlpatterns += static(settings.STATIC_URL,document_root = settings.STATIC_ROOT)
   urlpatterns += static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)