from django.shortcuts import render, redirect,  get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import ContactForm, TemplateProductForm
from .models import ContactMessage, TemplateProducts, TemplatePurchase
from blog.models import NewsletterSubscriber
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from utils import increment_visitor_count, send_emails_in_thread, send_template_purchase_email, send_payment_failed_email
from threading import Thread
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import razorpay
import json
from django.http import JsonResponse
from requests.exceptions import RequestException


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
    templateProducts = TemplateProducts.objects.all().order_by("-created_at")
    templatePurchase = TemplatePurchase.objects.all().order_by("-purchased_at")
    
    total_amount = sum(purchase.amount_paid for purchase in templatePurchase if purchase.is_verified)
    
    for product in templateProducts:
        if product.image_video:
            file_extension = product.image_video.url.split('.')[-1].lower()
            product.is_video = file_extension in ["mp4", "webm", "ogg"]
        else:
            product.is_video = False
    return render(request, "admin/admin_panel.html", {
        "messages": messages, 
        "subscribers": subscribed_users, 
        "templateProducts": templateProducts, 
        "templatePurchase": templatePurchase,
        "total_amount": total_amount
    })

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

def templates(request):
    templateProducts = TemplateProducts.objects.all().order_by("-created_at")
    return render(request, "sellWork/templates.html", {"templateProducts": templateProducts, 'pay': False})

client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

def buy_template_view(request):
    templateProducts = TemplateProducts.objects.all().order_by("-created_at")
    if request.method == "POST":
        buyer_name = request.POST.get("buyer_name")
        buyer_email = request.POST.get("buyer_email")
        buyer_phone = request.POST.get("buyer_phone")
        template_id = request.POST.get("product_id")
        template = get_object_or_404(TemplateProducts, id=template_id)
        template_price = template.price
        template_title = template.title
        template_description = template.description
        try:
            order_amount = int(template_price * 100)
            order_currency = 'INR'
            order_receipt = 'order_rcptid_11'

            order = client.order.create(dict(amount=order_amount, currency=order_currency, receipt=order_receipt, payment_capture=1))

            context = {
                'razorpay_key_id': settings.RAZORPAY_KEY_ID,
                'order_id': order['id'],
                'amount': order_amount,
                'template_title': template_title,
                'template_description': template_description,
                'templateProducts': templateProducts,
                'template_id': template_id,
                'buyer_name': buyer_name,
                'buyer_email': buyer_email,
                'buyer_phone': buyer_phone,
                'pay': True
            }

            purchase = TemplatePurchase.objects.create(
                template=template,
                buyer_name=buyer_name,
                buyer_email=buyer_email,
                buyer_phone=buyer_phone,
                razorpay_order_id=order['id'],
                amount_paid=template.price
            )
            purchase.save()

            return render(request, 'sellWork/templates.html', context)
        except RequestException as e:
            print("API Error:", e)
            return redirect('templates')
    return redirect('templates')

@csrf_exempt
def payment_success(request):
    if request.method == "POST":
        data = json.loads(request.body)
        print("🧾 Razorpay data received:", data)

        template_id = int(data.get('template_id'))
        print("🧾 Template ID:", template_id)
        if not template_id:
            return JsonResponse({"success": False, "error": "Template ID missing."})
        razorpay_order_id = data.get('razorpay_order_id')
        razorpay_payment_id = data.get('razorpay_payment_id')
        razorpay_signature = data.get('razorpay_signature')

        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

        try:
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': razorpay_payment_id,
                'razorpay_signature': razorpay_signature
            }

            client.utility.verify_payment_signature(params_dict)

            template = TemplateProducts.objects.get(id=template_id)
            print("🧾 Template-source:", template.source)

            TemplatePurchase.objects.filter(razorpay_order_id=razorpay_order_id).update(
                razorpay_payment_id=razorpay_payment_id,
                razorpay_signature=razorpay_signature,
                is_verified=True
            )
            buyer= TemplatePurchase.objects.get(razorpay_order_id=razorpay_order_id)

            email_thread = Thread(
            target=send_template_purchase_email,
            args=(buyer.buyer_email, buyer.buyer_name, template.title, template.source)
            )
            email_thread.start()

            return JsonResponse({
                "success": True,
                "template_source": template.source,
                'buyer_email': buyer.buyer_email
            })

        except razorpay.errors.SignatureVerificationError:
            print(" Signature verification failed.")
            return JsonResponse({"success": False, "error": "Signature verification failed."})

    # return JsonResponse({"success": False, "error": "Invalid request method."})
    return redirect('templates')

@csrf_exempt
def payment_failed(request):
    # email_thread = Thread(
    #         target=send_payment_failed_email,
    #         args=(buyer.buyer_email, buyer.buyer_name, template.title, template.source)
    #         )
    # email_thread.start()
    return JsonResponse({'success': False, 'message': 'Payment failed. Please try again.'})


@login_required(login_url='/admin/')
def create_product(request):
    if request.method == "POST":
        form = TemplateProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('admin_panel') 
    else:
        form = TemplateProductForm()
    
    return render(request, "admin/admin_create_product.html", {"form": form})

@login_required(login_url='/admin/')
def edit_product(request, id):
    product = get_object_or_404(TemplateProducts, id=id)
    if request.method == "POST":
        form = TemplateProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('admin_panel')
    else:
        form = TemplateProductForm(instance=product)
    
    return render(request, "admin/admin_edit_product.html", {"form": form, "product": product})

@login_required(login_url='/admin/')
def delete_product(request, id):
    product = get_object_or_404(TemplateProducts, id=id)
    product.delete()
    return redirect('admin_panel')
