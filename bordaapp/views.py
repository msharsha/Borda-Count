from django.http.response import HttpResponse
from .models import Post, Submission
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import PostSubmitForm
from django.views.generic import (
    CreateView,
    ListView,
    DetailView,
    UpdateView,
    DeleteView
)
from django.utils import timezone
from django import forms

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
    if request.user.is_anonymous:
        return redirect('/')
    if request.method == "POST":
        form = PostSubmitForm(request.POST)
        if form.is_valid():
            # Registering the User
            post = Post.objects.get(id=pk)
            answered_users = post.answered_users
            answered_users += ','+request.user.email
            post.answered_users = answered_users
            post.save()
            
            # Saving the Submission
            submission = form.save(commit=False)
            submission.post_id = Post.objects.get(id=pk)
            submission.submitted_by = request.user
            submission.submitted_date = timezone.now()
            submission.save()
            return redirect('/')
        else:
            return redirect('/')
    else:
        post = Post.objects.get(id=pk)
        if request.user.email in post.answered_users:
            return redirect('/')
        form = PostSubmitForm(initial={'options': post.options})
        form.fields['options'].widget = forms.HiddenInput()
        template_name = 'borda/post_detail.html' 
        
        return render(request, template_name, {'post': post, 'form': form})


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

def get_preference_schedule(pk):
    '''Reads objects and returns candidates and preferences'''
    post = Post.objects.get(id = pk)
    submissions = Submission.objects.filter(post_id = pk)
    
    candidates = list(post.options.split(','))
    prefs = []
    for submission in submissions:
        prefs.append(list(submission.options.split(',')))
    return candidates, prefs