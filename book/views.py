from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from django.contrib.auth import login, logout, authenticate
from .forms import *


# Create your views here.
def home(request):
    books = Book.objects.all()
    context = {"books": books}
    if request.user.is_staff:
        return render(request, "book/home.html", context)
    else:
        return render(request, "book/home.html", context)


def logoutPage(request):
    logout(request)
    return redirect("/")


def loginPage(request):
    if request.user.is_authenticated:
        return redirect("home")
    else:
        if request.method == "POST":
            username = request.POST.get("username")
            password = request.POST.get("password")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                print("working")
                login(request, user)
                return redirect("/")
        context = {}
        return render(request, "book/login.html", context)


def registerPage(request):
    if request.user.is_authenticated:
        return redirect("home")
    else:
        form = createuserform()
        cust_form = createcustomerform()
        if request.method == "POST":
            form = createuserform(request.POST)
            cust_form = createcustomerform(request.POST)
            if form.is_valid() and cust_form.is_valid():
                user = form.save()
                customer = cust_form.save(commit=False)
                customer.user = user
                customer.save()
                return redirect("login")
        context = {
            "form": form,
            "cust_form": cust_form,
        }
        return render(request, "book/register.html", context)


def addbook(request):
    form = createbookform()
    if request.method == "POST":
        form = createbookform(request.POST)
        if form.is_valid():
            form.save()
        return redirect("/")

    context = {"form": form}
    return render(request, "book/addbook.html", context)


def viewcart(request):
    cust = Customer.objects.filter(user=request.user)
    for c in cust:
        carts = Cart.objects.all()
        for cart in carts:
            if cart.customer == c:
                context = {"cart": cart}
                return render(request, "book/viewcart.html", context)
        else:
            return render(request, "book/emptycart.html")


def addtocart(request, pk):
    book = Book.objects.get(id=pk)
    cust = Customer.objects.filter(user=request.user)

    for c in cust:
        carts = Cart.objects.all()
        reqcart = ""
        for cart in carts:
            if cart.customer == c:
                reqcart = cart
                break
        if reqcart == "":
            reqcart = Cart.objects.create(
                customer=c,
            )
        reqcart.books.add(book)
    return redirect("/")
