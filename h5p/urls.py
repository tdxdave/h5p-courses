from django.conf.urls import url

from . import views

urlpatterns = [
    url(r"^$", views.h5p_content_list, name="h5p_content_list"),
    url(r"^view/([0-9]*)/", views.h5p_view_content, name="h5p_view_content"),
    url(r"^edit/([0-9]*)", views.h5p_editor, name="h5p_editor"),
    url(r"^add/", views.h5p_add_content, name="h5p_add_content"),
    url(r"^ajax/", views.h5p_ajax, name="h5p_ajax"),
    url(r"^update/", views.h5p_h5p_update, name="h5p_h5p_update"),
]
