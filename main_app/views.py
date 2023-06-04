from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Park, ParkPhoto, ActivityPhoto
from .forms import ActivityForm

import uuid
import boto3

S3_BASE_URL = 'https://s3.us-east-2.amazonaws.com/'
BUCKET = 'park-hopper-2023'

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

def add_park_photo(request, park_id):
  photo_file = request.FILES.get('photo-file', None)
  if photo_file:
    s3 = boto3.client('s3')
    key = uuid.uuid4().hex + photo_file.name[photo_file.name.rfind('.'):]

    try:
      s3.upload_fileobj(photo_file, BUCKET, key)
      url = f"{S3_BASE_URL}{BUCKET}/{key}"
      photo = ParkPhoto(url=url, park_id=park_id)
      park_photo = ParkPhoto.objects.filter(park_id=park_id)
      if park_photo.first():
        park_photo.first().delete()
      photo.save()
    except Exception as err:
      print('An error occurred uploading file to S3: %s' % err)
  return redirect('park-detail', park_id=park_id)

# def add_activity_photo(request, activity_id, park_id):
#   photo_file = request.FILES.get('photo-file', None)
#   if photo_file:
#     s3 = boto3.client('s3')
#     key = uuid.uuid4().hex + photo_file.name[photo_file.name.rfind('.'):]

#     try:
#       s3.upload_fileobj(photo_file, BUCKET, key)
#       url = f"{S3_BASE_URL}{BUCKET}/{key}"
#       photo = ActivityPhoto(url=url, activity_id=activity_id)
#       activity_photo = ActivityPhoto.objects.filter(activity_id=activity_id)
#       if activity_photo.first():
#         activity_photo.first().delete()
#       photo.save()
#     except Exception as err:
#       print('An error occurred uploading file to S3: %s' % err)
#   return redirect('park-detail', park_id=park_id)