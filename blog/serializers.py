from rest_framework import serializers
from .models import BlogPost, Comment, Like
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    post = serializers.StringRelatedField()

    class Meta:
        model = Comment
        fields = '__all__'


class BlogPostSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()
    comment = CommentSerializer(
        many=True, required=False,)

    class Meta:
        model = BlogPost
        fields = ('title', 'comment', 'author',
                  'comment_count', 'like_count', 'category')
        lookoup_field = 'slug'


class LikeSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    post = serializers.StringRelatedField()

    class Meta:
        model = Like
        fields = (
            "user",
            "post",
        )
