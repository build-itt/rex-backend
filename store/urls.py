from django.urls import path
from .views import *

urlpatterns = [
    path('categories/', CategoryList.as_view(), name='api_home'),
    path('category/<str:category_slug>/', CategoryListView.as_view(), name='api_category_list'),
    # ... other URL patterns
]
