from django.urls import path, include
from core.views import index, product_list_view, category_list_view, \
    category_product_list_view, product_detail_view, tag_list, ajax_add_review,\
    search_view, add_to_cart, cart_view, checkout_view, delete_item_from_cart, update_items_cart, payment_completed_view, payment_failed_view, \
    response, profile_view, address_view,  order_history_view, track_order_view, contact_view
app_name= 'core'

urlpatterns=[
    path("",index, name='index'),
    path("products/",product_list_view, name="product-list"),
    path("category/", category_list_view, name="category-list"),
    path("category/<cid>/",category_product_list_view,name="category-product-list"), 
    path("product/<pid>/",product_detail_view , name="product-detail" ),
    path("products/tag/<slug:tag_slug>/", tag_list, name="tags"),
    path("ajax-add-review/<pid>/",ajax_add_review, name="ajax-add-review"),
    path("search/",search_view,name="search"),
    path("add-to-cart/",add_to_cart, name="add-to-cart"),
    path("cart/", cart_view, name="cart"),
    path("delete-from-cart/", delete_item_from_cart, name="delete-from-cart"),
    path("checkout/", checkout_view, name="checkout"),
    path('response/', response, name='response'),
    path("update-items-cart/", update_items_cart , name="update-items-cart"),
    path("paypal/", include("paypal.standard.ipn.urls")),
    path("payment-completed/", payment_completed_view , name="payment-completed"),
    path("payment-failed/", payment_failed_view, name="payment-failed"),
    path("profile/",profile_view,name='profile'),
    path("address/",address_view,name='address'),
    path("order_history/", order_history_view, name='order_history'),
    path("track_order/", track_order_view, name='track_order'),
    path("contact/",contact_view, name='contact')
]