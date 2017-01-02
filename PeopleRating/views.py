from django.shortcuts import render, redirect
from .forms import NameForm
from .models import Person, Rating
from django.core.exceptions import ObjectDoesNotExist

def index(request):
    people = Person.objects.all()
    return render(request, "PeopleRating/index.html", {"people": people})

def rate(request, person_slug):
    try:
        person = Person.objects.get(slug=person_slug)
    except (KeyError, Person.DoesNotExist):
        return render(request, "PeopleRating/new_name.html", {"error": "That is not a person, create one."})
    else:
        if request.method == "POST":
            Rating.save(stars=request.POST.get("rating"), name=person.name)
    return redirect("/")

def new_name(request):
    error = ""
    if request.method == 'POST':
        form = NameForm(request.POST)

        if form.is_valid():
            num_results = Person.objects.filter(name=form.cleaned_data['name']).exists()
            if num_results:
                error = "A person with that name already exists."
            else:
                form.save(commit=True)
                return redirect("/")
        else:
            error = form.errors
    else:
        form = NameForm()

    return render(request, 'PeopleRating/name.html', {'form': form, "error": error})
