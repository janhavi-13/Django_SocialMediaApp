from typing import Any
from django.contrib.auth.models import User
from django.views.generic import DetailView, View
from feed.models import Post
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponseBadRequest
from followers.models import Follower
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
# Create your views here.
class ProfileDetailView(DetailView):
    http_method_names = ['get']
    template_name = 'profiles/detail.html'
    model = User
    context_object_name = 'user'
    slug_field = 'username'
    slug_url_kwarg = 'username'

    def dispatch(self, request, *args, **kwrags):
        self.request = request
        return super().dispatch(request, *args, **kwrags)

    def get_context_data(self, **kwargs):
        user = self.get_object()
        context = super().get_context_data(**kwargs)
        context['total_post'] = Post.objects.filter(author=user).count()
        if self.request.user.is_authenticated:
            context['you_follow'] = Follower.objects.filter(following = user, followed_by = self.request.user)
        context['total_following'] = Follower.objects.filter(followed_by = user).count()
        context['total_followers'] = Follower.objects.filter(following = user).count()         
        return context
        
    
class FollowView(LoginRequiredMixin, View):
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()

        if 'action' not in data or 'username' not in data:
            return HttpResponseBadRequest('Missing data')
        
        try:
            other_user = User.objects.get(username=data['username'])
        except User.DoesNotExist:
             return HttpResponseBadRequest('Missing user')
        
        if data['action'] == 'follow':
            follower, created = Follower.objects.get_or_create(
                followed_by = request.user,
                following = other_user,
            )
        else:
            try:
                follower = Follower.objects.get(
                    followed_by = request.user,
                    following = other_user,
                )
            except Follower.DoesNotExist:
                follower = None

            if follower:
                follower.delete()
        total_followers = Follower.objects.filter(following = other_user).count()
        total_following = Follower.objects.filter(followed_by = other_user).count()
        return JsonResponse({
            'success' : True,
            'wording' : 'Unfollow' if data['action'] == 'follow' else 'Follow',
            'total_followers': total_followers,
            'total_following': total_following,
        })
    
    
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'profiles/change_password.html', {
        'form': form
    })
