from django.shortcuts import render, redirect, get_object_or_404
from .models import NewsletterSubscriber, BlogPosts
from .forms import NewsletterForm, BlogPostsForm
from django.contrib.auth.decorators import login_required
from rest_framework import status
import json
from .serializers import NewsletterSubscriberSerializer, VisitorCountSerializer, BlogPostsSerializer
from home.models import VisitorCount
from utils import increment_visitor_count, auto_email_subscribe, send_unsubscribe_email, auto_email_new_BlogPost
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from threading import Thread
from rest_framework.response import Response
from rest_framework.decorators import api_view


# #blog proxy views
# def bloghome(request):
#     return render(request, 'blog/blog_home_proxy.html')

# def blog_unsubscribe(request):
#     return render(request, 'blog/blog_unsubscribe_proxy.html')

# def blog_post(request, slug):
#     return render(request, 'blog/blog_post_proxy.html', {'slug': slug})

#admin views from blog CRUD methods
@login_required(login_url='/admin/')
def delete_subscriber(request, subscriber_email):
    user = get_object_or_404(NewsletterSubscriber, email=subscriber_email)
    user.delete()
    return redirect('admin_panel')

#api views for next.js frontend 
@api_view(['POST'])
def add_subscriber(request):
    if request.method == 'POST':
        email = request.data.get('email')
        name = request.data.get('name')
        
        if NewsletterSubscriber.objects.filter(email=email).exists():
            return Response(
                {"message": "You are already subscribed"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
            
        serializer = NewsletterSubscriberSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            email_thread = Thread(
                target=auto_email_subscribe,
                args=(email, name)
            )
            email_thread.start()
            return Response(
                {"message": "Subscription successful!"}, 
                status=status.HTTP_201_CREATED
            )
            
        return Response(
            {"message": "Invalid data", "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )
    
@api_view(['GET'])
def view_count(request):
    views = VisitorCount.objects.get(id=1)  
    serializer = VisitorCountSerializer(views) 
    return Response(serializer.data)

@api_view(["POST"])
def unsubscribe(request):
    email = request.data.get("email")
    
    if not email:
        return Response({"error": "Email is required"}, status=400)
    
    try:
        subscriber = NewsletterSubscriber.objects.get(email=email)
        unsubscribe_thread = Thread(
            target=send_unsubscribe_email,
            args=(email,)
        )
        unsubscribe_thread.start()
        subscriber.delete()
        return Response({"message": "Unsubscribed successfully"}, status=200)
    except ObjectDoesNotExist:
        return Response({"error": "Email not found"}, status=404)
    
#creating full blog posts
#Create
@login_required(login_url='/admin/')
def create_blog_post(request):
    if request.method == 'POST':
        form = BlogPostsForm(request.POST, request.FILES)
        if form.is_valid():
            blog_post = form.save()
            email_thread = Thread(
                target=auto_email_new_BlogPost,
                args=(blog_post,)
            )
            email_thread.start()
            return redirect('blog_post_list')
    else:
        form = BlogPostsForm()
    return render(request, 'admin/admin_panel_Blog.html', {'form': form})

#Read
@login_required(login_url='/admin/')
def blog_post_list(request):
    posts = BlogPosts.objects.all().order_by('-posted_at')
    for post in posts:
        if post.main_image:
            file_extension = post.main_image.url.split('.')[-1].lower()
            post.is_video = file_extension in ["mp4", "webm", "ogg"]
        else:
            post.is_video = False
    return render(request, 'admin/admin_panel_Blog_All.html', {'posts': posts})

#Delete
@login_required(login_url='/admin/')
def del_blog_post(request, id):
     post = get_object_or_404(BlogPosts, id=id)
     post.delete()
     return redirect('blog_post_list')

#Update
@login_required(login_url='/admin/')
def edit_blog_post(request, id):
    post = get_object_or_404(BlogPosts, id=id)
    if request.method == 'POST':
        form = BlogPostsForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('blog_post_list')
    else:
        form = BlogPostsForm(instance=post)
    return render(request, 'admin/admin_panel_Blog_edit.html', {'form': form})

#api views Full blog posts
@api_view(['GET'])
def get_blog_posts_full(request):
    views = increment_visitor_count()
    posts = BlogPosts.objects.all().order_by('-posted_at')
    serializer = BlogPostsSerializer(posts, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_blog_post_full_by_slug(request, slug):
    try:
        post = BlogPosts.objects.get(slug=slug)
        post.views += 1
        post.save()
        serializer = BlogPostsSerializer(post)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except BlogPosts.DoesNotExist:
        return Response({"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)
    
@api_view(['GET'])
def get_blogs_search(request):
    query = request.GET.get('search', '')
    if query:
        posts = BlogPosts.objects.filter(Q(title__icontains=query) | Q(subtitle__icontains=query) | Q(content__icontains=query))
    else:
        posts = BlogPosts.objects.all()
    serializer = BlogPostsSerializer(posts, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def like_blog(request, slug):
    try:
        post = BlogPosts.objects.get(slug=slug)
        post.likes += 1
        post.save()
        return Response(status=status.HTTP_200_OK)
    except BlogPosts.DoesNotExist:
        return Response({"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)
