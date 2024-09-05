from django.urls import path
from .views import *

urlpatterns = [
    path('categories/', CategoryList.as_view(), name='api_home'),
    path('category/<str:category_slug>/', CategoryListView.as_view(), name='api_category_list'),
    # ... other URL patterns
    path('create-comment/', CommentCreateView.as_view(), name='api_create_comment'),
    path('comments/', CommentListView.as_view(), name='api_comment_list'),
    path('delete-comment/<int:pk>/', DeleteComment.as_view(), name='api_delete_comment'),
    path('user-comments/', UserCommentsListView.as_view(), name='api_user_comments'),
]
