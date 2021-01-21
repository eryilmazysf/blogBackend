from rest_framework.response import Response
from rest_framework import permissions, viewsets
from rest_framework.views import APIView
from rest_framework import generics
from blog.models import BlogPost, Comment
from blog.serializers import BlogPostSerializer, CommentSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404, redirect, render


class BlogPostListView(generics.ListAPIView):
    queryset = BlogPost.objects.order_by('-date_created')
    serializer_class = BlogPostSerializer
    lookup_field = 'slug'
    permission_classes = [IsAuthenticated]


class CommentListView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
    queryset = Comment.objects.all()
    lookup_fields = 'slug'


class BlogPostDetailView(generics.ListCreateAPIView):

    serializer_class = BlogPostSerializer
    queryset = BlogPost.objects.all().filter(slug='blog-5')
    lookup_field = 'slug'
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        print('request:', request.data['content'])
        serializer = CommentSerializer(data=request.data['content'])
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class BlogPostFeaturedView(generics.ListAPIView):
    queryset = BlogPost.objects.filter(featured=True)
    serializer_class = BlogPostSerializer
    lookup_field = 'slug'
    permission_classes = [IsAuthenticated]


class BlogPostCategoryView(APIView):
    serializer_class = BlogPostSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        data = self.request.data
        category = data['category']
        queryset = BlogPost.objects.order_by(
            '-date_created').filter(category__iexact=category)
        serializer = BlogPostSerializer(queryset, many=True)
        return Response(serializer.data)


class BlogPostCreateApi(generics.CreateAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    #permission_classes = (permissions.AllowAny,)


class BlogPostUpdateApi(generics.RetrieveUpdateAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    lookup_field = 'slug'


class BlogPostDeleteApi(generics.DestroyAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    lookup_field = 'slug'
