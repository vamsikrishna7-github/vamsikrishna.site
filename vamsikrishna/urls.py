from django.contrib import admin
from django.urls import path, re_path, include
from home import views
from blog.views import add_subscriber, view_count, unsubscribe
from blog.views import delete_subscriber, create_blog_post, blog_post_list, del_blog_post, edit_blog_post, get_blog_posts_full, get_blog_post_full_by_slug, get_blogs_search, like_blog
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve  # Import serve for media files
from utils import health_check
from home.views import homepage, privacy_policy, terms_of_service


urlpatterns = [
    path('healthz/', health_check), #sleep time fix for render.com

    path('', homepage, name='home'),
    path('admin/', views.admin_login, name='admin'),
    path("admin-panel/", views.admin_panel, name="admin_panel"),
    path('delete-message/<int:msg_id>/', views.delete_message, name='delete_message'),
    path("logout/", views.admin_logout, name="logout"),


    #templates
    path("templates/", views.templates, name="templates"),
    path('buy-templates/', views.buy_template_view, name='buy_templates'),
    path('payment-success/', views.payment_success, name='payment_success'),
    path('payment-failed/', views.payment_failed, name='payment_failed'),

    path('create_product/', views.create_product, name='create_product'), #create product
    path('edit_product/<int:id>/', views.edit_product, name='edit_product'), #edit product
    path('delete_product/<int:id>/', views.delete_product, name='delete_product'), # delete product

    # #blog_urls
    # path('blog/', bloghome, name='blog'),
    # path('unsubscribe/', blog_unsubscribe, name='unsubscribe'),
    # path('blog/<slug:slug>/', blog_post, name='blog_post'),
   
    #blog admin urls
    path('delete_subscriber/<str:subscriber_email>/', delete_subscriber, name="delete_subscriber"),

    #Full blog post Admin Only 
    path('create_blog_post/', create_blog_post, name='create_blog_post'), #create blog post
    path('blog_post_list/', blog_post_list, name='blog_post_list'), #Read blog posts
    path('del_blog_post/<int:id>/', del_blog_post, name='del_blog_post'), #Delete blog post
    path('edit_blog_post/<int:id>/', edit_blog_post, name='edit_blog_post'), #Update blog post

    #Api for vamsi's blog
    path('api/get_blog_posts_full/', get_blog_posts_full, name='get_blog_posts_full'), #Read all blog posts
    path('api/get_blog_post_full_by_slug/<slug:slug>/', get_blog_post_full_by_slug, name='get_blog_post_full_by_id'), #Read 1 blog posts
    path('api/get_blogs_search/', get_blogs_search, name='get_blogs_search'), #Search all blog posts
    path('api/like_blog/<slug:slug>/', like_blog, name='like_blog'), #Like blog
    path('api/view-count/', view_count, name='view-count'),
    path("api/unsubscribe/", unsubscribe, name="unsubscribe"),
    path('api/subscribe/', add_subscriber, name='subscribe'),

    path('privacy-policy/', privacy_policy, name='privacy_policy'),
    path('terms-of-service/', terms_of_service, name='terms_of_service'),
    path('sellWork/', include('home.urls')),
]

# # Serve media files manually in production
# if not settings.DEBUG:
#     urlpatterns += [
#         re_path(r"^media/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT}),
#     ]

urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]

# Only serve static files this way in development
if settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    urlpatterns += staticfiles_urlpatterns()
