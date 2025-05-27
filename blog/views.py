from django.shortcuts import render, reverse
from blog.models import Post
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.core.paginator import Paginator


class PostListView(ListView):
    model = Post
    template_name = "blog/posts_list.html"
    paginate_by = 3

    def get_queryset(self):
        return Post.objects.filter(is_public=True)



class PostDetailView(DetailView):
    model = Post
    template_name = "blog/post_detail.html"
    context_object_name = "post"

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.view_counter += 1
        obj.save()
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['referer'] = self.request.META.get(
            'HTTP_REFERER',
            reverse("blog:posts_list")
        )
        return context


class PostCreateView(CreateView):
    model = Post
    fields = ['title', 'content', 'preview', 'is_public', 'view_counter']
    template_name = 'blog/post_form_create.html'
    success_url = reverse_lazy('blog:posts_list')


class PostUpdateView(UpdateView):
    model = Post
    fields = ['title', 'content', 'preview', 'is_public', 'view_counter']
    template_name = 'blog/post_form_update.html'

    def get_success_url(self):
        return reverse('blog:post_detail', kwargs={'pk': self.object.pk})


class PostDeleteView(DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('blog:posts_list')
