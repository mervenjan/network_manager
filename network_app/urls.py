from django.conf.urls import url,include
from . import views

app_name = 'network_app'
urlpatterns = [
    url(r'^$',views.index),
    url(r'^index/$',views.index),
    url(r'^login/$',views.login),
    url(r'^logout/$',views.logout),
    url(r'^backup/$',views.backup),
    url(r'^backup_network_config/$',views.backup_network_config),


]





