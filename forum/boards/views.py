from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Forum, Post, Profile
from django.db.models import Q
from .forms import CommentForm
from django.http import HttpResponseRedirect
from django.urls import reverse

def forum_list(request):
    query = request.GET.get('q', '')
    if query:
        forums = Forum.objects.filter(name__icontains=query)
    else:
        forums = Forum.objects.all()
    return render(request, 'boards/forum_list.html', {
        'forums': forums
    })

@login_required
def create_forum(request):
    if request.method == 'POST':
        name = request.POST['name']
        description = request.POST['description']
        Forum.objects.create(name=name, description=description)
        return redirect('forum_list')
    return render(request, 'boards/create_forum.html')

def forum_detail(request, forum_id):
    forum = get_object_or_404(Forum, id=forum_id)
    posts = forum.posts.all()
    return render(request, 'boards/forum_detail.html', {'forum': forum, 'posts': posts})

@login_required
def create_post(request, forum_id):
    forum = get_object_or_404(Forum, id=forum_id)
    if request.method == 'POST':
        title = request.POST['title']
        body = request.POST['body']
        Post.objects.create(forum=forum, author=request.user, title=title, body=body)
        return redirect('forum_detail', forum_id=forum.id)
    return render(request, 'boards/create_post.html', {'forum': forum})


def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    comments = post.comments.order_by('created_at')  # alle Kommentare zum Post

    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('/accounts/login')
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('post_detail', post_id=post_id)
    else:
        form = CommentForm()

    return render(request, 'boards/post_detail.html', {
        'post': post,
        'comments': comments,
        'form': form, })

def profile_view(request, username):
    user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=user).select_related('forum').order_by('-created_at')[:10]
    return render(request, 'boards/profile.html', {
        'profile_user': user,
        'posts': posts
    })

@login_required
def edit_profile(request):
    if request.method == 'POST':
        bio = request.POST['bio']
        avatar = request.FILES.get('avatar')
        profile = request.user.profile
        profile.bio = bio
        if avatar:
            if not avatar.content_type.startswith('image/'):
                return render(request, 'boards/edit_profile.html', {
                    'error': 'Bitte nur Bilddateien hochladen.'
                })
            profile.avatar = avatar
        profile.save()
        return redirect('profile_view', username=request.user.username)
    return render(request, 'boards/edit_profile.html')

@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return HttpResponseRedirect(reverse('post_detail', args=[post_id]))