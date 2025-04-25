from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from core.models import Product, Product_Category, Order_Item, Order_Detail, Discount, Product_Inventory, Payment, \
ProductReview, Wishlist, ProductImages, Staff, Salary
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
from taggit.models import Tag
from .AI_model import Answer_Question, Recommendation_System_Type_1
from userauths.models import Profile
from django.contrib.auth.hashers import check_password
from django.contrib import messages
from django.db import transaction
from django.utils import timezone
from django.views.decorators.http import require_GET
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.


def index(request):
    categories = Product_Category.objects.all()
    products= Product.objects.all()
    recommended_ids= Recommendation_System_Type_1()
    recommended_products = list(Product.objects.filter(id__in=recommended_ids))
    
    saleoff_products = Product.objects.filter(discount__Active=True)
    dessert_products = Product.objects.filter(category__ID_Product_Category="CAT004")
    fruit_products = Product.objects.filter(category__ID_Product_Category="CAT001")
    
    campaigns = Discount.objects.filter(Active=True)
    context ={
     "products": products,
     "categories": categories,
     "recommended_products": recommended_products,
     "dessert_products": dessert_products,
     "fruit_products":fruit_products,
     'saleoff_products': saleoff_products,
     'campaigns': campaigns
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
    request.session['totalmoney']= cart_total_amount
    
    context = render_to_string("core/cart-list.html", {
        "cart_data_obj": request.session['cart_data_obj'],
        "totalcartitems": len(request.session['cart_data_obj']),   
        "totalmoney": cart_total_amount,
         
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
    
    return render(request,"core/address.html")


def order_history_view(request):
    order_list = Order_Detail.objects.filter(user = request.user).order_by("-ID_Order_Detail")
    context={
        'Order_list': order_list
    }
    return render(request,'core/order-history.html', context)


def track_order_view(request):
    order_list = Order_Detail.objects.filter(user=request.user, Delivery_Status='process').order_by("-Date")
    item_lists = []

    for order in order_list:
        item_list = Order_Item.objects.filter(order_detail=order)
        item_lists.append(item_list)
    print(item_lists)
    context = {
        'item_lists': item_lists
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
    return render(request,"core/revenue-management.html")

def staff_management(request):
    total_employees = Staff.objects.count()

    active_employees = Staff.objects.filter(status="active").count()

    on_leave_employees = Staff.objects.filter(status="on_leave").count()

    start_of_month = timezone.now().replace(day=1)
    new_employees_this_month = Staff.objects.filter(Started__gte=start_of_month).count()

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        staffs = Staff.objects.select_related('user').all()
        data = []
        for staff in staffs:
            data.append({
                'id': staff.ID_Staff,
                'idcard': staff.ID_card,
                'name': staff.Name,
                'department': "N/A", 
                'position': staff.Position,
                'started': staff.Started.strftime('%Y-%m-%d') if staff.Started else '',
                'status': staff.status,
            })
        return JsonResponse({'staffs': data})

    else:
        context = {
            'total_employees': total_employees,
            'active_employees': active_employees,
            'on_leave_employees': on_leave_employees,
            'new_employees_this_month': new_employees_this_month,
        }
        return render(request, "core/staff-management.html", context)
    
def add_employee(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        idcard = request.POST.get('idcard')
        name = request.POST.get('name')
        birthday = request.POST.get('birthday')
        position = request.POST.get('position')
        started = request.POST.get('started')

        new_staff = Staff.objects.create(
            ID_card=idcard,
            ID_Staff=id,
            Name=name,
            user=None, 
            Position=position,
            Started=started,
            Birthday = birthday

        )
        
        return redirect('core:staff_management')


    return render(request, "core/add_employee.html")


def update_employee(request, employee_id):
    staff = get_object_or_404(Staff, ID_Staff=employee_id)

    if request.method == 'POST':
        staff.ID_Staff = request.POST.get('id')
        staff.ID_card = request.POST.get('idcard')
        staff.Name = request.POST.get('name')
        staff.Birthday = request.POST.get('birthday')
        staff.Position = request.POST.get('position')
        staff.Started = request.POST.get('started')
        staff.status = request.POST.get('status')
        staff.save()

        return redirect('core:staff_management')

    return render(request, 'core/update_employee.html', {'staff': staff})

def delete_employee(request, employee_id):
    employee = get_object_or_404(Staff, ID_Staff=employee_id)
    
    employee.delete()

    return JsonResponse({'message': 'Employee deleted successfully!'})

def payroll_view(request):
    active_staffs = Staff.objects.filter(status='active')
    salary_records = Salary.objects.select_related('staff').order_by('-Date')

    context = {
        'staffs': active_staffs,
        'salary_records': salary_records,
    }
    return render(request, 'core/payroll.html', context)

@require_GET
def payroll_data(request):
    staffs = Staff.objects.filter(status='active')
    payroll_data = []
    total_payroll = 0
    total_net_pay = 0

    for staff in staffs:
        try:
            salary_record = Salary.objects.filter(staff=staff).latest('Date')
            salary = salary_record.Salary
            bonus = salary_record.Bonus
            net_pay = salary + bonus

            payroll_data.append({
                'id': staff.ID_Staff,
                'name': staff.Name,
                'salary': f"{salary:.2f}",
                'bonus': f"{bonus:.2f}",
                'net_pay': f"{net_pay:.2f}",
                'status': staff.status,
            })

            total_payroll += salary + bonus
            total_net_pay += net_pay

        except ObjectDoesNotExist:
            # Nếu staff chưa có lương, vẫn add vào với 0
            payroll_data.append({
                'id': staff.ID_Staff,
                'name': staff.Name,
                'salary': "0.00",
                'bonus': "0.00",
                'net_pay': "0.00",
                'status': staff.status,
            })

    return JsonResponse({
        'data': payroll_data,
        'total_payroll': f"{total_payroll:.2f}",
        'total_net_pay': f"{total_net_pay:.2f}",
    })

@csrf_exempt
def update_salary(request):
    if request.method == 'POST':
        salary_id = request.POST.get('salary_id')
        new_salary = request.POST.get('salary')
        new_bonus = request.POST.get('bonus')

        try:
            salary = Salary.objects.get(ID_Salary=salary_id)
            salary.Salary = new_salary
            salary.Bonus = new_bonus
            salary.save()
            return JsonResponse({'success': True})
        except Salary.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Salary not found'})

    return JsonResponse({'success': False, 'error': 'Invalid request'})


def inventory_management(request):
    inventories = Product_Inventory.objects.all()
    inventories_json = [
        {
            "Name": inv.Name,
            "Unit": inv.Unit,
            "Quantity": inv.Quantity,
            "Updated": inv.Updated.strftime('%Y-%m-%d'),  # format datetime if needed
        }
        for inv in inventories
    ]
    
    context = {
        "inventories_json": inventories_json
    }
    return render(request, "core/inventory-management.html", context)


def add_to_wishlist(request):
    product_id = request.GET.get('id')

    if not product_id:
        return JsonResponse({"error": "Missing product ID"}, status=400)

    try:
        product = Product.objects.get(ID_Product=product_id)
    except Product.DoesNotExist:
        return JsonResponse({"error": "Product not found"}, status=404)

    wishlist_item, created = Wishlist.objects.get_or_create(
        product=product,
        user=request.user
    )

    return JsonResponse({"added": created})




def wishlist_view(request):
    wishlist_items = Wishlist.objects.filter(user=request.user)
    context = {
        'wishlist_items': wishlist_items
    }
    return render(request, 'core/wishlist.html', context)

def remove_from_wishlist(request, pid):
    product = get_object_or_404(Product, ID_Product=pid)
    wishlist_item = Wishlist.objects.filter(product=product, user=request.user)
    if wishlist_item.exists():
        wishlist_item.delete()
    return redirect('core:wishlist')
