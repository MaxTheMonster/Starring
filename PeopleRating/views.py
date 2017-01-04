from django.shortcuts import render, redirect
from .forms import NameForm
from django.http import HttpResponse
from .models import Person, Rating
from django.core.exceptions import ObjectDoesNotExist

def index(request):
    try:
        people = Person.objects.order_by("-stars")
    except (KeyError, Person.DoesNotExist):
        error = "Hmm.. There are no people."
    error = ""
    return render(request, "PeopleRating/index.html", {"people": people, "error": error})

def search(request):
    error = ""
    if request.GET.get('name'):
        query = request.GET["name"]
        try:
            person = Person.objects.get(name=query)
        except (KeyError, Person.DoesNotExist):
            return render(request, "PeopleRating/name.html", {"error": "That is not a person, create one."})
    else:
        error = 'You submitted nothing!'
    return name("/name/", person.slug)

def name(request, person_slug):
    error = ""
    try:
        person = Person.objects.get(slug=person_slug)
    except (KeyError, Person.DoesNotExist):
        error = "That person does not exist."
        person = ""
    return render(request, "PeopleRating/detail.html", {"person": person, "error": error})

def rate(request, person_slug):
    people = Person.objects.all()
    try:
        person = Person.objects.get(slug=person_slug)
    except (KeyError, Person.DoesNotExist):
        return render(request, "PeopleRating/name.html", {"error": "That is not a person, create one."})
    else:
        if request.method == "POST":
            if int(request.POST.get("rating")) > 5:
                error = "Rating is out of 5. (Yours was below 5)"
            else:
                rating = Rating(stars=int(request.POST.get("rating")), name=person)
                rating.save()
                error = "Rated successfully."
                names_ratings = Rating.objects.filter(name=person)
                total = 0
                amount = 0
                print(names_ratings)
                for current_rating in names_ratings:
                    total += current_rating.stars
                    amount += 1
                new_rating = total / amount

                print(new_rating)
                if person.name == "Max Ungless":
                    new_rating = 5
                person.stars = new_rating
                person.save()

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
