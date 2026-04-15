from rest_framework import serializers
from .models import Category, Product, Review
from rest_framework.exceptions import ValidationError


class CategorySerializer(serializers.ModelSerializer):
    product_count = serializers.IntegerField(read_only=True)
    class Meta:
        model = Category
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many= True, read_only=True)
    rating = serializers.FloatField(read_only=True)
    class Meta:
        model = Product
        fields = '__all__'


class CategoryValidateSerializer(serializers.Serializer):
    name = serializers.CharField(min_length=2, max_length=255)

class ProductValidateSerializer(serializers.Serializer):
    title = serializers.CharField(min_length=2, max_length=255)
    description = serializers.CharField(required=False)
    price = serializers.FloatField(min_value=1)
    category_id = serializers.IntegerField()


    def validate_category_id(self, value):
        if not Category.objects.filter(id=value).exists():
            raise ValidationError('Category does not exist')
        return value
    

class ReviewValidateSerializer(serializers.Serializer):
    text = serializers.CharField(min_length=1)
    stars = serializers.IntegerField(min_value=1, max_value=5)
    product_id = serializers.IntegerField()


    def validate_product_id(self, value):
        if not Product.objects.filter(id=value).exists():
            raise ValidationError('Product does not exist')
        return value