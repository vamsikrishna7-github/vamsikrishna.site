from django.shortcuts import render, redirect,  get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import ContactForm
from .models import ContactMessage
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_protect


@csrf_protect
def homepage(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            messages.success(request, "Your message has been sent successfully!")
            form.save()
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            title = form.cleaned_data['title']
            project_type = form.cleaned_data['project_type']
            message = form.cleaned_data['message']

            #auto response to the sender
            sender_html_content = render_to_string("email/auto_email_sender.html", {"name": name})
            send_mail(
                "Thank You for Contacting Me!",
                "This is a plain text fallback message.", 
                "vamsikrishna.nagidi@gmail.com",  
                [email],  
                fail_silently=False,
                html_message=sender_html_content,  
            )

            #auto response to the admin
            admin_html_content = render_to_string("email/auto_email_admin.html", {"name": name, "email": email, "phone":phone, "subject": title, "project_type":project_type ,"message": message})
            send_mail(
                "New Contact Form Submission",
                "A new message was received.",
                "vamsikrishna.nagidi@gmail.com",
                ["vamsikrishna.nagidi@gmail.com"],
                fail_silently=False,
                html_message=admin_html_content,
            )
            return redirect('home')
        else:
            messages.error(request, "Captcha is not valid. try again!")
    else:
        form = ContactForm()
    return render(request, 'index.html', {'form': form})

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
    return render(request, "admin/admin_panel.html", {"messages": messages})

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