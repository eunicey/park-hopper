from django.shortcuts import render
from .models import Park

def home(request):
  return render(request, 'home.html')

def about(request):
  return render(request, 'about.html')

def park_index(request):
  parks = Park.objects.all()
  return render(request, 'parks/index.html', { 'parks': parks })

def park_detail(request, park_id):
  park = Park.objects.get(id=park_id)
  return render(request, 'parks/detail.html', {'park': park})