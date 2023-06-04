from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView

from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Park
from .forms import ActivityForm

class Home(LoginView):
  template_name = 'home.html'

def about(request):
  return render(request, 'about.html')

@login_required
def park_index(request):
  parks = Park.objects.filter(user=request.user)
  return render(request, 'parks/index.html', { 'parks': parks })

@login_required
def park_detail(request, park_id):
  park = Park.objects.get(id=park_id)
  activity_form = ActivityForm()
  return render(request, 'parks/detail.html', {
    'park': park,
    'activity_form': activity_form,
  })

@login_required
def add_activity(request, park_id):
  form = ActivityForm(request.POST)
  if form.is_valid():
    new_activity = form.save(commit=False)
    new_activity.park_id = park_id
    new_activity.save()
  return redirect('park-detail', park_id=park_id)

class ParkCreate(LoginRequiredMixin, CreateView):
  model = Park
  fields = ['name', 'state', 'year_visited', 'highlights']
  
  def form_valid(self, form):
    form.instance.user = self.request.user  
    return super().form_valid(form)

class ParkUpdate(LoginRequiredMixin, UpdateView):
  model = Park
  fields = ['name', 'state', 'year_visited', 'highlights']

class ParkDelete(LoginRequiredMixin, DeleteView):
  model = Park
  success_url = '/parks/'

def signup(request):
  error_message = ''
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request, user)
      return redirect('park-index')
    else:
      error_message = 'Invalid sign up - try again'

  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'signup.html', context)