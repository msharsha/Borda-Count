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


def PostDetailView(request, pk):
    if request.user.is_anonymous:
        return redirect('/')

    template_name = 'borda/post_detail.html'
    if request.method == "POST":
        form = PostSubmitForm(request.POST)
        if form.is_valid():
            
            post = Post.objects.get(id=pk)
            answered_users = post.answered_users
            answered_users += ','+request.user.email
            post.answered_users = answered_users
            post.save()

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
        form.fields['preferences'].widget = forms.HiddenInput() 
        return render(request, template_name, {'post': post, 'form': form})

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

class ResultListView(ListView):
    model = Post
    template_name = 'borda/result_list.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        if self.request.user.is_anonymous or not self.request.user.is_superuser:
            return []
        post_list = self.model.objects.all()
        return post_list

def ResultDetailView(request, pk):
    if request.user.is_anonymous or not request.user.is_superuser:
        return redirect('/')
    post = Post.objects.get(id=pk)
    if post.answered_users=="_":
        template_name = 'borda/no_result.html'
        return render(request, template_name,{'post': post})
    template_name = 'borda/result_detail.html'
    aggr = Aggregator(pk)
    scores, winners = aggr.borda()
    total_score = sum(scores.values())
    percents = {}
    for candidate,score in scores.items():
        percents[candidate] = round((score/total_score)*100)
    num_users_answered = len(post.answered_users.split(',')) - 1
    total_users = len(post.allowed_users.split(','))
    return render(request, template_name, {'post': post, 'scores': scores.items(), 'winner': winners[0], 'total_score': total_score, 'percents': percents.items(), 'num_users_answered': num_users_answered, 'total_users': total_users })

class PreferenceSchedule():

    def __init__(self, candidates, prefs):
        self.candidates = candidates
        self.prefs = prefs
        self.detailed_prefs = self.getDetiledPrefs()

    def getDetiledPrefs(self):
        detailed_prefs = []
        for pref in self.prefs:
            sorted_pref = [k for k, v in sorted(pref.items(), key=lambda item: -item[1])]
            detailed_prefs.append(sorted_pref)
        return detailed_prefs

    def original(self):
        '''Returns the original preference schedule as a printable string'''

        res = ''
        for i in range(len(self.detailed_prefs)):
            res += 'Voter {}: '.format(i+1) + ', '.join(self.detailed_prefs[i]) + '\n'

        return res[:-1]

    def detailed(self):
        '''Returns the detailed preference schedule as a printable string'''
        # count the number of occurences of each preference
        prefs = self.detailed_prefs[:]
        prefs = [tuple(p) for p in self.detailed_prefs]
        counts = {}
        while prefs:
            pref = prefs.pop(0)
            count = 1
            while pref in prefs:
                prefs.remove(pref)
                count += 1
            counts[pref] = count

        res = ''
        for pref in counts:
            res += str(counts[pref]) + ' Voters: ' + ', '.join(pref) + '\n'

        return res[:-1]


class Aggregator():

    def __init__(self, pk):
        candidates, prefs = get_preference_schedule(pk)
        self.pref_schedule = PreferenceSchedule(candidates, prefs)

    def __str__(self):
        res = ''
        res += 'Preference Schedule:\n'
        res += self.pref_schedule.original() + '\n\n'
        res += 'Detailed Preference Schedule:\n'
        res += self.pref_schedule.detailed() + '\n'

        return res

    def borda(self):
        '''Finds who wins by the Cumulative Borda count'''
        scores = {}
        candidates = list(self.pref_schedule.candidates)
        for candidate in candidates:
            scores[candidate] = 0

        for pref in self.pref_schedule.prefs:
            for (key,value) in pref.items():
                scores[key] += value
        winner = self.find_winner(scores)
        return scores, winner

    def find_winner(self, aggregated_result):
        max_point = 0
        winners = [] # winner can be many, so use a list here
        for (candidate,point) in aggregated_result.items():
            if point > max_point:
                max_point = point
                winners.clear()
                winners.append(candidate)
            elif point == max_point:
                winners.append(candidate)
        return winners

def get_preference_schedule(pk):
    '''Reads objects and returns candidates and preferences'''
    post = Post.objects.get(id = pk)
    submissions = Submission.objects.filter(post_id = pk)
    
    candidates = list(post.options.split(','))
    prefs = []
    for submission in submissions:
        pref = submission.preferenceMap()
        prefs.append(pref)
    return candidates, prefs
