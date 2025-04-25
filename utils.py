from django.apps import apps
from django.template.loader import render_to_string
from django.core.mail import send_mail
from blog.models import NewsletterSubscriber
import datetime
from django.http import JsonResponse
from django.db import connection

#blog and portfolio visitor count
def increment_visitor_count():
    try:
        VisitorCount = apps.get_model('home', 'VisitorCount')
        visitor, created = VisitorCount.objects.get_or_create(id=1)
        visitor.views += 1
        visitor.save()
        return visitor.views 
    except Exception as e:
        print(f"Error incrementing visitor count: {e}")
        return 0

#auto blog subscribe email
def auto_email_subscribe(email, name):
    html_content = render_to_string(
        "blog/auto_email_subscribe.html",
        {"name": name}
    )
    
    send_mail(
        subject="Thanks for subscribing!",
        message=f"Hi {name},\n\nThanks for subscribing to my content!\n\n"
                "Unsubscribe anytime: https://blog.vamsikrishna.site/unsubscribe\n\n"
                "Best,\nVamsi",
        from_email="contact@vamsikrishna.site",
        recipient_list=[email],
        html_message=html_content
    )
    return "send"

#auto blog unsubscribe email
def send_unsubscribe_email(email):
    html_content = render_to_string(
        "blog/auto_email_unsubscribe.html",
        {"blog_url": "https://blog.vamsikrishna.site/"}
    )
    
    send_mail(
        subject="You're unsubscribed",
        message="You've been unsubscribed from our tech blog.\n\n"
               "Visit our blog: https://blog.vamsikrishna.site/",
        from_email="contact@vamsikrishna.site",
        recipient_list=[email],
        html_message=html_content
    )

#auto contact email to sender and admin portfolio
def send_emails_in_thread(name, email, phone=None, title=None, project_type=None, message=None):
    # Sender email
    sender_html = render_to_string("email/auto_email_sender.html", {"name": name})
    send_mail(
        "Thank You for Contacting Me!",
        "This is a plain text fallback message.", 
        "contact@vamsikrishna.site",
        [email],
        fail_silently=False,
        html_message=sender_html,
    )

    # Admin email
    admin_html = render_to_string("email/auto_email_admin.html", {
        "name": name,
        "email": email,
        "phone": phone,
        "subject": title,
        "project_type": project_type,
        "message": message
    })
    send_mail(
        "New Contact Form Submission",
        "A new message was received.",
        "contact@vamsikrishna.site",
        ["vamsikrishna.nagidi@gmail.com"],
        fail_silently=False,
        html_message=admin_html,
    )

#auto email subscribers new blog post
def auto_email_new_BlogPost(blog_post):
    for subscriber in NewsletterSubscriber.objects.all():
        send_mail(
            subject=f"New Blog Post: {blog_post.title}",
            message=f"Hi {subscriber.name},\n\nA new blog post is available: {blog_post.title}.\n\n"
                    f"Read more: https://blog.vamsikrishna.site/blog/{blog_post.slug}\n\nBest,\nVamsi",
            from_email="contact@vamsikrishna.site",
            recipient_list=[subscriber.email],
            html_message=render_to_string("blog/auto_email_new_blogPost.html", {
                "name": subscriber.name,
                "title": blog_post.title,
                "subtitle": blog_post.subtitle,
                "excerpt": blog_post.content[:200],
                "blog_url": f"https://blog.vamsikrishna.site/blog/{blog_post.slug}",
                "unsubscribe_url": "https://blog.vamsikrishna.site/unsubscribe",
            })
        )
    return "Emails sent"


#auto email to product buyer
def send_template_purchase_email(buyer_email, buyer_name, product_title, download_link):
    buyer_html = render_to_string("email/download_email.html", {
        "buyer_name": buyer_name,
        "product_title": product_title,
        "download_link": download_link,
        "now": datetime.datetime.now()
    })
    send_mail(
        f"Your {product_title} is ready for download!",
        f"Thank you for purchasing {product_title}!",
        "contact@vamsikrishna.site",
        [buyer_email],
        fail_silently=False,
        html_message=buyer_html,
    )

def send_payment_failed_email(buyer_email, buyer_name, product_title):
    buyer_html = render_to_string("email/payment_failed.html", {
        "buyer_name": buyer_name,
        "product_title": product_title,
        "now": datetime.datetime.now()
    })
    send_mail(
        f"Action needed: Payment failed for {product_title}",
        f"We couldn't process your payment for {product_title}.",
        "contact@vamsikrishna.site",
        [buyer_email],
        fail_silently=False,
        html_message=buyer_html,
    )


# Fix sleep time on render.com
from django.http import JsonResponse
from django.db import connection
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

def health_check(request):
    """Neon.tech-specific health check with connection pooling support"""
    response = {
        'status': 'ok',
        'timestamp': datetime.utcnow().isoformat(),
        'services': {
            'database': {
                'status': 'connected',
                'backend': 'neon.tech',
                'pool_status': None
            }
        }
    }
    status_code = 200

    try:
        # Test connection AND verify Neon's connection pool
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT 1, 
                pg_stat_activity_count(*) as active_connections,
                current_setting('max_connections') as max_connections
                FROM pg_stat_activity 
                WHERE usename = current_user
            """)
            row = cursor.fetchone()
            response['services']['database'].update({
                'active_connections': row[1],
                'max_connections': row[2],
                'pool_status': 'healthy'
            })
            
    except Exception as e:
        logger.error(f"Neon.tech connection failure: {str(e)}", exc_info=True)
        response.update({
            'status': 'error',
            'error': str(e),
            'services': {'database': {'status': 'disconnected'}}
        })
        status_code = 503  # Service Unavailable

    return JsonResponse(response, status=status_code)