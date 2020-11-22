from django.urls import path


from . import views
from .views import *

urlpatterns = [
	#Leave as empty string for base url

	path('', homeView.as_view(), name="home"),
	path('basic/', views.basic, name="basic"),
	path('shop/', views.shop, name="shop"),
	path('register/', views.register, name="register"),
	path('loginpage/', views.loginpage, name="loginpage"),
	path('search/', views.search, name="search"),
    path('logoutPage/', views.logoutPage, name="logoutPage"),
	path('checkout/',CheckoutView.as_view(), name="checkout"),
	path('order-summary/', OrderSummaryView.as_view(), name="order-summary"),
	path('product_detail/<slug>',productDetailView.as_view(), name="product"),
	path('add-to-cart/<slug>',add_to_cart, name="add-to-cart"),
	path('remove-from-cart/<slug>',remove_from_cart, name="remove-from-cart"),
	path('remove_single_item_from_cart/<slug>',remove_single_item_from_cart, name="remove_single_item_from_cart"),
    path('payment/', views.payment, name="payment"),
    path('sample/', views.sample, name="sample"),


]