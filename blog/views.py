from rest_framework.response import Response
from rest_framework import permissions, viewsets
from rest_framework.views import APIView
from rest_framework import generics
from blog.models import BlogPost, Comment, Like
from blog.serializers import BlogPostSerializer, CommentSerializer, LikeSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404, redirect, render
from blog import serializers
from django.contrib.auth.models import User


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = [IsAuthenticated]


# class UserDetail(generics.RetrieveAPIView):
#     queryset = User.objects.all()
#     serializer_class = serializers.UserSerializer
#     permission_classes = [IsAuthenticated]


class BlogPostListView(generics.ListAPIView):
    queryset = BlogPost.objects.order_by('-date_created')
    serializer_class = BlogPostSerializer
    lookup_field = 'slug'
    permission_classes = [IsAuthenticated]


# class CommentListView(generics.ListCreateAPIView):
#     queryset = Comment.objects.all()
#     serializer_class = CommentSerializer
#     lookup_fields = 'slug'
#     permission_classes = (AllowAny,)

#     def perform_create(self, serializer):
#         serializer.save()


class BlogPostDetailView(generics.ListCreateAPIView):

    #queryset = BlogPost.objects.filter(slug="blog-2")
    serializer_class = BlogPostSerializer
    permission_classes = [IsAuthenticated]
    #lookup_field = 'slug'

    def get_queryset(self):
        queryset = BlogPost.objects.all()
        slug = self.kwargs["slug"]
        queryset = queryset.filter(slug=slug)
        return queryset

    def create(self, request, *args, **kwargs):
        #print('request:', request.__repr__())
        queryset = BlogPost.objects.all()
        slug = self.kwargs["slug"]
        queryset = queryset.filter(slug=slug)
        #print("yusuf:", queryset[0])
        serializer = CommentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user, post=queryset[0])
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
    permission_classes = [IsAuthenticated]


class BlogPostUpdateApi(generics.RetrieveUpdateAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    lookup_field = 'slug'
    permission_classes = [IsAuthenticated]


class BlogPostDeleteApi(generics.DestroyAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    lookup_field = 'slug'
    permission_classes = [IsAuthenticated]


# class LikeList(generics.ListCreateAPIView):
#     serializer_class = BlogPostSerializer
#     permission_classes = [IsAuthenticated]
    # def get_queryset(self):
    #     queryset = BlogPost.objects.all()
    #     slug = self.kwargs["slug"]
    #     queryset = queryset.filter(slug=slug)
    #     return queryset
    # def create(self, request, *args, **kwargs):
    #     #print('request:', request.__repr__())
    #     queryset = BlogPost.objects.all()
    #     slug = self.kwargs["slug"]
    #     queryset = queryset.filter(slug=slug)
    #     #print("yusuf:", queryset[0])
    #     serializer = LikeSerializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save(user=request.user, post=queryset[0])
    #     return Response(serializer.data)


class LikeList(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, slug):
        obj = get_object_or_404(BlogPost, slug=slug)
        like_qs = Like.objects.filter(user=request.user, post=obj)
        if like_qs.exists():
            like_qs[0].delete()
            data = {
                "messages": "unlike"
            }
        else:
            Like.objects.create(user=request.user, post=obj)
            data = {
                "messages": "like"
            }
        return Response(data)
