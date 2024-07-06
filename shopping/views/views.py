from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from shopping.forms import CommentForm, OrderForm, ProductForm
from shopping.models import Product, Comment, Category


def home_page(request, en_slug=None):
    search = request.GET.get('searching')
    filter_expensive = request.GET.get('expensive')
    filter_cheap = request.GET.get('cheap')

    hide_slug = request.GET.get('hide')
    update_slug = request.GET.get('update')
    delete_slug = request.GET.get('delete')
    unlock_all = request.GET.get('unlock_all')
    page_number = request.GET.get('page_num')

    categories = Category.objects.all()
    products = Product.objects.filter(Q(is_available=True)).exclude(Q(quantity=0))
    paginator = Paginator(products, 2)
    try:
        products = paginator.page(page_number)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    if en_slug:
        products = Product.objects.filter(Q(category__slug=en_slug) & Q(is_available=True)).exclude(Q(quantity=0))

    if search:
        products = Product.objects.filter(Q(name__icontains=search) & Q(is_available=True)).exclude(Q(quantity=0))

    if hide_slug:
        product = Product.objects.get(slug=hide_slug)
        product.is_available = False
        product.save()
        return redirect('index')

    if delete_slug:
        product = Product.objects.get(slug=delete_slug)
        product.delete()
        return redirect('index')

    if update_slug:
        return redirect("update_product/{en_slug}".format(en_slug=update_slug))

    if unlock_all:
        products = Product.objects.all()
        for product in products:
            product.is_available = True
            product.save()

        return redirect('index')

    if filter_expensive:
        products = products.order_by('-price')[:2]
    elif filter_cheap:
        products = products.order_by('price')[:2]

    context = {'products': products,
               'categories': categories,
               'page_range': products, }
    return render(request, 'shopping/home.html', context)


def detail_page(request, en_slug):
    product = get_object_or_404(Product, slug=en_slug)
    related_products = Product.objects.filter(Q(category=product.category) & Q(is_available=True)).exclude(
        Q(slug=en_slug) | Q(quantity=0))
    product_comments = Comment.objects.filter(Q(product=product) & Q(is_accessible=True))
    categories = Category.objects.all()

    context = {'product': product,
               'related_products': related_products,
               'product_comments': product_comments,
               'categories': categories}
    return render(request, 'shopping/detail.html', context)


def add_comment(request, en_slug):
    product = get_object_or_404(Product, slug=en_slug)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.product = product
            comment.save()
            return redirect('details', en_slug)
    else:
        form = CommentForm(request.GET)

    return render(request, 'shopping/detail.html', {'form': form, 'product': product})


def add_order(request, en_slug):
    product = get_object_or_404(Product, slug=en_slug)

    print(request.POST.get('quantity'))

    if product.quantity >= int(request.POST.get('quantity')):
        product.quantity -= int(request.POST.get('quantity'))
        product.save()
        changed_slug = product.slug
        if request.method == 'POST':
            form = OrderForm(request.POST)
            if form.is_valid():
                order = form.save(commit=False)
                order.product = product
                order.save()
                messages.success(request, 'Order successfully created🎉')
                return redirect('details', changed_slug)
    else:
        form = OrderForm(request.GET)
        messages.success(request, "Pls, Order less product❗")

    context = {'form': form,
               'product': product}

    return render(request, 'shopping/detail.html', context)


def add_product(request):
    form = ProductForm()

    if request.method == 'POST':
        form = ProductForm(request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return redirect('index')

    context = {'Form': form}
    return render(request, 'shopping/add_product.html', context)


def update_product(request, en_slug):
    print(1)
    product = Product.objects.get(slug=en_slug)
    form = ProductForm(instance=product)
    if request.method == 'POST':
        form = ProductForm(data=request.POST, files=request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('index')

    context = {'Form': form}

    return render(request, 'shopping/update_product.html', context)


def about_page(request):
    return render(request, 'about/about.html')

# thanks for checking
