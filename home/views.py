from django.contrib import messages
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .forms import SearchForm

from .models import Setting, ContactForm, ContactMessage

from product.models import Category

from product.models import Product


def index(request):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    products_slider = Product.objects.all().order_by('id')[:4]  # первые 4 продукта / first 4 products
    products_latest = Product.objects.all().order_by('-id')[:4]  # последние 4 продукта / latest 4 products
    products_picked = Product.objects.all().order_by('?')[:4]  # случайные 4 продукта / random 4 products
    page = 'home'
    context = {'setting': setting,
               'page': page,
               'category': category,
               'products_slider': products_slider,
               'products_latest': products_latest,
               'products_picked': products_picked,
               }
    return render(request, 'home/index.html', context)

def about(request):
    setting = Setting.objects.get(pk=1)
    context = {'setting': setting}
    return render(request, 'home/about.html', context)

def contactus(request):
    if request.method == 'POST':  # проверить POST запрос / check POST
        form = ContactForm(request.POST)
        if form.is_valid(): # проверить валдацию формы / check validation form
            data = ContactMessage() # создать связь с моделью / creae relation with model
            data.name = form.cleaned_data['name']  # получить данные из форм / get form input data
            data.email = form.cleaned_data['email']
            data.subject = form.cleaned_data['subject']
            data.message = form.cleaned_data['message']
            data.ip = request.META.get('REMOTE_ADDR')
            data.save() # сохранить данные / save data to table
            messages.success(request, 'We would response soon')
            return HttpResponseRedirect('/contact')

    setting = Setting.objects.get(pk=1)
    form = ContactForm
    context = {'setting': setting, 'form': form}
    return render(request, 'home/contact.html', context)

def category_products(request, id, slug):
    category = Category.objects.all()
    products = Product.objects.filter(category_id=id)
    context = {
               'category': category,
               'products': products,
               }
    return render(request, 'home/category_products.html', context)

def search(request):
    if request.method == 'POST': # check post
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query'] # get form input data
            catid = form.cleaned_data['catid']
            if catid==0:
                products=Product.objects.filter(title__icontains=query)  #SELECT * FROM product WHERE title LIKE '%query%'
            else:
                products = Product.objects.filter(title__icontains=query,category_id=catid)

            category = Category.objects.all()
            context = {'products': products, 'query':query,
                       'category': category }
            return render(request, 'home/search_products.html', context)

    return HttpResponseRedirect('/')


