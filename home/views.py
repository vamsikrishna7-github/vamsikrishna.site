from django.shortcuts import render, redirect,  get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import ContactForm
from .models import ContactMessage
from blog.models import NewsletterSubscriber
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from utils import increment_visitor_count, send_emails_in_thread
from threading import Thread

@csrf_protect
def homepage(request):
    views = increment_visitor_count()
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            messages.success(request, "Your message has been successfully sent. A confirmation email has been sent to your inbox from contact@vamsikrishna.site. If you do not see it, please check your spam folder.")
            form.save()
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            title = form.cleaned_data['title']
            project_type = form.cleaned_data['project_type']
            message = form.cleaned_data['message']

            email_thread = Thread(
            target=send_emails_in_thread,
            args=(name, email, phone, title, project_type, message)
            )
            email_thread.start()
            return redirect('home')
        else:
            messages.error(request, "Captcha is not valid. try again!")
    else:
        form = ContactForm()
    return render(request, 'index.html', {'form': form, 'views': views})

def admin_login(request):
    if request.user.is_authenticated:
        return redirect("/admin-panel/")
    
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect("/admin-panel/")
        else:
            messages.error(request, "Invalid Credentials")

    return render(request, "admin/admin_login.html")

@login_required(login_url='/admin/')
def admin_panel(request):
    messages = ContactMessage.objects.all().order_by("-created_at")
    subscribed_users = NewsletterSubscriber.objects.all().order_by("-subscribed_at")
    return render(request, "admin/admin_panel.html", {"messages": messages,  "subscribers":subscribed_users})

@login_required(login_url='/admin/')
def admin_logout(request):
    logout(request)
    return redirect("/admin/") 

@login_required(login_url='/admin/')
def delete_message(request, msg_id):
    message = get_object_or_404(ContactMessage, id=msg_id)
    message.delete()
    messages.success(request, "Message deleted successfully.")
    return redirect("admin_panel")