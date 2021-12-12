from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from rest_framework import filters, mixins, viewsets, permissions

from .serializers import CommentSerializer, FollowSerializer, GroupSerializer, PostSerializer
from .permissions import IsAuthorOrReadOnlyPermission
from posts.models import Follow, Group, Post

CREATE_DENIED_MESSAGE = 'Необходима авторизация для создания поста'
DELETE = 'Удаление чужого контента запрещено'
UPDATE = 'Изменение чужого контента запрещено!'


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsAuthorOrReadOnlyPermission
    ]



    def perform_create(self, serializer):
    #    if not self.request.user.is_authenticated:
    #        raise PermissionDenied(CREATE_DENIED_MESSAGE)
        serializer.save(author=self.request.user)

#    def perform_update(self, serializer):
#        if serializer.instance.author != self.request.user:
#            raise PermissionDenied(UPDATE)
#        super().perform_update(serializer)

#   def perform_destroy(self, instance):
#        if instance.author != self.request.user:
#            raise PermissionDenied(DELETE)
#        instance.delete()


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsAuthorOrReadOnlyPermission
    ]

    def get_post(self):
        post_id = self.kwargs.get('post_id')
        post = get_object_or_404(Post, id=post_id)
        return post

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, post=self.get_post())

#    def perform_update(self, serializer):
#        if serializer.instance.author != self.request.user:
#            raise PermissionDenied(UPDATE)
#        super().perform_update(serializer)

#    def perform_destroy(self, instance):
#        if instance.author != self.request.user:
#            raise PermissionDenied(
#                DELETE)
#        instance.delete()

    def get_queryset(self):
        return self.get_post().comments


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CreateListViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                        viewsets.GenericViewSet):
    pass


class FollowViewSet(viewsets.CreateListViewSet):
    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=user__username', '=following__username',)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return self.request.user.user.all()

