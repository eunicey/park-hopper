from django.contrib import admin
from .models import Park, Activity, ActivityPhoto, ParkPhoto, NPS

admin.site.register(NPS)
admin.site.register(Park)
admin.site.register(Activity)
admin.site.register(ActivityPhoto)
admin.site.register(ParkPhoto)
