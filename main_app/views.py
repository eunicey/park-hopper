from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse

from .models import Park, Photo
from .forms import ActivityForm

import uuid
import boto3
import requests

S3_BASE_URL = 'https://s3.us-east-2.amazonaws.com/'
BUCKET = 'park-hopper-2023'

class Home(LoginView):
  template_name = 'home.html'

def about(request):
  return render(request, 'about.html')

def park_api(request):
  res = requests.get('https://developer.nps.gov/api/v1/parks?q=%22National%20Park%22&api_key=DUURkH3ztXkcEgB3aYFydtxJyyTtgt7GPFPr3reT&limit=200')
  data = res.json()

  park_data = list(filter(lambda park: park.get('designation') == "National Park", data["data"]))

  def keep_items(pair):
    wanted_keys = ['fullName', 'parkCode', 'states', 'images']
    key, value = pair
    if key in wanted_keys:
      return True
    else:
      return False
  
  clean_park_data = [dict(filter(keep_items, park.items())) for park in park_data]
  # for park in data["data"]:
  #   print(park["fullName"])
  return render(request, 'temp.html', {'data': clean_park_data})

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
def add_photo(request, park_id, activity_id):
  photo_file = request.FILES.get('photo-file', None)
  if photo_file:
    s3 = boto3.client('s3')
    key = uuid.uuid4().hex + photo_file.name[photo_file.name.rfind('.'):]

    try:
      s3.upload_fileobj(photo_file, BUCKET, key)
      url = f"{S3_BASE_URL}{BUCKET}/{key}"
      photo = Photo(url=url, activity_id=activity_id)
      park_photo = Photo.objects.filter(activity_id=activity_id)
      if park_photo.first():
        park_photo.first().delete()
      photo.save()
    except Exception as err:
      print('An error occurred uploading file to S3: %s' % err)
  return redirect('park-detail', park_id=park_id)

@login_required
def add_activity(request, park_id):
  form = ActivityForm(request.POST)
  if form.is_valid():
    new_activity = form.save(commit=False)
    new_activity.park_id = park_id
    new_activity.save()
  return add_photo(request, park_id=park_id, activity_id=new_activity.id)


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

