### Example Project: Restaurant API with Django Rest Framework

---

#### Slide: Restaurant API Overview
**Restaurant API Overview**
- We will create a simple API to manage restaurants using Django Rest Framework.
- Features:
  - List all restaurants
  - Retrieve a single restaurant
  - Create a new restaurant
  - Update an existing restaurant
  - Delete a restaurant

---

#### Slide: Environment Setup
**Environment Setup**
1. **Create a Virtual Environment**
   ```bash
   python -m venv env
   ```
2. **Activate the Virtual Environment**
   - On Windows:
     ```bash
     .\env\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source env/bin/activate
     ```
3. **Update Virtual Environmeny**
   ```bash
   python -m pip install --upgrade pip
   ```
---

#### Slide: Project Setup
**Project Setup**
1. **Install and Configure DRF**
   ```bash
   pip install djangorestframework
   pip install pillow      # for media
   ```
2. **Create a Django Project**
   ```bash
   django-admin startproject restaurant_project
   cd restaurant_project
   ```
3. **Create a Django App**
   ```bash
   python manage.py startapp restaurant
   ```

   - Add `'rest_framework'` and `'restaurant'` to `INSTALLED_APPS` in `settings.py`.
  ```python
  INSTALLED_APPS = [
    "restaurant",
    "rest_framework",
    # rest of apps
  ]
  ```
---

#### Slide: Models
**Models**
- Create the Restaurant model in `restaurant/models.py`
  ```python
  from django.db import models

  class Restaurant(models.Model):
      name = models.CharField(max_length=100)
      address = models.CharField(max_length=255)
      rating = models.FloatField()

      def __str__(self):
          return self.name
  ```

- Run migrations
  ```bash
  python manage.py makemigrations
  python manage.py migrate
  ```

---

#### Slide: Serializers
**Serializers**
- Create a serializer for the Restaurant model in `restaurant/serializers.py`
  ```python
  from rest_framework import serializers
  from .models import Restaurant

  class RestaurantSerializer(serializers.ModelSerializer):
    
      class Meta:
          model = Restaurant
          fields = '__all__'
          read_only_fields = ('id',)  # Make 'id' read-only
  ```

---

#### Slide: Views (Function-Based)
**Function-Based View**
- Create function-based views in `restaurant/views.py`
  ```python
  from rest_framework.decorators import api_view
  from rest_framework.response import Response
  from rest_framework import status
  from .models import Restaurant
  from .serializers import RestaurantSerializer

  @api_view(['GET', 'POST'])
  def restaurant_list(request):
      if request.method == 'GET':
          restaurants = Restaurant.objects.all()
          serializer = RestaurantSerializer(restaurants, many=True)
          return Response(serializer.data)
      elif request.method == 'POST':
          serializer = RestaurantSerializer(data=request.data)
          if serializer.is_valid():
              serializer.save()
              return Response(serializer.data, status=status.HTTP_201_CREATED)
          return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  @api_view(['GET', 'PUT', 'DELETE'])
  def restaurant_detail(request, pk):
      try:
          restaurant = Restaurant.objects.get(pk=pk)
      except Restaurant.DoesNotExist:
          return Response(status=status.HTTP_404_NOT_FOUND)

      if request.method == 'GET':
          serializer = RestaurantSerializer(restaurant)
          return Response(serializer.data)
      elif request.method == 'PUT':
          serializer = RestaurantSerializer(restaurant, data=request.data)
          if serializer.is_valid():
              serializer.save()
              return Response(serializer.data)
          return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
      elif request.method == 'DELETE':
          restaurant.delete()
          return Response(status=status.HTTP_204_NO_CONTENT)
  ```

---

#### Slide: Views (Class-Based APIView)
**Class-Based View (APIView)**
- Create class-based views using APIView in `restaurant/views.py`
  ```python
  from rest_framework.views import APIView
  from rest_framework.response import Response
  from rest_framework import status
  from .models import Restaurant
  from .serializers import RestaurantSerializer

  class RestaurantList(APIView):
      def get(self, request):
          restaurants = Restaurant.objects.all()
          serializer = RestaurantSerializer(restaurants, many=True)
          return Response(serializer.data)

      def post(self, request):
          serializer = RestaurantSerializer(data=request.data)
          if serializer.is_valid():
              serializer.save()
              return Response(serializer.data, status=status.HTTP_201_CREATED)
          return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  class RestaurantDetail(APIView):
      def get_object(self, pk):
          try:
              return Restaurant.objects.get(pk=pk)
          except Restaurant.DoesNotExist:
              return Response(status=status.HTTP_404_NOT_FOUND)

      def get(self, request, pk):
          restaurant = self.get_object(pk)
          serializer = RestaurantSerializer(restaurant)
          return Response(serializer.data)

      def put(self, request, pk):
          restaurant = self.get_object(pk)
          serializer = RestaurantSerializer(restaurant, data=request.data)
          if serializer.is_valid():
              serializer.save()
              return Response(serializer.data)
          return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

      def delete(self, request, pk):
          restaurant = self.get_object(pk)
          restaurant.delete()
          return Response(status=status.HTTP_204_NO_CONTENT)
  ```

---

#### Slide: Views (Generic Views)
**Class-Based View (Generic Views)**
- Create class-based views using generic views in `restaurant/views.py`
  ```python
  from rest_framework import generics
  from .models import Restaurant
  from .serializers import RestaurantSerializer

  class RestaurantList(generics.ListCreateAPIView):
      queryset = Restaurant.objects.all()
      serializer_class = RestaurantSerializer

  class RestaurantDetail(generics.RetrieveUpdateDestroyAPIView):
      queryset = Restaurant.objects.all()
      serializer_class = RestaurantSerializer
  ```

---

#### Slide: URLs
**URLs**
- Configure URLs in `restaurant/urls.py`
  ```python
  from django.urls import path
  from .views import restaurant_list, restaurant_detail, RestaurantList, RestaurantDetail

  urlpatterns = [
      # Function-Based Views
      path('fbv/restaurants/', restaurant_list),
      path('fbv/restaurants/<int:pk>/', restaurant_detail),

      # Class-Based APIViews
      path('cbv/restaurants/', RestaurantList.as_view()),
      path('cbv/restaurants/<int:pk>/', RestaurantDetail.as_view()),

      # Generic Views
      path('gv/restaurants/', RestaurantList.as_view()),
      path('gv/restaurants/<int:pk>/', RestaurantDetail.as_view()),
  ]
  ```

- Include the app URLs in the project `urls.py`
  ```python
  from django.contrib import admin
  from django.urls import path, include

  urlpatterns = [
      path('admin/', admin.site.urls),
      path('api/', include('restaurant.urls')),
  ]
  ```

---

These slides provide an example project using Django Rest Framework with function-based views, class-based APIViews, and class-based generic views to manage a simple restaurant API. Additionally, it includes steps for setting up a virtual environment and making the 'id' field read-only in the serializer.