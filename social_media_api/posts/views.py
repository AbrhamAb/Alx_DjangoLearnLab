from django.contrib.contenttypes.models import ContentType
from rest_framework import permissions, viewsets, filters, generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from notifications.models import Notification
from notifications.utils import create_notification

from .models import Comment, Like, Post
from .serializers import CommentSerializer, PostSerializer


class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return getattr(obj, 'author_id', None) == request.user.id


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'content']
    ordering_fields = ['created_at', 'updated_at', 'title']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class LikePostView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        post = generics.get_object_or_404(Post, pk=pk)
        like, created = Like.objects.get_or_create(user=request.user, post=post)
        if created and post.author != request.user:
            Notification.objects.create(
                recipient=post.author,
                actor=request.user,
                verb='liked your post',
                content_type=ContentType.objects.get_for_model(Post),
                object_id=post.pk,
            )
        status_code = status.HTTP_201_CREATED if created else status.HTTP_200_OK
        return Response({'detail': 'Liked'}, status=status_code)


class UnlikePostView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        post = generics.get_object_or_404(Post, pk=pk)
        like = Like.objects.filter(post=post, user=request.user).first()
        if like:
            like.delete()
        return Response({'detail': 'Unliked'}, status=status.HTTP_200_OK)


class FeedView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        following_users = user.following.all()
        return Post.objects.filter(author__in=following_users).order_by('-created_at').select_related('author')


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().select_related('post', 'author')
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrReadOnly]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at', 'updated_at']

    def get_queryset(self):
        queryset = super().get_queryset()
        post_id = self.request.query_params.get('post')
        if post_id:
            queryset = queryset.filter(post_id=post_id)
        return queryset

    def perform_create(self, serializer):
        comment = serializer.save(author=self.request.user)
        post = comment.post
        if post.author != self.request.user:
            create_notification(recipient=post.author, actor=self.request.user,
                                verb='commented on your post', target=post)
