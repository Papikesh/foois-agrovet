from .models import Cart

def cart_context(request):
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
        count = cart.total_items if cart else 0
    else:
        count = 0
    return {'cart_count': count}