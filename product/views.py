from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Avg
from django.db.models import Count

from .models import Category, Product, Review
from .serializers import CategorySerializer, ProductSerializer, ReviewSerializer

@api_view(['GET', 'POST'])
def category_list_api_view(request):
    if request.method == 'GET':
        categories = Category.objects.annotate(product_count=Count('products'))
        data = CategorySerializer(categories, many=True).data
        return Response(data=data)
    elif request.method == 'POST':
        name = request.data.get('name')
        category = Category.objects.create(name=name)
        return Response(CategorySerializer(category).data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
def category_detail_api_view(request, id):
    try:
        category = Category.objects.get(id=id)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        data = CategorySerializer(category, many=False).data
        return Response(data=data)

    elif request.method == 'PUT':
        category.name = request.data.get('name')
        category.save()
        return Response(status=status.HTTP_201_CREATED,
                        data=CategorySerializer(category).data)  

    elif request.method == 'DELETE':
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def product_list_api_view(request):
    if request.method == 'GET':
        products = Product.objects.all().annotate(rating=Avg('reviews__stars'))
        data = ProductSerializer(products, many=True).data
        return Response(data=data)

    elif request.method == 'POST':
        title = request.data.get('title')
        price = request.data.get('price')
        description = request.data.get('description')      
        category_id = request.data.get('category_id')      

        product = Product.objects.create(                  
            title=title,
            price=price,
            description=description,
            category_id=category_id
        )

        return Response(                                   
            status=status.HTTP_201_CREATED,
            data=ProductSerializer(product).data
        )


@api_view(['GET', 'PUT', 'DELETE'])
def product_detail_api_view(request, id):
    try:
        product = Product.objects.prefetch_related('reviews').get(id=id)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        data = ProductSerializer(product, many=False).data
        return Response(data=data)

    elif request.method == 'PUT':
        product.title = request.data.get('title')
        product.price = request.data.get('price')
        product.description = request.data.get('description')
        product.category_id = request.data.get('category_id')  

        product.save()

        return Response(
            data=ProductSerializer(product).data
        )

    elif request.method == 'DELETE':
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



@api_view(['GET', 'POST'])
def review_list_api_view(request):
    if request.method == 'GET':
        reviews = Review.objects.all()
        data = ReviewSerializer(reviews, many=True).data
        return Response(data=data)
    elif request.method == 'POST':
        text = request.data.get('text')
        stars = request.data.get('stars')
        product_id = request.data.get('product_id')
        
        review = Review.objects.create(
            text=text,
            stars=stars,
            product_id=product_id
        )

        return Response(data=ReviewSerializer(review).data,
            status=status.HTTP_201_CREATED
        )



@api_view(['GET','PUT', 'DELETE'])
def review_detail_api_view(request, id):
    try:
        review = Review.objects.get(id=id)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        data = ReviewSerializer(review, many=False).data
        return Response(data=data)
    elif request.method == 'PUT':
        review.text = request.data.get('text')
        review.stars = request.data.get('stars')
        review.product_id = request.data.get('product_id')

        review.save()

        return Response(
            data=ReviewSerializer(review).data
        )

    elif request.method == 'DELETE':
        review.delete()
        return Response(data=ReviewSerializer(review).data,
            status=status.HTTP_201_CREATED)
    

@api_view(['GET'])
def product_reviews_api_view(request):
    products = Product.objects.all().prefetch_related('reviews').all()
    data = ProductSerializer(products, many=True).data
    return Response(data)