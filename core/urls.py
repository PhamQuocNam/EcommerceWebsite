from django.urls import path, include
from core.views import (
    index, product_list_view, category_list_view,
    category_product_list_view, product_detail_view, tag_list,
    ajax_add_review, search_view, add_to_cart, cart_view, checkout_view,
    delete_item_from_cart, update_items_cart, payment_completed_view,
    payment_failed_view, response, profile_view, address_view,
    order_history_view, track_order_view, contact_view, change_password_view,
    place_order_completed, order_management, revenue_management,
    staff_management, inventory_management, customer_orders,
    update_order_status, order_stats, add_employee, update_employee,
    delete_employee, update_payroll_for_staff,add_to_wishlist,
    wishlist_view,remove_from_wishlist, create_product, update_product,
    remove_product, cancel, find_order, order_cancellation
    
)

app_name = 'core'

urlpatterns = [

    # ------------------ Public Pages ------------------ #
    path("", index, name='index'),  # Home page
    path("products/", product_list_view, name="product-list"),  # List of all products
    path("product/<pid>/", product_detail_view, name="product-detail"),  # Product detail view
    path("category/", category_list_view, name="category-list"),  # All categories
    path("category/<cid>/", category_product_list_view, name="category-product-list"),  # Products by category
    path("products/tag/<slug:tag_slug>/", tag_list, name="tags"),  # Products by tag
    path("search/", search_view, name="search"),  # Search results
    path("contact/", contact_view, name='contact'),  # Contact page
    

    # ------------------ Product Review ------------------ #
    path("ajax-add-review/<pid>/", ajax_add_review, name="ajax-add-review"),  # Add a product review (AJAX)
    

    # ------------------ Cart & Checkout ------------------ #
    path("add-to-cart/", add_to_cart, name="add-to-cart"),  # Add item to cart (AJAX or POST)
    path("cart/", cart_view, name="cart"),  # Cart overview
    path("delete-from-cart/", delete_item_from_cart, name="delete-from-cart"),  # Remove item from cart
    path("update-items-cart/", update_items_cart, name="update-items-cart"),  # Update item quantity in cart
    path("checkout/", checkout_view, name="checkout"),  # Checkout page
    path("place_order_completed/", place_order_completed, name='place_order_completed'),  # Final order confirmation
    

    # ------------------ Payment Integration ------------------ #
    path("paypal/", include("paypal.standard.ipn.urls")),  # PayPal IPN callback URLs
    path("response/", response, name='response'),  # General payment response handler
    path("payment-completed/", payment_completed_view, name="payment-completed"),  # Payment success
    path("payment-failed/", payment_failed_view, name="payment-failed"),  # Payment failure
    

    # ------------------ User Profile & Orders ------------------ #
    path("profile/", profile_view, name='profile'),  # User profile page
    path("address/", address_view, name='address'),  # Manage delivery address
    path("order_history/", order_history_view, name='order_history'),  # User's order history
    path("track_order/", track_order_view, name='track_order'),  # Track order by ID or reference
    path("change_password/", change_password_view, name='change_password'),  # Change user password
    path("cancel/", cancel ,name = 'cancel'),  # return & cancellation
    path("find_order/", find_order, name= 'find_order'),
    path("order_cancellation/",order_cancellation, name='order_cancellation'),

    # ------------------ Admin & Management Views ------------------ #
    path("order_management/", order_management, name="order_management"),  # Admin: manage orders
    path("revenue_management/", revenue_management, name="revenue_management"),  # Admin: view revenue stats
    path("staff_management/", staff_management, name="staff_management"),  # Admin: manage staff
    path("inventory_management/", inventory_management, name="inventory_management"),  # Admin: inventory dashboard
    path("customer_orders/", customer_orders, name="customer_orders"),  # Admin: view customer orders
    path("<str:order_id>/status/", update_order_status, name="update_order_status"),  # Admin: update order status
    path("order-stats/", order_stats, name="order_stats"),  # Admin: visualize order data
    path('add_employee/', add_employee, name='add-employee'),
    path('update_employee/<str:employee_id>/', update_employee, name='update_employee'),
    path('delete_employee/<str:employee_id>/', delete_employee, name='delete_employee'),
    path('staff/<str:staff_id>/payroll/', update_payroll_for_staff, name='update_payroll_for_staff'),
    path('create_product/',create_product, name='create_product'),
    path('update_product/<product_id>/', update_product, name='update_product'),
    path('remove_product/<pid>/',remove_product, name='remove_product'),
    
    # ------------------ Wishlist ------------------ #
    path("add-to-wishlist/", add_to_wishlist, name="add-to-wishlist"),
    path('wishlist/', wishlist_view, name='wishlist'),
    path("wishlist/remove/<pid>/", remove_from_wishlist, name="remove-from-wishlist"),
]
