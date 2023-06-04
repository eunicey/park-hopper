from django.contrib import admin
from .models import Park, Activity, ParkPhoto, ActivityPhoto

admin.site.register(Park)
admin.site.register(Activity)
admin.site.register(ParkPhoto)
admin.site.register(ActivityPhoto)
