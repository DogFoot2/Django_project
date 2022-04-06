from unicodedata import name
from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.list, name="list"),
    path('create/', views.create, name="restaurant-create"),
    path('update/', views.update, name="restaurant-update"),
 #   path('detail/', views.detail, name="restaurant-detail"), 디테일 페이지를 좀 더 어떤 pk에 접근하고 있는지 편하게 알기 위해서 코드 변경
    path('restaurant/<int:id>/delete/', views.delete, name="restaurant-delete"),
    
    path('restaurant/<int:id>/', views.detail, name="restaurant-detail"), #직관적으로 재정의
    path('restaurant/<int:restaurant_id>/review/create/', views.review_create, name='review-create'),
    path('restaurant/<int:restaurant_id>/review/delete/<int:review_id>', views.review_delete, name="review-delete"),
    path('review/list/', views.review_list, name='review-list'),
]
