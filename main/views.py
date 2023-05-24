from django.core.mail import send_mail
from rest_framework import generics, permissions
from rest_framework.throttling import UserRateThrottle

from assignment import settings
from .models import Post
from .permissions import IsOwnerOrReadOnly
from .serializers import PostSerializer


class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    def perform_create(self, serializer):
        post = serializer.save(author=self.request.user)
        subject = 'New Post Created successfully '
        user_content = f"""Dear {post.author.email}:,<br><br>

                                                  Congratulations! 'New Post Created',
                                                'A new post has been created.',
                                                  Thanks & regards<br>
                                                  Team """

        recipient_list = [post.author.email, ]
        sender = settings.DEFAULT_FROM_EMAIL
        send_mail(subject, user_content, sender, recipient_list, html_message=user_content)

    def get_queryset(self):
        queryset = super().get_queryset()

        title = self.request.query_params.get('title')
        body = self.request.query_params.get('body')
        author = self.request.query_params.get('author')

        if title:
            queryset = queryset.filter(title__icontains=title)
        if body:
            queryset = queryset.filter(body__icontains=body)
        if author:
            queryset = queryset.filter(author__username=author)

        return queryset


class PostRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
