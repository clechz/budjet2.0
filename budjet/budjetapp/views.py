from django.shortcuts import render, HttpResponse, HttpResponseRedirect, redirect
from .main.app import CSV
from .main.data import CATEGORIES, get_date
def index(request):
    if request.method == "GET":
        categories = CATEGORIES.values
        print(categories)
        return render(request, "index.html", {"categories": categories})

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
        CSV.add(date, amount, category, description)
        return redirect("/")