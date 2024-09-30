from django.urls import path
from . import views

app_name ='blog'

urlpatterns =[
    path('',views.home,name='home'),
    path('articles/',views.post_list,name='post-list'),
    path('post/<int:year>/<int:month>/<int:day>/<slug:post>/',views.post_detail,name='post-detail'),
    path('comment/<int:post_pk>/',views.post_comment,name='post-comment'),
    path('tag/<slug:tag_slug>/',views.post_list, name='post_list_by_tag'),
    path('articles/<str:category_name>/',views.posts_per_category,name='posts-per-category'),
    path('create-post/',views.create_post,name='create-post'),
    path('update-post/<int:pk>/',views.update_post,name='update-post'),
    path('privacy-policy/',views.privacy_policy,name='privacy-policy'),
    path('about/',views.about_us,name='about'),   
    path('terms/',views.terms,name='terms')
]