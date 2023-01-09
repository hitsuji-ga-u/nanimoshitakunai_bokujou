from django.shortcuts import render, redirect
from django.conf import settings
import requests

from pprint import pprint
from .animals import ANIMALS


BASE_URL = getattr(settings, "BASE_URL", None)
API_KEY = getattr(settings, "API_KEY", None)
HEADERS = {'X-MICROCMS-API-KEY': API_KEY}

# Create your views here.


def home(request):
    return render(request, 'nanimoshitakunai/home.html')

# カテゴリAPIから取得できる['contents']の内容
# {'category': 'blender',
#   'createdAt': '2022-11-05T16:38:08.855Z',
#   'id': 'blender',
#   'parentcategory': None,
#   'publishedAt': '2022-11-05T16:38:08.855Z',
#   'revisedAt': '2022-11-05T16:38:08.855Z',
#   'updatedAt': '2022-11-05T16:38:08.855Z'},


def animals_index(request):
    end_pt = '/category?fields=category,id&filters=parentcategory[not_exists]'
    main_categories = requests.request(
        'GET', BASE_URL+end_pt, headers=HEADERS).json()

    if main_categories['totalCount'] > len(ANIMALS):
        raise ValueError()

    for i, cat in enumerate(main_categories['contents']):
        ANIMALS[i]['id'] = cat['id']
        ANIMALS[i]['skill'] = cat['category']
    
    context = {
        'animals': ANIMALS
    }

    return render(request, 'nanimoshitakunai/animals-index.html', context)


def animal(request, animal_id):
    # 指定された親カテゴリを持つサブカテゴリのidを取得
    subcat_end_pt = f'/category?filters=parentcategory[equals]{animal_id}&fields=id'
    sub_cats = requests.request(
        'GET', BASE_URL+subcat_end_pt, headers=HEADERS).json()['contents']

    # subcategoryなしの記事取得
    posts = []
    mainposts_end_pt = f'/post?filters=category[equals]{animal_id}&fields=title,category,id,thumbnail'
    posts.append(requests.request('GET', BASE_URL+mainposts_end_pt,
                 headers=HEADERS).json()['contents'])

    # サブカテゴリに属する記事取得
    for sub_cat in sub_cats:
        subposts_end_pt = f"/post?filters=category[equals]{sub_cat['id']}&fields=title,category,id,description,thumbnail"
        posts.append(requests.request('GET', BASE_URL +
                     subposts_end_pt, headers=HEADERS).json()['contents'])

    animal_index = -1
    for i, ani in enumerate(ANIMALS):
        if ani['id'] == animal_id:
            animal_index = i
            break
    
    print(animal_index)
    if animal_index < 0:
        raise ValueError()

    context = {
        'animal': ANIMALS[animal_index],
        'cat_posts': posts
    }

    pprint(context)
    return render(request, 'nanimoshitakunai/animal.html', context)


def post(request, animal_id, cat_id, post_id):
    end_pt = f'/post?ids={post_id}'
    post_res = requests.request('GET', BASE_URL+end_pt, headers=HEADERS).json()
    context = {
        'post': post_res['contents'][0]
    }
    return render(request, 'nanimoshitakunai/post.html', context)


def about(request):
    return render(request, 'nanimoshitakunai/about.html')


def shop(request):
    return redirect('https://suzuri.jp/nanimoshitakunai?utm_source=others&utm_medium=social&utm_campaign=shop_share')
    # return render(request, 'nanimoshitakunai/about.html')


def playground(request):
    return render(request, 'nanimoshitakunai/playground.html')


def faq(request):
    return render(request, 'nanimoshitakunai/faq.html')
