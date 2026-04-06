from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Avg
from django.db.models import Count

from .models import Category, Product, Review
from .serializers import CategorySerializer, ProductSerializer, ReviewSerializer


@api_view(['GET'])
def category_list_api_view(request):
    categories = Category.objects.annotate(product_count=Count('products'))
    data = CategorySerializer(categories, many=True).data
    return Response(data=data)


@api_view(['GET'])
def category_detail_api_view(request, id):
    try:
        category = Category.objects.get(id=id)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)

    data = CategorySerializer(category, many=False).data
    return Response(data=data)



@api_view(['GET'])
def product_list_api_view(request):
    products = Product.objects.all().annotate(rating=Avg('reviews__stars'))
    data = ProductSerializer(products, many=True).data
    return Response(data=data)


@api_view(['GET'])
def product_detail_api_view(request, id):
    try:
        product = Product.objects.prefetch_related('reviews').get(id=id)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)

    data = ProductSerializer(product, many=False).data
    return Response(data=data)


@api_view(['GET'])
def review_list_api_view(request):
    reviews = Review.objects.all()
    data = ReviewSerializer(reviews, many=True).data
    return Response(data=data)



@api_view(['GET'])
def review_detail_api_view(request, id):
    try:
        review = Review.objects.get(id=id)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)

    data = ReviewSerializer(review, many=False).data
    return Response(data=data)

@api_view(['GET'])
def product_reviews_api_view(request):
    products = Product.objects.all().prefetch_related('reviews').all()
    data = ProductSerializer(products, many=True).data
    return Response(data)