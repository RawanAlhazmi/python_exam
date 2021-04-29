from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),

    # Registration & Login Section
    path('register', views.register),
    path('login', views.login),


    path('wishes', views.wishes),
    path('wishes/new', views.new_wish),
    path('wishes/create', views.create_wish),
    path('wishes/stats', views.stats_wish),
    path('wishes/<int:w_id>/update', views.update_wish),
    path('wishes/<int:w_id>/granted', views.granted_wish),
    path('wishes/edit/<int:w_id>', views.edit_wish),
    path('wishes/<int:w_id>/like', views.like_wish),
    path('wishes/<int:w_id>/delete', views.delete_wish),

    # Logout Section
    path('destroy', views.destroy),
]
