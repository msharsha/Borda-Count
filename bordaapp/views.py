from .models import Post
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import PostForm
from django.views.generic import (
    CreateView,
    ListView,
    DetailView,
    UpdateView,
    DeleteView
)
from django.utils import timezone


class PostListView(ListView):
    model = Post
    template_name = 'borda/index.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        try:
            keyword = self.request.GET['q']
        except:
            keyword = ''
        if (keyword != ''):
            object_list = self.model.objects.filter(
                Q(content__icontains=keyword) | Q(title__icontains=keyword))
        else:
            if self.request.user.is_anonymous:
                object_list = []
            else:
                object_list_with_deadline = self.model.objects.filter(allowed_users__contains=self.request.user.email, deadline__gt=timezone.now())
                object_list_no_deadline = self.model.objects.filter(allowed_users__contains=self.request.user.email, deadline=None)
                object_list = object_list_with_deadline | object_list_no_deadline
        
        return object_list


class UserPostListView(ListView):
    model = Post
    template_name = 'borda/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


def PostDetailView(request, pk):
    user = get_object_or_404(User, username=request.user)
    if request.method == "POST":
        print('post method')
        pass
    else:
        template_name = 'borda/post_detail.html' 
        post = Post.objects.get(id=pk)
        return render(request, template_name, {'post': post})


# class PostCreateView(LoginRequiredMixin, CreateView):
#     model = Post
#     form_class = PostForm
#     template_name = 'borda/post_form.html' 
#     def form_valid(self, form):
#         form.instance.author = self.request.user
#         return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']
    template_name = 'borda/post_detail.html' 
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'
    template_name = 'borda/post_confirm_delete.html' 
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def about(request):
    return render(request, 'borda/about.html', {'title': 'About'})
