from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseForbidden

from .models import Park, ActivityPhoto, ParkPhoto
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

def get_parks():
  res = requests.get('https://developer.nps.gov/api/v1/parks?q=%22National%20Park%22&api_key=DUURkH3ztXkcEgB3aYFydtxJyyTtgt7GPFPr3reT&limit=200')
  data = res.json()

  # filter out everything that is not a national park
  park_data = list(filter(lambda park: park.get('designation') == "National Park", data["data"]))

  # create tupes of park code, park name and park code, park iage url
  parkNames, parkImages = ([] for i in range(2))
  for idx, park in enumerate(park_data):
    parkNames.append((park['parkCode'], park['fullName']+', '+park['states']))
    parkImages.append((park['parkCode'], park['images'][0]['url']))
  parkNames = tuple(parkNames)
  parkImages = tuple(parkImages)
  
  return parkNames, parkImages

@login_required
def park_index(request):
  parks = Park.objects.filter(user=request.user)
  return render(request, 'parks/index.html', { 'parks': parks })


@login_required
def park_detail(request, park_id):
  park = Park.objects.get(id=park_id)
  activity_form = ActivityForm()

  if not park.user == request.user:
    return HttpResponseForbidden('Forbidden!')
  
  return render(request, 'parks/detail.html', {
    'park': park,
    'activity_form': activity_form,
  })


@login_required
def add_activity_photo(request, park_id, activity_id):
  photo_file = request.FILES.get('photo-file', None)
  if photo_file:
    s3 = boto3.client('s3')
    key = uuid.uuid4().hex + photo_file.name[photo_file.name.rfind('.'):]

    try:
      s3.upload_fileobj(photo_file, BUCKET, key)
      url = f"{S3_BASE_URL}{BUCKET}/{key}"
      photo = ActivityPhoto(url=url, activity_id=activity_id)
      activity_photo = ActivityPhoto.objects.filter(activity_id=activity_id)
      if activity_photo.first():
        activity_photo.first().delete()
      photo.save()
    except Exception as err:
      print('An error occurred uploading file to S3: %s' % err)


@login_required
def add_activity(request, park_id):
  form = ActivityForm(request.POST)
  if form.is_valid():
    new_activity = form.save(commit=False)
    new_activity.park_id = park_id
    new_activity.save()
    add_activity_photo(request, park_id=park_id, activity_id=new_activity.id)
  return redirect('park-detail', park_id=park_id)


@login_required
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


# class ParkCreate(LoginRequiredMixin, CreateView):
#   model = Park
#   fields = ['name', 'state', 'year_visited', 'highlights']
  
#   def form_valid(self, form):
#     form.instance.user = self.request.user
#     new_park = form.save()
#     add_park_photo(self.request, new_park.id)
#     return super().form_valid(form)

class ParkCreate(LoginRequiredMixin, CreateView):
  model = Park
  fields = ['name', 'year_visited', 'highlights', 'url']

  # def get_form(self):
  #   form = super().get_form()
  #   parkNames, parkImages = get_parks()
  #   print(parkImages)
  #   form.fields['name'].choices = parkNames
  #   return form
  
  def form_valid(self, form):
    form.instance.user = self.request.user
    new_park = form.save()
    print(new_park.name)

    # 
    # add_park_photo(self.request, new_park.id, new_park.name)
    return super().form_valid(form)

class ParkUpdate(LoginRequiredMixin, UserPassesTestMixin,  UpdateView):
  model = Park
  fields = ['name', 'year_visited', 'highlights', 'url']

  def form_valid(self, form):
    add_park_photo(self.request, self.kwargs['pk'])
    return super().form_valid(form)
  
  def test_func(self):
    park = self.get_object()
    return self.request.user == park.user


class ParkDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
  model = Park
  success_url = '/parks/'

  def test_func(self):
    park = self.get_object()
    return self.request.user == park.user


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