from django.urls import path
from .views import restaurant_list, restaurant_detail
# from .views import RestaurantList, RestaurantDetail

urlpatterns = [
    # Function-Based Views
    path('fbv/restaurants/', restaurant_list),
    path('fbv/restaurants/<int:pk>/', restaurant_detail),

    # # Class-Based APIViews
    # path('cbv/restaurants/', RestaurantList.as_view()),
    # path('cbv/restaurants/<int:pk>/', RestaurantDetail.as_view()),

    # # Generic Views
    # path('gv/restaurants/', RestaurantList.as_view()),
    # path('gv/restaurants/<int:pk>/', RestaurantDetail.as_view()),
]