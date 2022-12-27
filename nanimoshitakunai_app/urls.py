from django.urls import path

from . import views

# django-distill
from django_distill import distill_path
from . import views
from django.conf import settings
import requests
import math

from .animals import ANIMALS


url = getattr(settings, "BASE_URL", None)
api_key = getattr(settings, "API_KEY", None)
headers = {'X-MICROCMS-API-KEY': api_key}


def get_animals():
    for ani in ANIMALS:
        yield ani['id']


def get_posts():
    """
    記事詳細ページを生成するためのpost idを返す

    """

    end_point = f'/post?&fields=category,id'
    res = requests.request('GET', url=url + end_point, headers=headers).json()['contents']

    for post in res:
        post_id = post['id']
        category = post['category']['id']
        if post['category']['parentcategory'] is None:
            animal_id = post['category']['id']
        else:
            animal_id = post['category']['parentcategory']['id']
        yield {'cat_id': category, 'animal_id': animal_id, 'post_id': post_id}



# def get_pages():
#     """
#     ページ数を指定した一覧ページを生成するためのページ数を返す
#     """
#     post_total_count = _post_total_count()
#     num_page = math.ceil(post_total_count / limit)
#     for page_num in range(1, num_page + 1):
#         yield {'page': str(page_num)}



urlpatterns = [
    distill_path('', views.home, name='home',
        distill_file='home.html'),

    distill_path('about/', views.about, name='about'),
        # distill_file='about.html'),

    distill_path('omiyageshop/', views.shop, name='shop',
        distill_status_codes=(200, 302)),
    
    distill_path('playground/', views.access, name='playground',
        distill_file='playground.html'),
    
    distill_path('faq/', views.faq, name='faq',
        distill_file='faq.html'),
    
    distill_path('animals/', views.animals_index, name='animals_index'),

    distill_path('animals/<str:animal_id>-index/', views.animal, name='animal',
        distill_func=get_animals),

    distill_path('animals/<str:animal_id>/<str:cat_id>/<str:post_id>/', views.post, name='post',
        distill_func=get_posts),
]

# urlpatterns = [
#     path('', views.home, name='home',
#          distill_file='home.index'),
#     path('about', views.about, name='about',
#          distill_file='about.html'),

#     path('omiyageshop', views.shop, name='shop'),
    
#     path('playground', views.access, name='playground',
#          distill_file='access.html'),
#     path('faq', views.faq, name='faq',
#          distill_file='faq.html'),
    
#     path('animals/', views.animals_index, name='animals_index',
#          distill_file='animals_index.html'),
#     path('animals/<str:animal_id>-index', views.animal, name='animal',
#          distill_func='get_animals'),
#     path('animals/<str:animal_id>-index/<str:cat_id>/<str:post_id>', views.post, name='post',
#          distill_func='get_posts'),
# ]
