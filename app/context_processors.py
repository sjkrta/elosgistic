from .models import Order

def global_context(request):
    cart_length = 0

    if request.user.is_authenticated:
        try:
            cart = Order.objects.get(user_id=request.user, paid_status=False)
            for i in cart.orders.all():
                cart_length = cart_length + i.quantity
                if cart_length > 99:
                    cart_length = "99+"
        except:
            pass
    return{
        'cart_length':cart_length,
        "defaultProfileImage":"media/users/profile_pic.jpg",
    }