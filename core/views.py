from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from core.models import Product, Product_Category, Order_Item, Order_Detail, Discount, Product_Inventory, Payment, Order_Detail, \
ProductReview, Wishlist, Address, ProductImages, Staff, Salary
from .context_processor import default
from core.forms import ProductReviewForm
from django.db.models import Count, Avg
from django.http import JsonResponse
from django.template.loader import render_to_string
import json
from django.urls import reverse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from paypal.standard.forms import PayPalPaymentsForm
import uuid
# Create your views here.


def index(request):
    categories = Product_Category.objects.all()
    products= Product.objects.all()
    context ={
     "products": products,
     "categories": categories
    }
    
    return render(request,'core/index.html',context)



def category_list_view(request):
    categories = Product_Category.objects.all()
    
    context = {
        "categories": categories
    }
    return render(request, 'core/category-list.html', context)

def product_list_view(request):
    products = Product.objects.all()
    context = {
        'products': products
    }
    return render(request, 'core/product-list.html', context)


def category_product_list_view(request, cid):
    category= Product_Category.objects.get(ID_Product_Category=cid)
    products = Product.objects.filter(category=category)
    
    context = {
        'category': category,
        'products':products
    }
    return render(request, "core/category-product-list.html", context)


def product_detail_view(request, pid ):
    categories = Product_Category.objects.all()
    products= Product.objects.all()
    product= Product.objects.get(ID_Product=pid)
    related_products= Product.objects.filter(category=product.category).exclude(ID_Product=pid)
    p_images = product.p_images.all()
    
    
    
    reviews =ProductReview.objects.filter(product=product).order_by("-Date")
    
    average_rating = ProductReview.objects.filter(product=product).aggregate(Rating = Avg('Rating'))
    
    review_form = ProductReviewForm()
    
    context= {
        'categories': categories,
        'products': products,
        'product':product,
        'related_products': related_products,
        'p_images': p_images,
        'reviews': reviews,
        'average_rating': average_rating,
        'review_form':review_form
    }
    
    return render(request, "core/product-detail.html", context)

def tag_list(request, tag_slug=None):
    product= Product.objects.all().order_by("-ID_Product")
    tag =None
    if tag_slug:
        tag = get_object_or_404(Tag,slug=tag_slug)
        products = products.filter(tag__in=[tag])
        
    context = {
        'products': products
    }
    return render(request, "core/tag.html", context)


def ajax_add_review(request, pid):
    product = Product.objects.get(ID_Product=pid)
    user = request.user
    
    review = ProductReview.objects.create(
        user=user,
        product=product,
        Review = request.POST['review'],
        Rating= request.POST['Rating']
    )
    
    context= {
        'user': user.username,
        'review': request.POST['review'],
        'rating': request.POST['Rating'],
        
    }
    
    average_reviews = ProductReview.objects.filter(product=product).aggregate(Rating=Avg("Rating"))
    return JsonResponse({
        'bool': True,
        'context': context,
        'avg_reviews': average_reviews
    })
    
    
def search_view(request):
    query = request.GET.get("q")
    
    products = Product.objects.filter(Name__icontains=query)
    
    context = {
        "products": products,
        "query": query
    }
    
    return render(request,  "core/search.html", context)


def add_to_cart(request):
    cart_product = {}
    cart_product[str(request.GET['ID_Product'])] = {
        'Quantity': request.GET['Quantity'],
        'Price': request.GET['Price'],
        'Image': request.GET['Image'],
        'Name': request.GET['Name'],
        'Money': float(request.GET['Price'])*int(request.GET['Quantity'])
    }
    
    if 'cart_data_obj' in request.session:
        if str(request.GET['ID_Product']) in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            cart_data[str(request.GET['ID_Product'])]['Quantity'] = int(cart_product[str(request.GET['ID_Product'])]['Quantity'])
            cart_data.update(cart_data)
            request.session['cart_data_obj']= cart_data
        
        else:
            cart_data = request.session['cart_data_obj']
            cart_data.update(cart_product)
            request.session['cart_data_obj'] = cart_data
    
    else:
        request.session['cart_data_obj'] =cart_product
    
    
    total_money=0
    for p_id, item in request.session['cart_data_obj'].items():
            total_money += int(item['Quantity'])* float(item['Price'])
    request.session['totalmoney']=total_money
    return JsonResponse(
        {
            "data": request.session['cart_data_obj'],
            "totalmoney": request.session['totalmoney'],
            "totalcartitems": len(request.session['cart_data_obj'])   
        }
    )
    

def cart_view(request):
    cart_total_amount = 0
    print(request.session)
    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['Quantity'])* float(item['Price'])
        return render(request, "core/cart.html", {
            "cart_data": request.session['cart_data_obj'],
            "totalcartitems": len(request.session['cart_data_obj']),
            'cart_total_amount': cart_total_amount
            })    
    else:
        return redirect('core:index') 
    
    
    
def delete_item_from_cart(request):
    product_id = str(request.GET.get('id'))
    
    if 'cart_data_obj' in request.session:
        if product_id in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            del cart_data[product_id]
            request.session['cart_data_obj'] = cart_data

    # Recalculate the total cart amount
    
    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for item in request.session['cart_data_obj'].values():
            qty = int(item.get('qty', 0))
            price = float(item.get('price', 0))
            cart_total_amount += qty * price
       
    context= render_to_string("core/cart-list.html",
            {"cart_data_obj": request.session['cart_data_obj'],
             "totalcartitems": len(request.session['cart_data_obj']),
            'cart_total_amount': cart_total_amount})

    print(context)
    return JsonResponse({
        "data":context,
        "cart_data_obj": request.session['cart_data_obj'],
        "totalcartitems": len(request.session['cart_data_obj']),
    })

    
    
def update_items_cart(request):
    
    ids = request.GET.get('ids').split(',')
    quantities = [int(float(num)) for num in request.GET.get('quantities').split(',')]

    cart_total_amount=0
    for i in range(len(ids)):
        if 'cart_data_obj' in request.session:
            product_id = ids[i]
            product_qty= quantities[i]           
            if product_id in request.session['cart_data_obj']:
                cart_data = request.session['cart_data_obj']
                if product_qty != cart_data[product_id]['Quantity']:
                    cart_data[product_id]['Quantity'] = product_qty
                    cart_data[product_id]['Money'] = product_qty * float(cart_data[product_id]['Price'])
                    request.session['cart_data_obj'] = cart_data
            
            cart_total_amount += product_qty * float(cart_data[product_id]['Price'])
    
    
    context = render_to_string("core/cart-list.html", {
        "cart_data_obj": request.session['cart_data_obj'],
        "totalcartitems": len(request.session['cart_data_obj']),
        'cart_total_amount': cart_total_amount
    })
    print(context)
    
    return JsonResponse({
        "data": context,
        "cart_data_obj": request.session['cart_data_obj'],
        "totalcartitems": len(request.session['cart_data_obj']),
        "totalmoney": cart_total_amount,
    })
    

def checkout_view(request):
    cart_total_amount = 0
    cart_data={}
    host = request.get_host()
    paypal_dict = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': request.session['totalmoney'],
        'item_name': "Order",
        "invoice": str(uuid.uuid4()),
        'currency_code': 'USD',
        'notify_url': f'http://{host}{reverse("paypal-ipn")}',
        'return': f'http://{host}{reverse("core:payment-completed")}',
        'cancel_return': f'http://{host}{reverse("core:payment-failed")}',
        'custom': "Order",
    }
    paypal_payment_button = PayPalPaymentsForm(initial=paypal_dict)

    if 'cart_data_obj' in request.session:
        cart_data = request.session['cart_data_obj']
        for p_id, item in cart_data.items():
            cart_total_amount += int(float(item['Price'])) * int(item['Quantity'])

        return render(request,"core/checkout.html",{
                "cart_data": cart_data,
                "totalcartitem": len(cart_data),
                "cart_total_amount": cart_total_amount,
                "paypal_payment_button": paypal_payment_button,
            }
        )

def payment_completed_view(request):
    cart_total_amount = 0
    cart_data = {}

    if 'cart_data_obj' in request.session:
        cart_data = request.session['cart_data_obj']
        for pid, item in cart_data.items():
            cart_total_amount += float(item['Price']) * int(item['Quantity'])

    return render(request, "core/payment-completed.html", {
        "cart_data_obj": cart_data,
        "cart_total_amount": cart_total_amount
    })
    
def payment_failed_view(request):
    return render(request, "core/payment-failed.html")

