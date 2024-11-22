from rest_framework import serializers
from .models import Product,Category,Comment

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
        
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id','name','slug','location')

class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        attatchment = serializers.FileField(required=False)
        model = Comment
        fields = ( 'id','body', 'created_by','attachment')

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
