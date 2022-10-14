from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from .forms import PostForm, PostDeleteForm
from django.contrib.auth.decorators import permission_required
from taggit.models import Tag
from django.core.paginator import Paginator


'''
def all_tags(request):
    common_tags = Post.tags.most_common()
    context = {'common_tags': common_tags, }
    return render(request, 'base.html', context)
'''


def home(request, tag=None):
    posts = Post.objects.all().order_by('-updated')
    paginator = Paginator(posts, 5)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    context = {'section': 'blog_home',
               'posts': posts,
               #    'tag_obj': tag_obj,
               }
    return render(request, 'blog/home.html', context)


def per_tag(request, tag=None):
    tag_obj = get_object_or_404(Tag, slug=tag)
    posts = Post.objects.filter(tags__in=[tag_obj])
    paginator = Paginator(posts, 5)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    context = {'section': 'blog_per_tag',
               'posts': posts,
               'tag_obj': tag_obj,
               }
    return render(request, 'blog/per_tag.html', context)


def detail(request, slug=None):
    post = get_object_or_404(Post, slug=slug)
    context = {'section': 'blog_detail',
               'post': post,
               }
    return render(request, 'blog/detail.html', context)


@permission_required('blog.add_post', raise_exception=True)
def create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            # using the app_name and name of url path i.e '<app_name>:<path_name>'
            return redirect('blog:home')
    else:
        form = PostForm()
    context = {'section': 'blog_create',
               'form': form,
               }
    return render(request, 'blog/create.html', context)


@permission_required('blog.change_post', raise_exception=True)
def edit(request, pk=None):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('blog:detail', slug=post.slug)
    else:
        form = PostForm(instance=post)

    context = {'section': 'blog_edit',
               'form': form,
               'post': post,
               }
    return render(request, 'blog/edit.html', context)


@permission_required('blog.delete_post', raise_exception=True)
def delete(request, pk=None):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = PostDeleteForm(request.POST, instance=post)
        if form.is_valid():
            post.delete()
            return redirect('blog:home')
    else:
        form = PostDeleteForm(instance=post)

    context = {'section': 'blog_delete',
               'form': form,
               'post': post,
               }
    return render(request, 'blog/delete.html', context)
