from rest_framework import serializers
from .models import BlogPost, Comment


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class BlogPostSerializer(serializers.ModelSerializer):
    comment = CommentSerializer(required=False, many=True)

    class Meta:
        model = BlogPost
        fields = '__all__'
        lookoup_field = 'slug'
