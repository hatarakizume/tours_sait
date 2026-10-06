from rest_framework import serializers
from django.utils.text import slugify
from .models import Category, Product

class CategorySerializer(serializers.ModelSerializer):
    post_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id','name','slug','post_count','created_at']
        read_only_fields = ['slug','created_at']

    def get_post_count(self, obj):
        return obj.posts.filter(status='published').count()

    def create(self, validated_data):
        validated_data['slug'] = slugify(validated_data['name'])
        return super().create(validated_data)

class ProductListSerializer(serializers.ModelSerializer):

    class Mata:
        model = Product
        fields = [
                    'id','title','slug','content','main_image','category',
                    'author','status','created_at','updated_at',
                    'price','total_places','available_places']
        read_only_fields = ['slug','author']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if len(data['content']) > 200:
            data['content'] = data['content'][:200] + '...'
        return data


class ProductDatailSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()
    category = serializers.StringRelatedField()

    class Meta:
        model = Product
        fields = [
            'id','title','slug','content','main_image','category',
            'category_info','author','author_info','status',
            'created_at','updated_at','price','total_places','available_places']

    def get_author_info(self, obj):
        author = obj.author
        return{
            'id': author.id,
            'username': author.username,
            'full_name': author.full_name,
            'avatar': author.avatar.url if author.avatar else None
        }

    def get_category_info(self, obj):
        if obj.category:
            return {
                'id': obj.category.id,
                'name': obj.category.name,
                'slug': obj.category.slug
            }
        return None

class ProductCreateUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        field = [
            'title','content','main_image','category','status',
            'price','total_places','available_places'
            ]

    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        validated_data['slug'] = slugify(validated_data['title'])
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if 'title' in validated_data:
            validated_data['slug'] = slugify(validated_data['title'])
        return super().update(instance, validated_data)