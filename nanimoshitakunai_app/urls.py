from django.urls import path

from . import views



urlpatterns = [
    path('', views.home, name='home'),
    path('about', views.about, name='about'),
    path('omiyageshop', views.shop, name='shop'),
    path('information', views.access, name='access'),
    path('playground', views.access, name='playground'),
    path('faq', views.faq, name='faq'),
    
    path('animals/', views.animals_index, name='animals_index'),
    path('animals/<str:animal_id>-index', views.animal, name='animal'),
    path('animals/<str:animal_id>-index/<str:cat_id>/<str:post_id>', views.post, name='post'),
]
