from django.shortcuts import render,get_object_or_404,redirect
from .models import *
from django.views.generic import ListView,DetailView,View
from django.utils import timezone
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from.forms import CheckoutForm,CreateUserForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import UserCreationForm
# Create your views here.


def loginpage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        # else:
        #   messages.info(request,'Username or password is incorrect')

    context = {}
    return render(request, 'store/login.html', context)


def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account was create ,please login here')
                return redirect('loginpage')

        context = {'form': form}
        return render(request, 'store/register.html', context)

def logoutPage(request):
    logout(request)
    return redirect('home')

def payment(request):
    order = Order.objects.get(user=request.user, ordered=False)
    context = {
         'object': order
    }

    return render(request,'store/payment.html',context)

class homeView(ListView):
    model = Item

    template_name = 'store/index.html'





class productDetailView(DetailView):
    model = Item
    template_name = 'store/product-detail.html'



class OrderSummaryView(LoginRequiredMixin,View):
    def get(self,*args, **kwargs):
        try:
            order = Order.objects.get(user = self.request.user,ordered=False)
            context ={'object':order}
            return render(self.request,'store/shoping-cart.html',context)
        except ObjectDoesNotExist:
            messages.error(self.request,"You do not have an active order")
            return redirect("/")



def search(request):
    query = request.GET.get('search')
    search_item = Item.objects.filter(title__contains =query)

    context = {'search_item':search_item}
    return render(request, 'store/search.html', context)

def basic(request):


    context = { }
    return render(request, 'store/basic.html', context)

class CheckoutView(View):
    def get(self,*args,**kwargs):
        form = CheckoutForm()
        order = Order.objects.get(user=self.request.user, ordered=False)
        context = {
            'form':form,'object': order
        }
        return render(self.request, 'store/checkout.html',context)

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        try:
            order = Order.objects.get(user = self.request.user,ordered=False)

        except ObjectDoesNotExist:
            messages.error(self.request,"You do not have an active order")
            return redirect("order-summary")

        if form.is_valid():
            address = form.cleaned_data.get('address')
            city = form.cleaned_data.get('city')
            state = form.cleaned_data.get('state')

            zip = form.cleaned_data.get('zip')
            same_billing_address = form.cleaned_data.get('same_billing_address')
            save_info = form.cleaned_data.get('save_info')
            payment_option = form.cleaned_data.get('payment_option')
            billing_addreess = BillingAddress(
                user=self.request.user,
                address=address,
            city = city,
            zip = zip,
            state = state
            )
            billing_addreess.save()
            return redirect('payment')
        return redirect('payment')





def shop(request):


    context = {
        'item':Item.objects.all()

    }
    return render(request, 'store/shop.html', context)




@login_required(login_url='loginpage')
def add_to_cart(request,slug):
    item = get_object_or_404(Item,slug=slug)
    order_item, created = OrderItem.objects.get_or_create(item = item,
                                                 user=request.user,
                                                 ordered=False)
    order_qs = Order.objects.filter(user=request.user,ordered=False)
    if order_qs.exists():
        order =order_qs[0]
        if order.items.filter(item__slug = item.slug).exists():
            order_item.quantity +=1
            order_item.save()
            messages.info(request, "Item is added to your cart ")
        else:
            order.items.add(order_item)
            messages.info(request, "This item is added to your cart")
            return redirect("checkout")

    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user= request.user,ordered_date =ordered_date)
        order.items.add(order_item)
        messages.info(request, "This item quantity is updated ")
    return redirect("checkout")


@login_required(login_url='loginpage')
def remove_from_cart(request,slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(item = item,
                                                 user=request.user,
                                                 ordered=False)[0]
            order.items.remove(order_item)
            messages.info(request, "This item  is removed from your cart ")
            return redirect("product", slug=slug)
        else:
            messages.info(request, "This item was not in  your cart ")
            return redirect("product", slug=slug)

    else:
        messages.info(request, "You do not have an active order ")
        return redirect("product", slug=slug)



@login_required(login_url='loginpage')
def remove_single_item_from_cart(request,slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(item = item,
                                                 user=request.user,
                                                 ordered=False)[0]
            order_item.quantity -= 1
            order_item.save()

            messages.info(request, "This item quantity was updated ")
            return redirect("order-summary")
        else:
            messages.info(request, "This item was not in  your cart ")
            return redirect("product", slug=slug)

    else:
        messages.info(request, "You do not have an active order ")
        return redirect("product", slug=slug)

def sample(request):
    return render(request,'store/sample.html')