from django.contrib import admin
from .models import Park, Activity, ActivityPhoto, ParkPhoto

admin.site.register(Park)
admin.site.register(Activity)
admin.site.register(ActivityPhoto)
admin.site.register(ParkPhoto)
