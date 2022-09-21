from datetime import datetime
from distutils.log import error
import random
from unicodedata import decimal
from django.shortcuts import redirect, render
from app.forms import ShippingDetailsForm, SupportQueryForm
from app.models import Account, Carousel, Category, Coupon, Order, OrderItem, Product, ProductImage, Address, ShippingDetails, TrackingNumber
from django.contrib.auth import authenticate, login, logout
defaultProductImage = "/media/categories/products/default.png"


def index_view(request):
    productsByCategory = []
    categories = Category.objects.all()
    for category in categories:
        products = []
        for product in Category.objects.get(id=category.id).products.all():
            image = defaultProductImage
            try:
                image = Product.objects.get(
                    id=product.id).images.first().image.url
            except:
                pass
            products.append({"product": product, "image": image})
        productsByCategory.append({"category": category, "products": products})
    context = {
        "Carousel": Carousel.objects.all(),
        "ProductsByCategory": productsByCategory
    }
    return render(request, 'index.html', context)


def login_view(request):
    if request.user.is_anonymous:
        formValues = {}
        formErrors = {}
        if request.method == "POST":
            try:
                del request.session['message']
            except:
                pass
            formValues['email'] = request.POST['email']
            formValues['password'] = request.POST['password']
            if formValues['email'] == "":
                formErrors['email'] = "Please enter your email address."
            elif len(formValues['email']) > 125:
                formErrors['email'] = "Your email address is invalid."
            if formValues['password'] == "":
                formErrors['password'] = "Please enter a password."
            elif len(formValues['password']) < 4 or len(formValues['password']) > 20:
                formErrors['password'] = "Your password is invalid."
            if len(formErrors) == 0:
                try:
                    email_search = Account.objects.get(
                        email=formValues['email'])
                    user = authenticate(
                        request, username=formValues['email'], password=formValues['password'])
                    if user is not None:
                        login(request, user)
                        return redirect('home')
                    else:
                        formErrors['email'] = 'Your password is incorrect.'
                except:
                    formErrors['email'] = "User with that email doesn't exist."
        context = {"formValues": formValues, "formErrors": formErrors,
                   "message": request.session.get('message') or ""}
        return render(request, 'pages/accounts/login.html', context)
    else:
        return redirect('home')


def register_view(request):
    if request.user.is_anonymous:
        day = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16,
               17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31]
        month = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                 "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        year = []
        gender = [
            {"id": "M", "name": "Male"},
            {"id": "F", "name": "Female"},
            {"id": "O", "name": "Other"}
        ]
        formValues = {}
        formErrors = {}
        currentyear = datetime.now().year
        for i in range(120):
            year.append(currentyear)
            currentyear -= 1
        if request.method == "POST":
            try:
                del request.session['message']
            except:
                pass
            formValues['first_name'] = request.POST['first_name'].capitalize()
            formValues['last_name'] = request.POST['last_name'].capitalize()
            formValues['email'] = request.POST['email']
            formValues['username'] = request.POST['username'].lower()
            formValues['password'] = request.POST['password']
            formValues['password2'] = request.POST['password2']
            formValues['day'] = int(request.POST['day'])
            formValues['month'] = int(request.POST['month'])
            formValues['year'] = int(request.POST['year'])
            formValues['gender'] = request.POST.get('gender', None)
            if formValues['first_name'] == "" and formValues['last_name'] == "":
                formErrors['names'] = "First and last names are required."
            elif formValues['first_name'] == "":
                formErrors['first_name'] = "First name is required."
            elif formValues['last_name'] == "":
                formErrors['last_name'] = "Last name is required."
            elif len(formValues['first_name']) > 20:
                formErrors['first_name'] = "First name must not exceed more than 20 characters."
            elif len(formValues['last_name']) > 20:
                formErrors['last_name'] = "Last name must not exceed more than 20 characters."
            if formValues['username'] == "":
                formErrors['username'] = "Username is a required field."
            elif not re.match("^[a-z0-9.]*$", formValues['username']):
                formErrors['username'] = "Ensure to use letters, numbers and period only"
            elif len(formValues['username']) < 4 or len(formValues['username']) > 20:
                formErrors['username'] = "Username must be between 4-20 characters."
            else:
                if len(Account.objects.filter(username=formValues['username'])) > 0:
                    formErrors['username'] = "User with that username already exists."
            if formValues['email'] == "":
                formErrors['email'] = "Email address is a required field."
            elif len(formValues['email']) > 125:
                formErrors['email'] = "Email must not exceed more than 125 characters."
            else:
                if len(Account.objects.filter(email=formValues['email'])) > 0:
                    formErrors['email'] = "User with that email already exists."
            if formValues['gender'] == None:
                formErrors['gender'] = "Please select your gender."
            if formValues['password'] == "":
                formErrors['password'] = "Please enter a password."
            elif len(formValues['password']) < 8 or len(formValues['password']) > 20:
                formErrors['password'] = "Password must be between 8-20 characters."
            elif formValues['password2'] == "":
                formErrors['password2'] = "Confirm your password."
            elif formValues['password2'] != formValues['password']:
                formErrors['password2'] = "Passwords do not match."
            try:
                x = datetime(formValues['year'],
                             formValues['month'], formValues['day'])
            except:
                formErrors['date_of_birth'] = "Enter valid date of birth."
            else:
                diff = datetime.now() - \
                    datetime(
                        formValues["year"], formValues["month"], formValues["day"], 0, 0)
                if diff.days < (365*5):
                    formErrors['date_of_birth'] = "Enter your real date of birth."
            if len(formErrors) == 0:
                user = Account.objects.create_user(
                    first_name=formValues['first_name'],
                    last_name=formValues['last_name'],
                    email=formValues['email'],
                    username=formValues['username'],
                    date_of_birth=f"{formValues['year']}-{formValues['month']}-{formValues['day']}",
                    gender=formValues['gender']
                )
                user.set_password(formValues['password'])
                user.save()
                login(request, user)
                return redirect("home")
        context = {"formValues": formValues, "day": day,
                   "month": month, "year": year, "formErrors": formErrors, "gender": gender}
        return render(request, 'pages/accounts/register.html', context)
    else:
        return redirect('home')


def logout_view(request):
    logout(request)
    return redirect('login')


def reset_view(request):
    context = {}
    return render(request, 'pages/accounts/reset.html', context)

def cost_calculator_view(request):
    cost_result = ''
    values = []
    try:
        if request.method == "POST":
            distance = eval(request.POST.get("distance"))
            weight =eval(request.POST.get("weight"))
            if weight < 0 or weight == 0:
                cost_result = "Weight should be at least greater than 0"
            elif distance < 0:
                cost_result = "Distance cannot be a negative number."
            elif distance == 0:
                cost_result = f'You have selected pick up method. Estimate cost is ${weight * 1 * .5}'
            else:
                cost_result = f'Estimate cost is ${distance * weight * .5}'
            values = [request.POST.get("pick"),request.POST.get("delivery"),request.POST.get("medium"), weight, distance]
    except:
        cost_result= "Fill in all the data first."
    print(values)
    return render(request, 'pages/cost_calculator.html', { 'values' : values, 'cost_result': cost_result})

def categories_view(request):
    context = {}
    return render(request, 'pages/products/categories.html', context)

def tracking(request):
    msg = None
    tracking_number = ''
    if request.method == "POST":
        tracking_number = request.POST['tracking-number']
        if tracking_number == '':
            msg = "Please enter your tracking number first."
        else:
            tracked_item = TrackingNumber.objects.filter(tracking_number = tracking_number).first()
            if tracked_item:
                msg = tracked_item.status
            else:
                msg = "This tracking is either invalid or not yet added to the system."
    return render(request, 'pages/tracking.html', {'msg': msg,'tracking_number':tracking_number})

def shipping(request):
    form = ShippingDetailsForm()
    if request.method == 'POST':
        form = ShippingDetailsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/thankyou")
        else:
            print('Something went wrong')
    return render(request, 'pages/shipping.html', {
        'form':form
    })

def thankyou(request):
    return render(request, "pages/thankyou.html")

def aboutus(request):
    return render(request, "pages/aboutus.html")

def support(request):
    form = SupportQueryForm()
    if request.method == 'POST':
        form = SupportQueryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/support/thankyou")
        else:
            print('Something went wrong')
    return render(request, "pages/support.html",{'form':form})

def thankyouSupport(request):
    return render(request, "pages/support_thankyou.html")

def category_view(request, category):
    context = {}
    return render(request, 'pages/products/category.html', context)


def product_view(request, productId):
    product = Product.objects.get(id=productId)
    order = []
    orderItem = []
    quantity = 0
    product_in_cart_message = None
    try:
        order = Order.objects.filter(user_id=request.user, paid_status=False)
        orderItem = OrderItem.objects.filter(order_id=Order.objects.get(
            user_id=request.user, paid_status=False), product_id=product)
    except:
        pass
    # if order exists already in cart.
    if len(orderItem) != 0:
        quantity = orderItem[0].quantity
        product_in_cart_message = "This product is in your cart."

    # image
    image = defaultProductImage
    images = product.images.all()
    try:
        image = images.first().image.url
    except:
        pass

    # post
    if request.user.is_authenticated:
        if 'addToCart' in request.POST:
            quantity = int(request.POST['quantity'])
            price = round(product.price-(product.discount/100)
                          * product.price, 2)
            if len(order) == 0:
                order = Order.objects.create(user_id=request.user,
                                             total_price=(price*quantity))
                OrderItem.objects.create(
                    order_id=order, product_id=product, price=price, quantity=quantity)
                product_in_cart_message = "Item is added to your cart."
            else:
                order_id = Order.objects.get(
                    user_id=request.user, paid_status=False)
                if len(orderItem) == 0:
                    OrderItem.objects.create(
                        order_id=order_id, product_id=product, price=price, quantity=quantity)
                    product_in_cart_message = "Item is added to your cart."
                else:
                    OrderItem.objects.filter(order_id=order_id, product_id=product).update(
                        price=price, quantity=quantity)
                    product_in_cart_message = "Cart is updated successfully"
    else:
        request.session['message'] = 'You have to login first to add products to cart.'
        return redirect('login')

    context = {
        "images": images,
        "image": image,
        "product": product,
        "quantity": quantity,
        "product_in_cart_message": product_in_cart_message
    }
    return render(request, 'pages/products/product.html', context)


def sales_view(request):
    context = {}
    return render(request, 'pages/products/sales.html', context)







# cartview------------------------------------------------------------------------------------------------------
def cart_view(request):
    orders = []
    cart = []
    couponError = ""
    couponSuccess = ""
    delivery_choice = "P"
    items = 0
    delivery = 0
    items_discount = 0
    total_price = 0
    coupon_discount = 0
    coupon_discount_num = 0
    if request.user.is_authenticated:
        # checking if order exists
        try:
            order = Order.objects.get(user_id=request.user, paid_status=False)
            try:
                coupon_discount_num = order.coupon.discount
            except:
                pass
            # if exists give me all order items
            cart = order.orders.all()
            # changing delivery choice to choosed one
            delivery_choice = order.delivery_choice
            # to get all orders
            for i in order.orders.all():
                productImage = Product.objects.filter(
                    id=i.product_id.id)[0].images.all()
                # checking if image exists for product
                try:
                    productImage = productImage.first().image.url
                except:
                    productImage = defaultProductImage
                # add all order items to orders list.
                orders.append({"id": i.id, "image": productImage, "name": i.product_id.name, "color": i.product_id.color,
                               "price": i.price, "stock": i.product_id.stock, "quantity": i.quantity})
        except:
            # if doesn't exists return empty list
            orders=[]
    # if delivery choice is submitted
    if 'button_delivery_choice' in request.POST:
        delivery_choice = request.POST['select_delivery_choice'] 
        Order.objects.filter(user_id = request.user, paid_status=False).update(delivery_choice=delivery_choice)
    # if coupon is applied
    elif 'button_coupon' in request.POST:
        input_coupon = request.POST['input_coupon']
        try:
            coupon = Coupon.objects.get(coupon = input_coupon)
            if coupon.expired == True:
                couponError = "This coupon code is expired."
                couponSuccess = ""
            else:
                Order.objects.filter(user_id = request.user, paid_status=False).update(coupon = coupon)
                coupon_discount_num = coupon.discount
                couponError = ""
                couponSuccess = "Coupon applied successfully"
        except:
            couponError = "Invalid Coupon"
            couponSuccess = ""
    # else update cart items individually
    elif 'updateProductItem' in request.POST:
        cart_order_id = request.POST['cart_order_id']
        cart_order_index = int(request.POST['cart_order_index'])
        quantity = int(request.POST['quantity'])
        orderItem = OrderItem.objects.filter(id=cart_order_id)
        if quantity == 0:
            orderItem.delete()
            orders.pop(cart_order_index-1)
        else:
            orderItem.update(quantity=quantity)
            orders[cart_order_index-1]['quantity'] = quantity

    try:
        for i in cart:
            items = items + (i.quantity * i.product_id.price)
            total_price = total_price + i.quantity*i.price
            items_discount = items - total_price

        coupon_discount = round(coupon_discount_num*0.01*float(total_price),2)
        # checking delivery choice
        if Order.objects.get(user_id=request.user, paid_status=False).delivery_choice == 'D':
            if total_price < 500:
                delivery = 10.99
            elif total_price < 1000:
                delivery = 5.99
            else:
                delivery = 0
        total_price = round(float(items - items_discount) - coupon_discount + delivery,2)
    except:
        print({"error":"order doesn't exist"})
    
    
    context = {
        "promocode": "SALES2022",
        "orders": orders,
        "delivery_choice": delivery_choice,
        "couponError": couponError,
        "couponSuccess":couponSuccess,
        "items":items,
        "delivery":delivery,
        "items_discount":items_discount,
        "coupon_discount":coupon_discount,
        'total_price':total_price,
    }
    return render(request, 'pages/shopping/cart.html', context)


def checkout_view(request):
    context = {}
    return render(request, 'pages/shopping/checkout.html', context)


def profile_view(request, username):
    orders = TrackingNumber.objects.filter(user=request.user)
    sidebar = [{"name": "Basic Info", "id":"basic-info","template": "includes/profileTabBasicInfo.html"},
               {"name": "Your Orders", "id":"your-orders", "template": "includes/profileTabYourOrders.html"},
               {"name": "Address Detail", "id":"address-detail", "template": "includes/profileTabAddressDetail.html"},
               {"name": "Login & Security", "id":"login-and-security", "template": "includes/profileTabLoginSecurity.html"}]
    context = {
        "sidebar": sidebar,
        "activeSidebar": sidebar[0],
        "addressDetail": Address.objects.filter(user_id = request.user).first(),
        "orders":orders
    }
    return render(request, 'pages/accounts/profile.html', context)