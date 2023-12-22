from django.views.generic import ListView, DetailView, TemplateView
from .models import Product, Cart, CartItem
from django.shortcuts import render, get_object_or_404, redirect
from .forms import AddToCartForm
from django.db import transaction
from django.contrib import messages
from django.contrib.auth.decorators import login_required

class StoreListView(ListView):
    model = Product
    template_name = 'base.html'
class ProductListView(ListView):
    model = Product
    template_name = 'product_list.html'
    context_object_name = 'products'

class ProductDetailView(DetailView):
    model = Product
    template_name = 'product_detail.html'

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'store/product_detail.html', {'product': product})

class AboutView(TemplateView):
    template_name = 'about.html'

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)

    if request.method == 'POST':
        form = AddToCartForm(request.POST)
        if form.is_valid():
            cart_item.quantity += form.cleaned_data['quantity']
            cart_item.save()
            success_message = f'{product.name} успішно додані в корзину.'
            cart.update_total()
            return render(request, 'add_to_cart.html', {'form': form, 'success_message': success_message})
    else:
        form = AddToCartForm()

    return render(request, 'add_to_cart.html', {'form': form})
@login_required
def view_cart(request):
    cart = get_object_or_404(Cart, user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)

    return render(request, 'view_cart.html', {'cart_items': cart_items})


@transaction.atomic
def buy_items(request):
    cart = get_object_or_404(Cart, user=request.user)
    cart_items = cart.cartitem_set.all()

    if cart_items.exists():

        cart_items.delete()
        cart.update_total()
        messages.success(request, f'Товари успішно куплені!')

        return redirect('product_list')


    messages.warning(request, 'Корзина пуста. ')

    return redirect('view_cart')