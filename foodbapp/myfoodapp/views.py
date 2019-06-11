from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.views import generic, View
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .models import Question, Choice
from .forms import ConnexionForm, NewUserForm, SearchForm

# Create your views here.
class IndexView(View):
    template_name = 'myfoodapp/index.html'
    prodform = SearchForm

    def get(self, request):
        form = self.prodform
        return render(request, self.template_name, {'form': form})

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]

    def post(self, request):
        form = self.prodform(request.POST)
        if form.is_valid():
            # <process form cleaned data>
            return HttpResponseRedirect('/myfoodapp/connexion/')

        return render(request, self.template_name, {'form': form})



class DetailView(generic.DetailView):
    model = Question
    template_name = 'myfoodapp/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'myfoodapp/results.html'

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'myfoodapp/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('myfoodapp:results', args=(question.id,)))

def creation(request):
    errorusr = False
    erroremail = False

    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            email = form.cleaned_data["email"]
            if User.objects.filter(username=username).exists():
                errorusr = True
            if User.objects.filter(email=email).exists():
                erroremail = True
            else:
                newuser = User.objects.create_user(username, email, password, first_name=first_name, last_name=last_name)
                if not newuser:  # Si l'objet renvoyé n'est pas None
                    error = True
    else:
        form = NewUserForm()
    
    return render(request, 'myfoodapp/creation.html', locals())

def connexion(request):
    error = False

    if request.method == "POST":
        form = ConnexionForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(username=username, password=password)  # Nous vérifions si les données sont correctes
            if user:  # Si l'objet renvoyé n'est pas None
                login(request, user)  # nous connectons l'utilisateur
            else: # sinon une erreur sera affichée
                error = True
    else:
        form = ConnexionForm()

    return render(request, 'myfoodapp/connexion.html', locals())

def deconnexion(request):
    logout(request)
    return redirect(reverse('myfoodapp:connexion'))

class CompteView(generic.ListView):
    model = User
    template_name = 'myfoodapp/compte.html'
