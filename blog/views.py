from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseForbidden
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib.auth import login
from .models import Post, Image
from .forms import CreatePostForm, ImageFormSet, CommentForm, SearchForm, SignupForm, EditProfileForm
from taggit.models import Tag

def all_posts(request, tag_slug=None):
    tag = None
    posts = Post.publish.select_related('auther') \
        .prefetch_related('comments') \
        .annotate(comment_count=Count('comments', filter=Q(comments__active=True))) \
        .order_by('-created')

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        posts = posts.filter(tags__in=[tag])

    tags = Tag.objects.all().order_by('name')
    paginator_tags = Paginator(tags, 4)
    page_number_tags = request.GET.get('page_tag', 1)
    page_obj_tags = paginator_tags.get_page(page_number_tags)

    paginator_posts = Paginator(posts, 10)
    page_number_posts = request.GET.get('page', 1)
    page_obj_posts = paginator_posts.get_page(page_number_posts)

    context = {
        'posts': page_obj_posts,
        'page': page_obj_posts,
        'tag': tag,
        'tags': page_obj_tags,
        'posts_tag': page_obj_tags,
        'page_tag': page_obj_tags,
    }

    return render(request, 'blog/index.html', context)

def post_detail(request, id):
    post = get_object_or_404(Post, id=id)
    comments = post.comments.filter(active=True)
    form = CommentForm()
    user = request.user
    usercomment = post.comments.filter(name=user, active=False)
    tags = Tag.objects.all().order_by('name')

    text_parts = post.description.split("\n", 2)
    first_part = text_parts[0] if len(text_parts) > 0 else ""
    second_part = text_parts[1] if len(text_parts) > 1 else ""
    third_part = text_parts[2] if len(text_parts) > 2 else ""

    paginator_tags = Paginator(tags, 4)
    page_number_tags = request.GET.get('page_tag', 1)
    page_obj_tags = paginator_tags.get_page(page_number_tags)

    latest_posts = Post.publish.order_by('-created')[:3]

    context = {
        'post': post,
        'first_part': first_part,
        'second_part': second_part,
        'third_part': third_part,
        'form': form,
        'comments': comments,
        'tags': page_obj_tags,
        'latest_posts': latest_posts,
        'usercomment': usercomment,
    }

    return render(request, 'blog/post.html', context)

@login_required
@require_POST
def set_comment(request, id):
    post = get_object_or_404(Post, id=id)
    comment = None
    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.name = request.user.username
        comment.post = post
        comment.save()
        return redirect("blog:post", id=post.id)

    context = {
        'post': post,
        'form': form,
        'comment': comment
    }
    return render(request, "blog/post.html", context)

def search(request):
    query = ''
    result = []

    if 'query' in request.GET:
        form = SearchForm(data=request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            result = Post.publish.filter(Q(title__icontains=query) | Q(description__icontains=query))

    paginator_posts = Paginator(result, 1)
    page_number_posts = request.GET.get('page', 1)
    page_obj_posts = paginator_posts.get_page(page_number_posts)

    context = {
        'posts': page_obj_posts,
        'page': page_obj_posts,
        'query': query
    }
    return render(request, "blog/search.html", context)

@login_required
def create_post(request):
    if request.method == 'POST':
        post_form = CreatePostForm(request.POST)
        image_formset = ImageFormSet(request.POST, request.FILES, prefix='images')

        if post_form.is_valid() and image_formset.is_valid():
            post = post_form.save(commit=False)
            post.auther = request.user
            post.save()
            
            tags = post_form.cleaned_data['tags']
            post.tags.add(*tags)

            images = image_formset.save(commit=False)
            for image in images:
                image.post = post
                image.save()
            return redirect('blog:all_posts')
    else:
        post_form = CreatePostForm()
        image_formset = ImageFormSet(prefix='images')

    return render(request, 'forms/create_post.html', {
        'form': post_form,
        'image_formset': image_formset,
    })

@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, auther=request.user)

    if request.method == 'POST':
        form = CreatePostForm(request.POST, instance=post)
        image_formset = ImageFormSet(request.POST, request.FILES, instance=post)

        if form.is_valid() and image_formset.is_valid():
            post = form.save()
            instances = image_formset.save(commit=False)
            for instance in instances:
                instance.post = post
                instance.save()
            for obj in image_formset.deleted_objects:
                obj.delete()
            return redirect('blog:profile')
    else:
        form = CreatePostForm(instance=post)
        image_formset = ImageFormSet(instance=post)

    return render(request, "forms/edit_post.html", {
        'form': form,
        'image_formset': image_formset,
        'post': post,
    })

@login_required
def delete_post(request, id):
    post = get_object_or_404(Post, id=id, auther=request.user)
    if post.auther != request.user:
        return HttpResponseForbidden("You can not delete this post.")
    post.delete()
    return redirect("blog:profile")

@login_required
def profile(request):
    user = request.user
    posts = Post.objects.filter(auther=user)
    context = {
        'posts': posts,
    }
    return render(request, "user/profile.html", context)

def edit_profile(request):
    if request.method == "POST":
        form = EditProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('blog:profile')
    else:
        form = EditProfileForm(instance=request.user)
    return render(request, 'registration/edituser.html', {'form': form})

def sign_up(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            return redirect('blog:profile')
    else:
        form = SignupForm()
    return render(request, 'registration/signup.html', {'form': form})

@login_required
def activat_post(request, id):
    post = get_object_or_404(Post, id=id, auther=request.user)
    post.active = 0 if post.active == 1 else 1
    post.save()
    return redirect("blog:profile")

def resume_view(request):
    return render(request, 'blog/contact.html')

# @login_required
# def profile(request,username):
#     user = get_object_or_404(User , username=username)
#     posts = Post.objects.filter(auther=user.id)
#     return render(request, "user/profile.html", {"user":user,"posts":posts})
