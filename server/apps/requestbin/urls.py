from django.urls import re_path

from . import views

urlpatterns = [
    re_path(r'^bin/(?P<bin_id>\d+)/(?P<path>.*)', views.catch_request),
    re_path(r'^export_bin/(?P<bin_id>\d+)/?', views.export_bin),
]
