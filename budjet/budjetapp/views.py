from django.shortcuts import render, HttpResponse, HttpResponseRedirect, redirect
from .main.app import CSV
from .main.data import CATEGORIES, get_date
from functools import wraps
from .helpers import *

def index(request):
    if request.method == "GET":
        return render(request, "index.html")
    else:
        redirect("")

def add(request):
    session_required(request)
    categories = CATEGORIES.values
    
    if request.method == "GET":
        
        print(categories)
        return render(request, "add.html", {"categories": categories})

    elif request.method == "POST":
        # Retrieve form data using request.POST.get
        date = get_date(request.POST.get('dateInput'), allow_default=True)
        date = request.POST.get('dateInput')
        amount = request.POST.get('amountInput')
        category = request.POST.get('categoryInput')
        description = request.POST.get('descriptionInput')
        

        # #ensures there is a dict already
        CSV.init_csv()
        print("adding...")
        print("Form data retrieved:")
        print(f"Date: {date}")
        print(f"Amount: {amount}")
        print(f"Category: {category}")
        print(f"Description: {description}")
        print(f"session: {request.session.session_key}")
        CSV.add(date, amount, category, description, session_key=request.session.session_key)
        return render(request, "add.html", {"categories": categories, "alert": "success"})
    
def transactions(request):
    session_required(request)
    if request.method == "GET":
        rows = CSV.read(request.session.session_key)
        print("columns", CSV.columns)
        return render(request, "transactions.html", {"rows": rows, "columns": CSV.columns[:-1]})
    else:
        redirect("/")