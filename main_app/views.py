from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from .models import Park
from .forms import ActivityForm

def home(request):
  return render(request, 'home.html')

def about(request):
  return render(request, 'about.html')

def park_index(request):
  parks = Park.objects.all()
  return render(request, 'parks/index.html', { 'parks': parks })

def park_detail(request, park_id):
  park = Park.objects.get(id=park_id)
  activity_form = ActivityForm()
  return render(request, 'parks/detail.html', {
    'park': park,
    'activity_form': activity_form,
  })

def add_activity(request, park_id):
  form = ActivityForm(request.POST)
  if form.is_valid():
    new_activity = form.save(commit=False)
    new_activity.park_id = park_id
    new_activity.save()
  return redirect('park-detail', park_id=park_id)

class ParkCreate(CreateView):
  model = Park
  fields = '__all__'

class ParkUpdate(UpdateView):
  model = Park
  fields = '__all__'

class ParkDelete(DeleteView):
  model = Park
  success_url = '/parks/'
