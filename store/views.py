from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib import messages
from decimal import Decimal
import uuid
from datetime import datetime, timedelta
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
from .models import (
    Banner, Product, Category, Ingredient, WhyGlowify, Testimonial,
    ContactMessage, FAQ, OfferBanner, BogoProduct, ExclusiveOffer, 
    NewsletterSection, AboutPage, CoreValue, FounderSection, 
    CommitmentSection, LoginRecord
)

def home(request):
    return render(request, 'home.html', {
        'banners': Banner.objects.all(),
        'products': Product.objects.all()[:6],  
        'categories': Category.objects.all(),
        'ingredients': Ingredient.objects.all(),
        'why_points': WhyGlowify.objects.all(),
        'testimonials': Testimonial.objects.all(),
    })

def contact_view(request):
    faqs = FAQ.objects.all()
    if request.method == "POST":
        ContactMessage.objects.create(
            full_name=request.POST.get("full_name"),
            email=request.POST.get("email"),
            mobile=request.POST.get("mobile"),
            message=request.POST.get("message"),
        )
        return redirect("contact")
    return render(request, "contact.html", {"faqs": faqs})

def offers(request):
    context = {
        'banner': OfferBanner.objects.filter(is_active=True).first(),
        'bogo_products': BogoProduct.objects.all()[:3],
        'exclusive': ExclusiveOffer.objects.filter(is_active=True).first(),
        'newsletter': NewsletterSection.objects.filter(is_active=True).first(),
    }
    return render(request, 'offers.html', context)

def about(request):
    context = {
        'about': AboutPage.objects.filter(is_active=True).first(),
        'core_values': CoreValue.objects.all(),
        'founder': FounderSection.objects.filter(is_active=True).first(),
        'commitment': CommitmentSection.objects.filter(is_active=True).first(),
    }
    return render(request, 'about.html', context)

def login_view(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        if email and password:
            LoginRecord.objects.create(email=email, password=password)
            messages.success(request, "Login Successful ✅")
            return redirect('login')
        else:
            messages.error(request, "Please fill all fields ❌")
    return render(request, 'login.html')

def shop(request):
    products = Product.objects.all()
    # Add filter logic here if needed
    brand = request.GET.get('brand')
    color = request.GET.get('color')
    price = request.GET.get('price')
    
    if brand:
        products = products.filter(brand=brand)
    if color:
        products = products.filter(color=color)
    if price == 'low':
        products = products.filter(price__lt=500)
    elif price == 'mid':
        products = products.filter(price__gte=500, price__lte=1000)
    elif price == 'high':
        products = products.filter(price__gt=1000)
        
    return render(request, 'shop.html', {'products': products})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    related_products = Product.objects.exclude(pk=pk)[:4]
    return render(request, 'product_detail.html', {
        'product': product,
        'related_products': related_products
    })

def add_to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    cart = request.session.get('cart', {})
    pk_str = str(pk)
    qty = int(request.POST.get('quantity', 1))
    shade = request.POST.get('shade', product.color)
    
    if pk_str in cart:
        cart[pk_str]['qty'] += qty
        cart[pk_str]['shade'] = shade  # Update shade if changed
    else:
        cart[pk_str] = {
            'name': product.name,
            'price': str(product.price),
            'image': product.image.url,
            'shade': shade,
            'qty': qty,
            'selected': True
        }
    
    request.session['cart'] = cart
    request.session.modified = True
    return redirect('cart')

def cart(request):
    cart = request.session.get('cart', {})
    cart_items = []
    subtotal = Decimal('0')
    
    for pk, item in cart.items():
        item_total = Decimal(item['price']) * item['qty']
        cart_items.append({
            'id': pk,
            'name': item['name'],
            'price': item['price'],
            'image': item['image'],
            'shade': item['shade'],
            'qty': item['qty'],
            'total': item_total,
            'selected': item['selected']
        })
        if item['selected']:
            subtotal += item_total
    
    shipping = Decimal('50') if subtotal > 0 else Decimal('0')
    gst = Decimal('50') if subtotal > 0 else Decimal('0')
    total = subtotal + shipping + gst
    
    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'shipping': shipping,
        'gst': gst,
        'total': total,
        'item_count': len([i for i in cart.values() if i['selected']])
    })

def update_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        action = request.POST.get('action')
        cart = request.session.get('cart', {})
        
        if product_id in cart:
            if action == 'increase':
                cart[product_id]['qty'] += 1
            elif action == 'decrease':
                cart[product_id]['qty'] = max(1, cart[product_id]['qty'] - 1)
            elif action == 'toggle':
                cart[product_id]['selected'] = not cart[product_id]['selected']
        
        request.session['cart'] = cart
        request.session.modified = True
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'})

def remove_from_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        cart = request.session.get('cart', {})
        if product_id in cart:
            del cart[product_id]
        request.session['cart'] = cart
        request.session.modified = True
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'})

def checkout(request):
    cart = request.session.get('cart', {})
    selected_items = [item for item in cart.values() if item['selected']]
    
    if not selected_items:
        messages.warning(request, "Please select items to checkout")
        return redirect('cart')
    
    subtotal = sum(Decimal(item['price']) * item['qty'] for item in selected_items)
    shipping = Decimal('100')
    gst = Decimal('100')
    total = subtotal + shipping + gst
    
    return render(request, 'checkout.html', {
        'cart_items': selected_items,
        'subtotal': subtotal,
        'shipping': shipping,
        'gst': gst,
        'total': total
    })

def place_order(request):
    if request.method == 'POST':
        cart = request.session.get('cart', {})
        selected_items = {k:v for k,v in cart.items() if v['selected']}
        
        if not selected_items:
            return redirect('cart')
        
        order_id = str(uuid.uuid4().int)[:9]
        order_data = {
            'order_id': order_id,
            'items': selected_items,
            'billing': {
                'first_name': request.POST.get('first_name'),
                'last_name': request.POST.get('last_name'),
                'mobile': request.POST.get('mobile'),
                'address': request.POST.get('address'),
                'city': request.POST.get('city'),
                'state': request.POST.get('state'),
                'pincode': request.POST.get('pincode'),
            },
            'date': datetime.now().strftime('%b %d, %Y at %I:%M %p'),
            'delivery_date': (datetime.now() + timedelta(days=5)).strftime('%A, %B %d')
        }
        
        request.session['last_order'] = order_data
        # Remove only selected items from cart, keep unselected
        request.session['cart'] = {k:v for k,v in cart.items() if not v['selected']}
        request.session.modified = True
        return redirect('order_success', order_id=order_id)
    
    return redirect('checkout')

def order_success(request, order_id):
    order = request.session.get('last_order', {})
    if not order or order['order_id'] != order_id:
        messages.error(request, "Order not found")
        return redirect('shop')
    
    items = list(order['items'].values())
    subtotal = sum(Decimal(item['price']) * item['qty'] for item in items)
    shipping = Decimal('100')
    gst = Decimal('100')
    total = subtotal + shipping + gst
    
    return render(request, 'order_success.html', {
        'order': order,
        'items': items,
        'subtotal': subtotal,
        'shipping': shipping,
        'gst': gst,
        'total': total
    })


def register_view(request):
    if request.method == "POST":
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered")
            return redirect('register')
        
        # Create user
        name_parts = full_name.split(' ', 1)
        user = User.objects.create(
            username=email,
            email=email,
            first_name=name_parts[0],
            last_name=name_parts[1] if len(name_parts) > 1 else '',
            password=make_password(password)
        )
        messages.success(request, "Account created successfully!")
        return redirect('login')
    
    return render(request, 'register.html')

def login_view(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        remember = request.POST.get('remember')
        
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            login(request, user)
            if not remember:
                request.session.set_expiry(0)
            messages.success(request, "Login Successful")
            return redirect('home')
        else:
            messages.error(request, "Invalid email or password")
            return redirect('login')
    
    return render(request, 'login.html')