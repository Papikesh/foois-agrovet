# orders/views.py
import urllib.parse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from products.models import Product
from .models import Cart, CartItem, Order, OrderItem
from django.http import JsonResponse


@login_required
def add_to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk, is_active=True)
    cart, _ = Cart.objects.get_or_create(user=request.user)

    if not product.in_stock:
        return JsonResponse({'success': False, 'message': f"{product.name} is out of stock."}, status=400)

    item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        item.quantity += 1
    item.save()

    return JsonResponse({
        'success': True,
        'message': f"{product.name} added to cart!",
        'cart_count': cart.total_items,
    })


@login_required
def cart_view(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    return render(request, 'orders/cart.html', {'cart': cart})


@login_required
def update_cart_item(request, item_id):
    item = get_object_or_404(CartItem, pk=item_id, cart__user=request.user)
    action = request.POST.get('action')

    if action == 'increase':
        item.quantity += 1
        item.save()
    elif action == 'decrease':
        item.quantity -= 1
        if item.quantity <= 0:
            item.delete()
        else:
            item.save()

    return redirect('orders:cart')


@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, pk=item_id, cart__user=request.user)
    item.delete()
    messages.info(request, "Item removed from cart.")
    return redirect('orders:cart')


@login_required
def checkout(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)

    if not cart.items.exists():
        messages.warning(request, "Your cart is empty.")
        return redirect('orders:cart')

    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        phone_number = request.POST.get('phone_number')
        delivery_address = request.POST.get('delivery_address', '')

        order = Order.objects.create(
            user=request.user,
            full_name=full_name,
            phone_number=phone_number,
            delivery_address=delivery_address,
        )

        message_lines = [f"New Order #{order.id}", f"Name: {full_name}", f"Phone: {phone_number}"]
        if delivery_address:
            message_lines.append(f"Address: {delivery_address}")
        message_lines.append("")
        message_lines.append("Items:")

        for cart_item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity,
                price_at_order=cart_item.product.price,
            )
            message_lines.append(f"- {cart_item.product.name} x{cart_item.quantity} = ₦{cart_item.subtotal}")

        message_lines.append("")
        message_lines.append(f"Total: ₦{order.total_price}")

        whatsapp_message = urllib.parse.quote("\n".join(message_lines))
        cart.items.all().delete()

        whatsapp_url = f"https://wa.me/{settings.ADMIN_WHATSAPP_NUMBER}?text={whatsapp_message}"
        return redirect(whatsapp_url)

    return render(request, 'orders/checkout.html', {'cart': cart})