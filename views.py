from io import BytesIO
from django.contrib.auth import logout as auth_logout
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from .admin import ProductModelAdmin
import razorpay
from django.contrib.auth.decorators import login_required
from urllib.parse import urlparse, parse_qs
from django.contrib.auth import views as auth_view

from . models import Customer, OrderPlaced, Payment, Product, Cart, Wishlist
from . forms import CustomerProfileForm, CustomerRegistrationForm, ProductForm
from django.contrib import messages
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist

from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from .models import Feedback, OrderPlaced

# Create your views here.

@login_required
def getWishlist(request):
    return len(Cart.objects.filter(user=request.user)), len(Wishlist.objects.filter(user=request.user))

# (Cart.objects.filter(isDeleted=False).filter(user=request.user)

@login_required
def home(request):
    #---------
    print('result = ',request.user)
    #---------
    # For the Authentication with showing the cart items
    if request.user.is_authenticated:
        totalitem, wishitem = getWishlist(request)
    return render(request, "app/home.html", locals())

@login_required
def about(request):

    # For the Authentication with showing the cart items
    if request.user.is_authenticated:
        totalitem, wishitem = getWishlist(request)

    return render(request, "app/about.html", locals())

@login_required
def contact(request):

    # For the Authentication with showing the cart items
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))

    return render(request, "app/contact.html", locals())

@method_decorator(login_required,name="dispatch")
class CategoryView(View):
    def get(self, request, val):

         # For the Authentication with showing the cart items
        if request.user.is_authenticated:
            totalitem, wishitem = getWishlist(request)

        product = Product.objects.filter(category=val)
        title = Product.objects.filter(category=val).values('title')
        return render(request, 'app/category.html', locals())

# This is for the individual the search for the product

@method_decorator(login_required,name="dispatch")
class CategoryTitle(View):
    def get(self, request, val):

        # For the Authentication with showing the cart items
        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Wishlist.objects.filter(user=request.user))

        product = Product.objects.filter(category=val)
        title = Product.objects.filter(
            category=product[0].category).values('title')
        return render(request, 'app/category.html', locals())

@method_decorator(login_required,name="dispatch")
class ProductDetail(View):
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        print('result = ',request.user)
        wishlist = Wishlist.objects.filter(
            Q(product=product) & Q(user=request.user))

        # For the Authentication with showing the cart items
        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Wishlist.objects.filter(user=request.user))

        return render(request, "app/productdetail.html", locals())


class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()

        # For the Authentication with showing the cart items
        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Wishlist.objects.filter(user=request.user))

        return render(request, 'app/customerregistration.html', locals())

    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request, "Congratulation! User Registration Successfully!")
        else:
            messages.warning(request, "Invalid Input Data! ")
        return render(request, 'app/customerregistration.html', locals())


@method_decorator(login_required,name="dispatch")
class ProfileView(View):
    def get(self, request):
        form = CustomerProfileForm()

        # For the Authentication with showing the cart items
        totalitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))

        return render(request, 'app/profile.html', locals())

    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            mobile = form.cleaned_data['mobile']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']

            reg = Customer(user=user, name=name, locality=locality,
                           mobile=mobile, city=city, state=state, zipcode=zipcode)
            reg.save()
            messages.success(
                request, "Congratulation! User Registration Successfully!")
        else:
            messages.warning(request, "Invalid Input Data! ")

        return render(request, 'app/profile.html', locals())


@login_required
def address(request):
    add = Customer.objects.filter(user=request.user)

    # For the Authentication with showing the cart items
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))

    return render(request, 'app/address.html', locals())

# for used to updating the update the address using class UpdateAddress

@method_decorator(login_required,name="dispatch")
class updateAddress(View):
    def get(self, request, pk):
        add = Customer.objects.get(pk=pk)
        # according to using the instance get update and add the information
        form = CustomerProfileForm(instance=add)

        # For the Authentication with showing the cart items
        totalitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))

        return render(request, "app/updateAddress.html", locals())

    def post(self, request, pk):
        form = CustomerProfileForm(request.POST)
        # return render(request,"app/updateAddress.html",locals())
        if form.is_valid():
            add = Customer.objects.get(pk=pk)
            add.name = form.cleaned_data['name']
            add.locality = form.cleaned_data['locality']
            add.city = form.cleaned_data['city']
            add.mobile = form.cleaned_data['mobile']
            add.state = form.cleaned_data['state']
            add.zipcode = form.cleaned_data['zipcode']
            add.save()
            messages.success(
                request, "Congratulation! User Registration Successfully!")
        else:
            messages.warning(request, "Invalid Input Data! ")
        return redirect("address")

# def add_to_cart(request):
#     # pass
#     user = request.user
#     product_id = request.GET.get('prod_id')
#     product = Product.objects.get(id=product_id)
#     Cart(user=user,product=product).save()
#     # return redirect("/cart")
#     num = 5
#     return render(request,'app/test.html',{'num':num})

@login_required
def add_to_cart(request):
    # pass
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    try:
        prod = Cart.objects.filter(product=product).get()
        prod.quantity += 1
        prod.save()
    except Exception as e:
        Cart(user=user, product=product).save()
    return redirect("/cart")


@login_required
def show_cart(request):
    user = request.user
    cart = Cart.objects.filter(user=user)
    amount = 0
    for p in cart:
        value = p.quantity * p.product.discounted_price
        amount = amount + value
    totalamount = amount + 40

    # For the Authentication with showing the cart items

    if request.user.is_authenticated:
        totalitem, wishitem = getWishlist(request)

    return render(request, "app/addtocart.html", locals())

# Note:--This is chekout connected prices with item and users

@method_decorator(login_required,name="dispatch")
class checkout(View):
    def get(self, request):

        # For the Authentication with showing the cart items

        if request.user.is_authenticated:
            totalitem, wishitem = getWishlist(request)

        user = request.user
        add = Customer.objects.filter(user=user)
        cart_items = Cart.objects.filter(user=user)
        famount = 0
        for p in cart_items:
            value = p.quantity * p.product.discounted_price
            famount = famount + value
        totalamount = famount + 40
        razoramount = int(totalamount * 100)
        client = razorpay.Client(
            auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
        data = {"amount": razoramount, "currency": "INR",
                "receipt": "order_rcptid_12"}
        payment_responce = client.order.create(data=data)
        # print(payment_responce)
        # {'id': 'order_LY7TGZp5zw5kIC', 'entity': 'order', 'amount': 29000, 'amount_paid': 0, 'amount_due': 29000, 'currency': 'INR', 'receipt': 'order_rcptid_12', 'offer_id': None, 'status': 'created', 'attempts': 0, 'notes': [], 'created_at': 1680263094}

        order_id = payment_responce['id']
        order_status = payment_responce['status']
        if order_status == 'created':
            payment = Payment(
                user=user,
                amount=totalamount,
                razorpay_order_id=order_id,
                razorpay_payment_status=order_status
            )
            payment.save()
        return render(request, 'app/checkout.html', locals())

# url = 'http://localhost:8000/paymentdone/?order_id=order_LYVcd5K2uLFLNN&payment_id=pay_LYVd5UNlPhvyzE&cust_id=2'

# parsed_url = urlparse(url)
# params = parse_qs(parsed_url.query)

# order_id = params.get('order_id', [None])[0]
# payment_id = params.get('payment_id', [None])[0]
# cust_id = params.get('cust_id', [None])[0]

# if None in [order_id, payment_id, cust_id]:
#     print('Error: Missing parameters')
# else:
#     print(f'order_id: {order_id}')
#     print(f'payment_id: {payment_id}')
#     print(f'cust_id: {cust_id}')


# Payment done with respect to using the razorpay
# @login_required(login_url = 'login')
@login_required
def payment_done(request):
    # print(request.GET)
    order_id = request.GET.get('order_id')
    payment_id = request.GET.get('payment_id')
    cust_id = request.GET.get('cust_id')
    # print("payment_done : oid = ",order_id,"pid = ",payment_id," cid = ",cust_id)
    user = request.user
    # return redirect("orders")
    customer = Customer.objects.get(id=cust_id)

    # To Update Payment status and Payment_id
    payment = Payment.objects.get(razorpay_order_id=order_id)

    # customer = get_object_or_404(Customer, id=cust_id)
    # payment = get_object_or_404(Payment, razorpay_order_id=order_id)

    payment.paid = True
    payment.razorpay_payment_id = payment_id
    payment.save()

    # To save order Details
    cart = Cart.objects.filter(user=user.id)
    for c in cart:
        OrderPlaced(user=user, customer=customer, product=c.product,
                    quantity=c.quantity, payment=payment).save()
        c.delete()
    return redirect("orders")


@login_required
def orders(request):

    # For the Authentication with showing the cart items
    if request.user.is_authenticated:
        totalitem, wishitem = getWishlist(request)

    order_placed = OrderPlaced.objects.filter(
        user=request.user.id).filter(isDeleted=False)
    return render(request, 'app/orders.html', locals())

# def orders(request):
#     order_placed = OrderPlaced.objects.filter(user=request.user)
#     context = {'order_placed': order_placed}
#     return render(request, 'app/orders.html', context)

# Adding to Plus cart to card

@login_required
def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        print('prod_id',prod_id)
        try:
            c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
            c.quantity += 1
            c.save()
        except ObjectDoesNotExist:
            # If Cart object does not exist, create a new one
            product = Product.objects.get(id=prod_id)
            c = Cart.objects.create(
                product=product, quantity=1, user=request.user)

        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        # print(prod_id)
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount + value
            totalamount = amount + 40
        data = {
            'quantity': c.quantity,
            'amount': amount,
            'totalamount': totalamount
        }
        return JsonResponse(data)


# Substracting to Minus cart to card
@login_required
def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity -= 1
        c.save()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        # print(prod_id)
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount + value
            totalamount = amount + 40
        data = {
            'quantity': c.quantity,
            'amount': amount,
            'totalamount': totalamount
        }
        return JsonResponse(data)

@login_required
def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()

        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        # print(prod_id)
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount + value
        totalamount = amount + 40
        data = {
            'amount': amount,
            'totalamount': totalamount
        }
        return JsonResponse(data)

@login_required
def plus_wishlist(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        product = Product.objects.get(id=prod_id)
        user = request.user
        Wishlist(user=user, product=product).save()
        data = {
            'message': 'Wishlist Added Successfully'
        }

        return JsonResponse(data)

@login_required
def minus_wishlist(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        product = Product.objects.get(id=prod_id)
        user = request.user
        Wishlist.objects.filter(user=user, product=product).delete()
        data = {
            'message': 'Wishlist Remove Successfully'
        }

        return JsonResponse(data)

@login_required
def logout(request):
    auth_logout(request)
    o = OrderPlaced.objects.all()
    for i, j in enumerate(o):
        o[i].isDeleted = True
    OrderPlaced.objects.bulk_update(o, ['isDeleted'])
    return redirect('/accounts/login/')


#-------------show the wishlist item--------
def show_wishlist(request):
        # For the Authentication with showing the cart items
    user = request.user    
    if request.user.is_authenticated:
        totalitem, wishitem = getWishlist(request)

    product = Wishlist.objects.filter(user=user)
    print('product id :',product[0].product.id)
    return render(request, 'app/wishlist.html', locals())


#------------------------------------

#--------------------------------new type
# For creating the search bar:--

def search(request):
    if request.method == 'POST':
        query = request.POST.get('search')
    if request.method == 'GET':
        query = request.GET['Search']

    # For the Authentication with showing the cart items

    if request.user.is_authenticated:
        totalitem, wishitem = getWishlist(request)

    # if  else   check the product are product=None with deleted
    if query is not None:
        product = Product.objects.filter(Q(title__contains=query))
    else:
        product = None
    context = {'product':product , 'query':query}
    # context.update(locals())
    return render(request, "app/search.html", context)




#-----------2nd Search Bar code------------------
# @login_required
# def search(request):
#     query = request.GET.get('search',None)

#     # For the Authentication with showing the cart items

#     if request.user.is_authenticated:
#         totalitem, wishitem = getWishlist(request)

    # if  else   check the product are product=None with deleted
    # if query is not None:
    #     product = Product.objects.filter(Q(title__contains=query))
    # else:
    #     product = None
    # context = {'product':product , 'query':query}
    # # context.update(locals())
    # return render(request, "app/search.html", context)
#-------------------------------------------------------------


#--------------------------------Feedback form-------------------------------

def feedback_form(request, pk):
    order_placed = get_object_or_404(OrderPlaced, pk=pk)

    if request.method == 'POST':
        form = FeedbackForm(request.POST)

        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.user = request.user
            feedback.order_placed = order_placed
            feedback.save()
            return redirect('orders')

    else:
        form = FeedbackForm()

    return render(request, 'app/feedback_form.html', {'form': form})

#------------------------------------feedback end form------------------------------
# For the creating the Generating the PDF OF THE KOT:--
@login_required
def generate_pdf(request, pk): 
    order = OrderPlaced.objects.filter(user_id=pk).all()
    customer = order[0].user.username
    # items = order.items.all()
    items = [i.product.title for i in order]

    # user = request.user
    # cart = Cart.objects.filter(user=user)
    # amount = 0
    # # print(prod_id)
    # for p in cart:
    #     value = p.quantity * p.product.discounted_price
    #     amount = amount + value
    #     totalamount = amount + 40
    #     data = {
    #         'amount': amount,
    #         'totalamount': totalamount
    #     }

    context = {
        'order': order,
        'customer': customer,
        'items': items,
        # 'amount': amount,
        # 'totalamount': totalamount,
        # 'data':data,
    }
    template = get_template('app/order_pdf.html')
    html = template.render(context)
    pdf = render_to_pdf('app/order_pdf.html', context)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = f'order_{order[0].pk}.pdf'
        content = f'attachment; filename={filename}'
        response['Content-Disposition'] = content
        return response
    return HttpResponse('Error generating PDF')

@login_required
def render_to_pdf(template_path, context):
    template = get_template(template_path)
    html = template.render(context)
    pdf = get_bytes(html)
    return pdf


def get_bytes(html):
    html = html.encode('UTF-8')
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html), result)
    if not pdf.err:
        return result.getvalue()
    return None


# Create views here

def Pro(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                return redirect('/show')
            except:
                pass
        else:
            form = ProductForm()
            return render(request,'index.html',{'form':form})
        

def show(request):
    Product = Product.objects.all()
    return render(request,"show.html",{'product':ProductModelAdmin})

def edit(request,id):
    product = Product.objects.get(id = id)
    form = ProductForm(request.POST,instance = product)
    if form.is_valid():
        form.save()
        return redirect("/show")
    return render(request,"edit.html",{'product':product})

def update(request, id):  
    product = Product.objects.get(id=id)  
    form = ProductForm(request.POST, instance = product)  
    if form.is_valid():  
        form.save()  
        return redirect("/show")  
    return render(request, 'edit.html', {'employee': product})  

def destroy(request,id):
    product = Product.objects.get(id = id)
    product.delete()
    return redirect("/show")
