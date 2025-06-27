from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Forum, Post

def forum_list(request):
    forums = Forum.objects.all()
    return render(request, 'boards/forum_list.html', {'forums': forums})

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
    post = get_object_or_404(Post, id=post_id)
    return render(request, 'boards/post_detail.html', {'post': post})
