from decimal import Decimal
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.db.models import Sum, F, DecimalField, ExpressionWrapper
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from .models import Product, Client, Sale, SaleDetail
from .forms import ProductForm, ClientForm, AddItemForm, CustomUserCreationForm
import json

# Helpers de Carrito
CART_KEY = "cart"

def cart_get(request):
    return request.session.get(CART_KEY, {"client_id": None, "items": []})

def cart_save(request, cart):
    request.session[CART_KEY] = cart
    request.session.modified = True

# Register
def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()

            return render(request, "registration/register_success.html")
    else:
        form = CustomUserCreationForm()

    return render(request, "registration/register.html", {"form": form})

# Home
@login_required
def home(request):
    monto_expr = ExpressionWrapper(
        F('quantity') * F('product__price'),
        output_field=DecimalField(max_digits=14, decimal_places=2)
    )
    kpi_total_monto = SaleDetail.objects.aggregate(total=Sum(monto_expr))['total'] or 0
    kpi_items_vendidos = SaleDetail.objects.aggregate(q=Sum('quantity'))['q'] or 0
    kpi_clientes_activos = Sale.objects.values('client_id').distinct().count()
    kpi_ventas = Sale.objects.count()
    kpi_productos = Product.objects.count()

    productos = (
        SaleDetail.objects
        .values('product__name')
        .annotate(total_vendido=Sum('quantity'))
        .order_by('-total_vendido')[:5]
    )
    clientes = (
        Sale.objects
        .values('client__name')
        .annotate(total_items=Sum('details__quantity'))
        .order_by('-total_items')[:5]
    )

    ctx = {
        'kpi_total_monto': kpi_total_monto,
        'kpi_items_vendidos': kpi_items_vendidos,
        'kpi_clientes_activos': kpi_clientes_activos,
        'kpi_ventas': kpi_ventas,
        'kpi_productos': kpi_productos,
        'productos_json': json.dumps(list(productos)),
        'clientes_json': json.dumps(list(clientes)),
        'has_prod': len(productos) > 0,
        'has_cli': len(clientes) > 0,
    }
    return render(request, 'catalog/home.html', ctx)

# Productos y Clientes
@login_required
def product_list(request):
    products = Product.objects.all()
    return render(request, 'catalog/product_list.html', {'products': products})

@login_required
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto creado correctamente.')
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'catalog/product_form.html', {'form': form})

@login_required
def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto actualizado.')
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'catalog/product_form.html', {'form': form})

@login_required
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == "POST":
        product.delete()
        messages.success(request, "Producto eliminado correctamente.")
        return redirect('product_list')

    return render(request, 'catalog/confirm_delete.html', {
        'title': 'Eliminar producto',
        'obj': product.name,
    })

@login_required
def client_list(request):
    clients = Client.objects.all()
    return render(request, 'catalog/client_list.html', {'clients': clients})

@login_required
def client_create(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cliente creado correctamente.')
            return redirect('client_list')
    else:
        form = ClientForm()
    return render(request, 'catalog/client_form.html', {'form': form})

@login_required
def client_edit(request, pk):
    client = get_object_or_404(Client, pk=pk)
    if request.method == 'POST':
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cliente actualizado.')
            return redirect('client_list')
    else:
        form = ClientForm(instance=client)
    return render(request, 'catalog/client_form.html', {'form': form})

@login_required
def client_delete(request, pk):
    client = get_object_or_404(Client, pk=pk)

    if request.method == "POST":
        client.delete()
        messages.success(request, "Cliente eliminado correctamente.")
        return redirect('client_list')

    return render(request, 'catalog/confirm_delete.html', {
        'title': 'Eliminar cliente',
        'obj': client.name,
    })

# Ventas (Flujo con carrito)
@login_required
def sale_list(request):
    sales = Sale.objects.all().select_related('client').order_by('-id')
    return render(request, 'catalog/sale_list.html', {'sales': sales})

@login_required
def sale_delete(request, pk):
    sale = get_object_or_404(Sale, pk=pk)

    if request.method == "POST":
        sale.delete()
        messages.success(request, "Venta eliminada correctamente.")
        return redirect('sale_list')

    return render(request, 'catalog/confirm_delete.html', {
        'title': 'Eliminar venta',
        'obj': f"Venta #{sale.id}",
    })

@login_required
def sale_start(request):
    if request.method == 'POST':
        client_id = request.POST.get('client_id')
        if not client_id:
            messages.error(request, 'Selecciona un cliente válido.')
            return redirect('sale_start')
        cart = {"client_id": int(client_id), "items": []}
        cart_save(request, cart)
        messages.success(request, 'Cliente seleccionado, ahora puedes agregar productos.')
        return redirect('sale_cart')
    clients = Client.objects.all()
    return render(request, 'catalog/sale_start.html', {'clients': clients})

@login_required
def sale_cart(request):
    cart = cart_get(request)
    if not cart["client_id"]:
        messages.info(request, "Primero selecciona un cliente.")
        return redirect("sale_start")

    add_form = AddItemForm(request.POST or None)
    if request.method == "POST" and add_form.is_valid():
        p = add_form.cleaned_data["product"]
        q = int(add_form.cleaned_data["quantity"])
        cart["items"].append({
            "product_id": p.id,
            "name": p.name,
            "price": str(p.price),
            "quantity": q
        })
        cart_save(request, cart)
        messages.success(request, f"Agregado: {p.name} x{q}")
        return redirect("sale_cart")

    items = []
    total = Decimal("0")
    for idx, it in enumerate(cart["items"]):
        price = Decimal(it["price"])
        qty = int(it["quantity"])
        sub = price * qty
        total += sub
        items.append({
            "index": idx,
            "name": it["name"],
            "price": price,
            "quantity": qty,
            "subtotal": sub
        })

    ctx = {
        "client": get_object_or_404(Client, pk=cart["client_id"]),
        "add_form": add_form,
        "items": items,
        "total": total,
    }
    return render(request, "catalog/sale_cart.html", ctx)

@login_required
def sale_item_remove(request, index):
    if request.method != "POST":
        messages.error(request, "Método no permitido.")
        return redirect("sale_cart")
    cart = cart_get(request)
    try:
        cart["items"].pop(index)
        cart_save(request, cart)
        messages.info(request, "Producto eliminado del carrito.")
    except IndexError:
        messages.error(request, "Ítem no encontrado en el carrito.")
    return redirect("sale_cart")

@login_required
@transaction.atomic
def sale_confirm(request):
    if request.method != "POST":
        messages.error(request, "Método no permitido.")
        return redirect("sale_cart")

    cart = cart_get(request)
    if not cart["items"]:
        messages.error(request, "No hay ítems para confirmar.")
        return redirect("sale_cart")

    client = get_object_or_404(Client, pk=cart["client_id"])
    sale = Sale.objects.create(client=client)

    for it in cart["items"]:
        product = get_object_or_404(Product, pk=it["product_id"])
        SaleDetail.objects.create(
            sale=sale,
            product=product,
            quantity=int(it["quantity"])
            # unit_price eliminado para coincidir con tu modelo actual
        )

    request.session[CART_KEY] = {"client_id": None, "items": []}
    request.session.modified = True
    messages.success(request, f"Venta #{sale.id} confirmada correctamente.")
    return redirect("sale_list")

def sale_cancel(request):
    request.session[CART_KEY] = {"client_id": None, "items": []}
    request.session.modified = True
    messages.info(request, "Venta cancelada.")
    return redirect("sale_list")

def sale_edit(request, sale_id):
    sale = get_object_or_404(Sale.objects.select_related('client'), pk=sale_id)

    add_form = AddItemForm(request.POST or None)
    if request.method == "POST" and add_form.is_valid():
        p = add_form.cleaned_data["product"]
        q = int(add_form.cleaned_data["quantity"])
        SaleDetail.objects.create(sale=sale, product=p, quantity=q)
        messages.success(request, f"Agregado: {p.name} x{q}")
        return redirect("sale_edit", sale_id=sale.id)

    details = (
        sale.details.select_related("product")
        .annotate(
            line_total=ExpressionWrapper(
                F("quantity") * F("product__price"),
                output_field=DecimalField(max_digits=14, decimal_places=2),
            )
        )
        .order_by("id")
    )

    total = sum(d.line_total for d in details)

    ctx = {
        "sale": sale,
        "details": details,
        "add_form": add_form,
        "total": total,
    }
    return render(request, "catalog/sale_edit.html", ctx)

@login_required
@require_POST
def sale_detail_delete(request, sale_id, detail_id):
    sale = get_object_or_404(Sale, pk=sale_id)
    detail = get_object_or_404(SaleDetail, pk=detail_id, sale=sale)
    detail.delete()
    messages.info(request, "Ítem eliminado de la venta.")
    return redirect("sale_edit", sale_id=sale.id)
