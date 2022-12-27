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
    # # <animal_id>-index/<cat_id>　のとこだけやってみる
    # end_point = f'/category?&fields=category,id'
    # end_point = f'/category'
    # res = requests.request('GET', url=url + end_point, headers=headers).json()['contents']

    # print (' >> ' * 10)
    # from pprint import pprint
    # pprint(res)
    # print (' <<  ' * 10)
    # for cat in res:
    #     if cat['parentcategory'] is None:
    #         animal_id = cat['id']
    #     else:
    #         animal_id = cat['parentcategory']['id']
    #     cat_id = cat['id']
    #     yield {'animal_id': animal_id, 'cat_id': cat_id}

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


# def get_tags():
#     """
#     タグとページ数を指定した一覧ページを生成するための
#     タグ＋ページ数を返す
#     """
#     tag_total_count = _tag_total_count()
#     post_total_count = _post_total_count()
#     # タグの一覧を取得
#     end_point = f'/tag?limit={tag_total_count}&fields=id'
#     tag_res = requests.request(method='GET',
#                                url=url + end_point,
#                                headers=headers)

#     for data in tag_res.json()['contents']:
#         # タグIDを取得
#         tag_id = data['id']
#         # タグに紐づく記事が何個あるか？を取得
#         res = requests.request(method='GET',
#                                url=url + f'/post?limit={post_total_count}&filters=tag[contains]{tag_id}',
#                                headers=headers)
#         post_total_count_with_tag = res.json()['totalCount']
#         # 一ページあたりの記事数で割り出して、何ページあるか？を計算
#         num_page = math.ceil(post_total_count_with_tag / limit)
#         # タグIDとページ数をyield
#         for page_num in range(1, num_page + 1):
#             yield {'tag_id': tag_id, 'page': str(page_num)}


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
        # distill_file='about.html'),
        # distill_file='animals-index.html'),

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
