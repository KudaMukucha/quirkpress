from django.shortcuts import get_object_or_404, redirect, render
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from .models import Post,Category
from .forms import CommentForm,CreatePostForm,UpdatePostForm
from taggit.models import Tag

def home(request):
    posts = Post.objects.filter(status='PB')
    featured_posts = Post.objects.filter(status='PB',featured='Yes').order_by('?')[:1]
    random_posts = Post.objects.filter(status='PB').order_by('?')[:4]
    return render(request,'home.html',{'posts':posts,'featured_posts':featured_posts,'random_posts':random_posts})

def post_list(request,tag_slug=None):
    post_list = Post.objects.filter(status='PB')
    featured_posts = Post.objects.filter(status='PB',featured='Yes').order_by('?')[:2]
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        post_list = post_list.filter(tags__in=[tag])
    paginator = Paginator(post_list,4)
    page_number = request.GET.get('page',1)
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request,'blog/list.html',{'posts':posts,'featured_posts':featured_posts})

def post_detail(request,year,month,day,post):
    post = Post.objects.get(publish__year=year,publish__month =month,publish__day =day,slug=post,status ='PB')
    comments = post.comments.filter(active=True)
    featured_posts = Post.objects.filter(status='PB',featured='Yes').order_by('?')[:2]
    form = CommentForm()
    similar_posts = Post.objects.filter(category=post.category).exclude(pk=post.pk).filter(status='PB')[:2]
    return render(request,'blog/post.html',{'post':post,'comments':comments,'form':form,'similar_posts':similar_posts,'featured_posts':featured_posts})


def posts_per_category(request,category_name):
    category = Category.objects.get(name__iexact = category_name)
    featured_posts = Post.objects.filter(status='PB',featured='Yes').order_by('?')[:1]
    post_list = Post.objects.filter(category=category,status='PB')
    paginator = Paginator(post_list,2)
    page_number = request.GET.get('page',1)
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request,'blog/category-posts.html',{'posts':posts,'featured_posts':featured_posts,'category':category})

def post_comment(request,post_pk):
    post = Post.objects.get(pk = post_pk,status='PB')
    comment = None
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return render(request,'blog/comment.html',{'form':form,'comment':comment,'post':post})
    

def create_post(request):
    post = None
    if request.method == 'POST':
        form = CreatePostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('blog:home')
    else:
        form = CreatePostForm()
        return render(request,'blog/create-post.html',{'form':form})
    
def update_post(request,pk):
    post = Post.objects.get(pk=pk)
    if request.method == 'POST':
        form = UpdatePostForm(request.POST,instance=post)
        if form.is_valid():
            form.save()
            return redirect('blog:home')
    else:
        form = UpdatePostForm(instance=post)
        return render(request,'blog/update-post.html',{'form':form})
    

def privacy_policy(request):
    featured_posts = Post.objects.filter(status='PB',featured='Yes').order_by('?')[:4]
    return render(request,'privacy.html',{'featured_posts':featured_posts})

def about_us(request):
    return render(request,'about.html')

def terms(request):
    featured_posts = Post.objects.filter(status='PB',featured='Yes').order_by('?')[:4]
    return render(request,'terms.html',{'featured_posts':featured_posts})
