from django.urls import path
from .views import BlogPostCreateApi, BlogPostUpdateApi, BlogPostDeleteApi, BlogPostListView, BlogPostDetailView, BlogPostFeaturedView, BlogPostCategoryView
urlpatterns = [
    path('', BlogPostListView.as_view()),
    path('featured', BlogPostFeaturedView.as_view()),
    path('category', BlogPostCategoryView.as_view()),
    path('<str:slug>', BlogPostDetailView.as_view()),
    path('create/', BlogPostCreateApi.as_view()),
    path('<str:slug>/update', BlogPostUpdateApi.as_view()),
    path('<str:slug>/delete', BlogPostDeleteApi.as_view()),
]
