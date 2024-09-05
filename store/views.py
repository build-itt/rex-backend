from .serializers import *
from .models import *
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication

class CategoryList(generics.ListCreateAPIView):
    queryset = Category.objects.all().exclude(name__in=["Extraction", "Dumps"])
    serializer_class = CategorySerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

class CategoryListView(generics.ListAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

    def get_queryset(self):
        category_slug = self.kwargs['category_slug']
        category = Category.objects.get(slug=category_slug)
        products = Product.objects.filter(category=category, Status=True)
        return products
    
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = ProductSerializer(queryset, many=True)
        if queryset:
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

class CommentCreateView(generics.CreateAPIView):
    serializer_class = CommentCreateSerializer
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def perform_create(self, serializer):
        username = self.request.user.username
        serializer.save(created_by=self.request.user,name=username)

class CommentListView(generics.ListAPIView):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()

    def get_queryset(self):
        comments = Comment.objects.filter(active=True).order_by('-created')
        return comments


    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = CommentSerializer(queryset, many=True)
        if queryset:
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

class UserCommentsListView(generics.ListAPIView):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get_queryset(self):
        comments = Comment.objects.filter(created_by=self.request.user)
        return comments

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = CommentSerializer(queryset, many=True)
        if queryset:
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

class DeleteComment(generics.DestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    def delete(self, request, *args, **kwargs):
        comment = Comment.objects.get(pk=kwargs['pk'])
        if request.user == comment.created_by:
            comment.active = False
            comment.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)