from django.urls import path
from .views import BlogPostCreateApi, BlogPostUpdateApi, BlogPostDeleteApi, BlogPostListView, BlogPostDetailView, BlogPostFeaturedView, BlogPostCategoryView, UserList, UserDetail
urlpatterns = [
    path('', BlogPostListView.as_view()),
    path('featured/', BlogPostFeaturedView.as_view()),
    path('category/', BlogPostCategoryView.as_view()),
    path('<str:slug>/', BlogPostDetailView.as_view()),
    path('users', UserList.as_view()),
    path('users/<int:pk>/', UserDetail.as_view()),
    #path('<str:slug>/comment', CommentListView.as_view()),
    path('create/', BlogPostCreateApi.as_view()),
    path('<str:slug>/update/', BlogPostUpdateApi.as_view()),
    path('<str:slug>/delete/', BlogPostDeleteApi.as_view()),
]
