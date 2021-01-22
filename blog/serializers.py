from rest_framework import serializers
from .models import BlogPost, Comment
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class BlogPostSerializer(serializers.ModelSerializer):
    comment = CommentSerializer(many=True, required=False, )

    class Meta:
        model = BlogPost
        fields = '__all__'
        lookoup_field = 'slug'
