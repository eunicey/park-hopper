from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

TYPES = (
  ('T', 'Trail'),
  ('S', 'Scenic Drive'),
  ('C', 'Camp'),
  ('V', 'Viewpoints'),
)

class Park(models.Model):
  name = models.CharField(max_length = 100)
  state = models.CharField('State (abbreviation)', max_length = 2)
  year_visited = models.IntegerField('If visited, what year', blank = True, null = True)
  highlights = models.TextField(max_length = 250, blank = True, null = True)
  user = models.ForeignKey(User, on_delete=models.CASCADE)

  def __str__(self):
    return self.name
  
  def get_absolute_url(self):
    return reverse('park-detail', kwargs={'park_id': self.id})
  
  class Meta:
    ordering = ['-year_visited']

class Activity(models.Model):
  type = models.CharField(
    max_length = 1,
    choices = TYPES,
    default = TYPES[0][0]
  )
  description = models.CharField(max_length = 200)
  comments = models.TextField(max_length = 250, blank = True, null = True)

  park = models.ForeignKey(Park, on_delete = models.CASCADE)

  def __str__(self):
    return self.description
  
  class Meta:
    verbose_name_plural = 'activities'

class ActivityPhoto(models.Model):
  url = models.CharField(max_length=250)
  activity = models.OneToOneField(Activity, on_delete=models.CASCADE)

  def __str__(self):
    return f"Photo for activity_id: {self.activity_id} @{self.url}"

class ParkPhoto(models.Model):
  url = models.CharField(max_length=250)
  park = models.OneToOneField(Park, on_delete=models.CASCADE)

  def __str__(self):
    return f"Photo for park_id: {self.park_id} @{self.url}"