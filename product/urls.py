from django.urls import path
from . import views

urlpatterns = [
    path('', views.ProductListAPIView.as_view()),
    path('<int:id>/', views.ProductDetailAPIView.as_view()),

    path('reviews/', views.ReviewListAPIView.as_view()),
    path('reviews/<int:id>/', views.ReviewDetailAPIView.as_view()),

    path('categories/', views.CategoryListAPIView.as_view()),
    path('categories/<int:id>/', views.CategoryDetailAPIView.as_view()),

    path('viewset/', views.ProductViewSet.as_view({
    'get': 'list', 'post': 'create'
    })),

    path('viewset/<int:pk>/', views.ProductViewSet.as_view({
    'get': 'retrieve', 'put': 'update', 'delete': 'destroy'
    })),
]