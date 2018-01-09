from django.conf.urls import include, url

# from django.contrib import admin
# admin.autodiscover()
from master import views
# Examples:
# url(r'^$', 'gettingstarted.views.home', name='home'),
# url(r'^blog/', include('blog.urls')),

urlpatterns = [
    url(r'^$', views.home),
    url(r'^set_bus_location/$', views.set_bus_location),
    url(r'^get_bus_location/$', views.get_bus_location),
    url(r'^get_bus_status/$', views.get_bus_status),
]
