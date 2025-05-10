from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from django.urls import reverse
from django.template.loader import render_to_string
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.db import transaction
from django.db.models import Count, Avg, Prefetch, Sum
from decimal import Decimal
from collections import defaultdict
from paypal.standard.forms import PayPalPaymentsForm
from taggit.models import Tag
import uuid
import json

# App-specific imports
from core.models import Product, Product_Category, Order_Item, Order_Detail, Discount, Product_Inventory, Payment, \
    ProductReview, Wishlist, ProductImages, Staff, Salary, Coupon
from core.forms import ProductReviewForm
from userauths.models import Profile

from .RAG_system.RAG import Answer_Question
from .Recommendation_system import Recommendation_System_Type_1


def index(request):
    """Homepage view showing all products and recommendations"""
    categories = Product_Category.objects.all()
    products = Product.objects.all()
    recommended_ids = Recommendation_System_Type_1()
    
    recommended_products = list(Product.objects.filter(id__in=recommended_ids))

    saleoff_products = Product.objects.filter(discount__Active=True)
    dessert_products = Product.objects.filter(category__ID_Product_Category="CAT004")
    fruit_products = Product.objects.filter(category__ID_Product_Category="CAT001")
    campaigns = Discount.objects.filter(Active=True)

    context = {
        "products": products,
        "categories": categories,
        "recommended_products": recommended_products,
        "dessert_products": dessert_products,
        "fruit_products": fruit_products,
        'saleoff_products': saleoff_products,
        'campaigns': campaigns
    }

    return render(request, 'core/index.html', context)


def category_list_view(request):
    """Lists all product categories"""
    categories = Product_Category.objects.all()
    return render(request, 'core/category-list.html', {"categories": categories})


def product_list_view(request):
    """Lists all products"""
    products = Product.objects.all()
    return render(request, 'core/product-list.html', {'products': products})


def category_product_list_view(request, cid):
    categories = Product_Category.objects.all()
    related_category= Product_Category.objects.get(ID_Product_Category=cid)
    products = Product.objects.filter(category=related_category)
    
    context = {
        'categories': categories,
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
    
    if request.POST:
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
    categories = Product_Category.objects.all()
    products = Product.objects.filter(Name__icontains=query)
    
    context = {
        "products": products,
        "query": query,
        "categories": categories
    }
    return render(request,  "core/search.html", context)


def add_to_cart(request):
    cart_product = {}
    cart_product[str(request.GET['ID_Product'])] = {
        'Quantity': request.GET['Quantity'],
        'Image': request.GET['Image'],
        'Price': request.GET['Price'],
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
    cart_total_amount = request.session['totalmoney']
    final_amount = 0
    coupon_code = None

    if request.method == "POST":
        code = request.POST.get("coupon")
        coupon = Coupon.objects.filter(Code=code, Active=True).first()
        if coupon:
            coupon_code = coupon.Code
            request.session['applied_coupon'] = code
            messages.success(request, "Coupon Activated")
        else:
            request.session.pop('applied_coupon', None)
            messages.error(request, "Coupon Does Not Exist")

    if 'cart_data_obj' in request.session:
        if 'applied_coupon' in request.session:
            applied_coupon = Coupon.objects.filter(Code=request.session['applied_coupon'], Active=True).first()
            if applied_coupon:
                discount_money = cart_total_amount * float(applied_coupon.Discount)
                coupon_code = applied_coupon.Code
                request.session['discount_money']= discount_money
            request.session['totalmoney'] = cart_total_amount - discount_money
        else:
            request.session['totalmoney'] = cart_total_amount

        return render(request, "core/cart.html", {
            "cart_data": request.session['cart_data_obj'],
            "totalcartitems": len(request.session['cart_data_obj']),
            "cart_total_amount": cart_total_amount,
            "final_amount": final_amount,
            "coupon_code": coupon_code,
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
        for p_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['Quantity'])* float(item['Price'])
    
    if 'applied_coupon' in request.session:
        applied_coupon = Coupon.objects.filter(Code=request.session['applied_coupon'], Active=True).first()
        if applied_coupon:
            discount_money = cart_total_amount * float(applied_coupon.Discount)
            request.session['discount_money']= discount_money
        request.session['totalmoney'] = cart_total_amount - discount_money
        context = render_to_string("core/cart-list.html", {
            "cart_data_obj": request.session['cart_data_obj'],
            "totalcartitems": len(request.session['cart_data_obj']),   
            "totalmoney": cart_total_amount,
            "final_amount": request.session['totalmoney'],
            "coupon_code": request.session['applied_coupon'],
        })
    else:
        request.session['totalmoney'] = cart_total_amount
        
        context = render_to_string("core/cart-list.html", {
            "cart_data_obj": request.session['cart_data_obj'],
            "totalcartitems": len(request.session['cart_data_obj']),   
            "totalmoney": cart_total_amount,
            "final_amount": cart_total_amount
        })
    
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
    if 'applied_coupon' in request.session:
        applied_coupon = Coupon.objects.filter(Code=request.session['applied_coupon'], Active=True).first()
        if applied_coupon:
            discount_money = cart_total_amount * float(applied_coupon.Discount)
            request.session['discount_money']= discount_money
        request.session['totalmoney'] = cart_total_amount - discount_money
        context = render_to_string("core/cart-list.html", {
            "cart_data_obj": request.session['cart_data_obj'],
            "totalcartitems": len(request.session['cart_data_obj']),   
            "totalmoney": cart_total_amount,
            "final_amount": request.session['totalmoney'],
            "coupon_code": request.session['applied_coupon'],
        })
    else:
        request.session['totalmoney'] = cart_total_amount
        
        context = render_to_string("core/cart-list.html", {
            "cart_data_obj": request.session['cart_data_obj'],
            "totalcartitems": len(request.session['cart_data_obj']),   
            "totalmoney": cart_total_amount,
            "final_amount": cart_total_amount
        })
    
    return JsonResponse({
        "data": context,
        "cart_data_obj": request.session['cart_data_obj'],
        "totalcartitems": len(request.session['cart_data_obj']),
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
            cart_data[p_id]['subtotal']= float(item['Price']) * int(item['Quantity'])
            cart_total_amount += cart_data[p_id]['subtotal']
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




@csrf_exempt
def response(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        message = data.get('message', '')
        answer = Answer_Question(message)
        # new_chat = Chat(message=message, response=answer)
        # new_chat.save()
        return JsonResponse({'response': answer})
    
    return JsonResponse({'response': 'Invalid request'}, status=400)




def profile_view(request):
    
    profile, created = Profile.objects.get_or_create(user=request.user)
    if created:
        profile.full_name = f"{request.user.last_name}{request.user.first_name}"
        profile.phone = request.user.Phone  # Ensure the attribute name is lowercase if your User model has `phone`
        profile.save()

    context = {
        'profile': profile
    }
    return render(request, 'core/profile.html', context)
    

def address_view(request):
    profile =  Profile.objects.get(user=request.user)
    
    context={
        "profile": profile
    }
    return render(request,"core/address.html",context)


def order_history_view(request):
    orders = Order_Detail.objects.filter(user=request.user) \
        .annotate(items_count=Count('order_item')) \
        .order_by('-Date')
    
    order_list =[]
    for order in orders.values():
        order['Date']= str(order['Date'])
        order['Total_Price'] = float(order['Total_Price'])
        order['Payment_Status']= int(order['Payment_Status'])
        order_list.append(order)
        
    context = {
        'order_list': order_list
    }
    return render(request,'core/order-history.html', context)


def track_order_view(request):
    orders = Order_Detail.objects.filter(user=request.user).order_by("-Date")
    
    order_data = []

    for order in orders:
        items = Order_Item.objects.filter(order_detail=order).select_related('product')
        order_data.append({
            'order': order,
            'items': items
        })

    context = {
        'order_data': order_data
    }

    return render(request, "core/track-order.html", context)



def contact_view(request):
    return render(request, "core/contact.html")



def change_password_view(request):
    user = request.user
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        if confirm_password != new_password:
            messages.error(request, 'Confirm password does not match')
            return redirect('core:change_password')
        
        if check_password(old_password,user.password):
            user.set_password(new_password)
            user.save()
            messages.success(request, 'Password changed successfully')
            return redirect('core:profile')
        else:
            messages.error(request, 'Old password is incorrect')
            return redirect('core:change_password')
    return render(request, "core/change-password.html")



def place_order_completed(request):
    cart_data = request.session.get('cart_data_obj')
    total_price = request.session.get('totalmoney')

    if not cart_data or not total_price:
        return redirect("cart")  # Redirect to cart if session is invalid

    if request.method != 'POST':
        return redirect("cart")  # Or show a 405 page if desired

    payment_method = request.POST.get('payment_option')
    special_requests = request.POST.get('special_requests', '')

    try:
        with transaction.atomic():
            # Create Payment
            new_payment = Payment.objects.create(
                user=request.user,
                Method=payment_method
            )

            # Create Order Detail
            new_order = Order_Detail.objects.create(
                user=request.user,
                Total_Price=total_price,
                Payment=new_payment,
                Note=special_requests
            )

            # Create Order Items
            for product_id, item in cart_data.items():
                try:
                    product = Product.objects.get(ID_Product=product_id)
                    Order_Item.objects.create(
                        order_detail=new_order,
                        product=product,
                        Quantity=int(item.get('Quantity', 0)),
                        Total=item.get('Money', 0)
                    )
                except Product.DoesNotExist:
                    continue  # Optionally log missing product

            # Clear session data after successful transaction
            del request.session['cart_data_obj']
            del request.session['totalmoney']
            payment_method=' '.join(payment_method.split('_'))
            print(payment_method)
            context = {
                'totalmoney': total_price,
                'num_items': len(cart_data),
                'method': payment_method
            }
            
            return render(request, "core/place-order-completed.html", context)
    except Exception as e:
        # Log error or redirect to error page
        print("Order placement failed:", e)
        return redirect("cart")  # Optional: redirect to a dedicated error page
    
    
def order_management(request):
    
    return render(request,"core/order-management.html")




def revenue_management(request):
    product_metrics = {}
    total_revenue = Decimal('0.00')
    total_cost = Decimal('0.00')
    
    order_items = Order_Item.objects.select_related('product', 'order_detail').all()
    
    for item in order_items:
        if not item.product or not item.order_detail:
            continue

        product = item.product
        quantity = item.Quantity

        # Calculate effective price (considering discount)
        price = product.get_price() or Decimal('0.00')
        cost = product.Cost or Decimal('0.00')

        revenue = price * quantity
        cost_total = cost * quantity
        gross_profit = revenue - cost_total

        total_revenue += revenue
        total_cost += cost_total

        if product.ID_Product not in product_metrics:
            product_metrics[product.ID_Product] = {
                'name': product.Name,
                'total_quantity_sold': 0,
                'revenue': Decimal('0.00'),
                'cost': Decimal('0.00'),
                'gross_profit': Decimal('0.00'),
            }

        product_metrics[product.ID_Product]['total_quantity_sold'] += quantity
        product_metrics[product.ID_Product]['revenue'] += revenue
        product_metrics[product.ID_Product]['cost'] += cost_total
        product_metrics[product.ID_Product]['gross_profit'] += gross_profit

    daily_data = defaultdict(lambda: {
        'revenue': Decimal('0.00'),
        'cost': Decimal('0.00'),
        'gross_profit': Decimal('0.00'),
        'order_count': 0
    })

    order_details = Order_Detail.objects.prefetch_related(
        Prefetch('order_item_set', queryset=Order_Item.objects.select_related('product'))
    )
    
    
    for order in order_details:
        date = order.Date.date()  # Convert to just the date (not datetime)
        daily_data[date]['order_count'] += 1
        
        for item in order.order_item_set.all():
            if not item.product:
                continue

            price = item.product.get_price() or Decimal('0.00')
            cost = item.product.Cost or Decimal('0.00')
            quantity = item.Quantity

            revenue = price * quantity
            total_cost = cost * quantity
            gross_profit = revenue - total_cost

            daily_data[date]['revenue'] += revenue
            daily_data[date]['cost'] += total_cost
            daily_data[date]['gross_profit'] += gross_profit
        
        
            
    # Optional: sort by date
    sorted_data = dict(sorted(daily_data.items()))
    revenues = []
    costs= []
    profits = []
    labels = []    
    
    for key,value in sorted_data.items():
        revenues.append(float(value['revenue']))
        costs.append(float(value['cost']))
        profits.append(float(value['gross_profit']))
        labels.append(key.strftime('%Y-%m-%d'))
    
    context= {
        'total_revenue': total_revenue,
        'total_cost': total_cost,
        'total_gross_profit': total_revenue - total_cost,
        'product_metrics': product_metrics,
        'daily_data': sorted_data,
        'labels': labels,
        "revenues": revenues,
        'costs': costs,
        'profits':profits
        
    }
        
    
    return render(request,"core/revenue-management.html", context)

def staff_management(request):
    return render(request,"core/staff-management.html")

def inventory_management(request):
    products = Product.objects.all()
    categories=Product_Category.objects.all()
    inventories_json = [
        {
            "Name": p.Name,
            "Category": p.category.Name,
            "Price": float(p.Price),
            "Unit": p.inventory.Unit,
            "Quantity": p.inventory.Quantity,
            "Updated": p.inventory.Updated.strftime('%Y-%m-%d'),  # format datetime if needed
        }
        for p in products
    ]
    context = {
        "inventories_json": inventories_json,
        "categories": categories
    }
    return render(request, "core/inventory-management.html", context)



def customer_orders(request):
    orders = []

    for order in Order_Detail.objects.all().order_by('-Date'):
        items = Order_Item.objects.filter(order_detail=order)
        item_count = sum(item.Quantity for item in items)

        order_items = []
        for item in items:
            product = item.product
            image = ProductImages.objects.filter(product=product).first()
            image_url = request.build_absolute_uri(image.image.url) if image and hasattr(image, 'image') else "https://via.placeholder.com/80"

            order_items.append({
                "name": product.Name,
                "sku": product.ID_Product,
                "quantity": item.Quantity,
                "price": float(item.Total),
                "image": image_url
            })

        customer = order.user
        customer_name = customer.username if customer else "Anonymous"
        customer_email = customer.email if customer else ""
        customer_phone = getattr(customer, "phone", "") if customer else ""

        payment = order.Payment
        payment_method = payment.Method if payment else "N/A"

        orders.append({
            "id": order.ID_Order_Detail,
            "customer": customer_name,
            "date": order.Date.strftime("%Y-%m-%d"),
            "items": item_count,
            "total": float(order.Total_Price),
            "status": order.Delivery_Status.lower(),
            "customerEmail": customer_email,
            "customerPhone": customer_phone,
            "shippingAddress": getattr(order, "Address", ""),
            "paymentMethod": payment_method,
            "shippingCarrier": getattr(order, "Shipping_Carrier", ""),
            "trackingNumber": getattr(order, "Tracking_Number", ""),
            "estimatedDelivery": order.Date.strftime("%Y-%m-%d"),
            "orderItems": order_items
        })

    return JsonResponse({"orders": orders})


@csrf_exempt
def update_order_status(request, order_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            new_status = data.get('status')

            order = Order_Detail.objects.get(ID_Order_Detail=order_id)
            order.Delivery_Status = new_status
            order.save()

            return JsonResponse({'message': 'Order status updated successfully'})
        except Order_Detail.DoesNotExist:
            return JsonResponse({'error': 'Order not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request method'}, status=400)


def order_stats(request):
    
    try:

        total_orders = Order_Detail.objects.count()

        pending_orders = Order_Detail.objects.filter(Delivery_Status='pending').count()
        processing_orders = Order_Detail.objects.filter(Delivery_Status='process').count()

        total_revenue = Order_Detail.objects.aggregate(total=Sum('Total_Price'))['total'] or 0
        return JsonResponse({
            'total_orders': total_orders,
            'pending_orders': pending_orders,
            'processing_orders': processing_orders,
            'total_revenue': float(total_revenue)
        })

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


