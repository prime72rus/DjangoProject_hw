from django.urls import path
from blog.apps import BlogConfig
from blog.views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView

app_name = BlogConfig.name

urlpatterns = [
    path("posts_list/", PostListView.as_view(), name="posts_list"),
    path("post_detail/<int:pk>/", PostDetailView.as_view(), name="post_detail"),
    path("post_create/", PostCreateView.as_view(), name="post_create"),
    path("post_update/<int:pk>/", PostUpdateView.as_view(), name="post_update"),
    path("post_delete/<int:pk>/", PostDeleteView.as_view(), name="post_delete"),
]
