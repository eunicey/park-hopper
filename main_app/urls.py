from django.urls import path
from . import views

urlpatterns = [
  path('', views.Home.as_view(), name='home'),
  path('about/', views.about, name='about'),
  path('index/', views.get_parks, name='get-parks'),
  path('parks/', views.park_index, name='park-index'),
  path('accounts/signup/', views.signup, name='signup'),

  path('parks/<int:park_id>/', views.park_detail, name='park-detail'),
  path('parks/<int:park_id>/add-activity/', views.add_activity, name='add-activity'),
  path('parks/<int:park_id>/add-photo/', views.add_park_photo, name='add-park-photo'),
  path('parks/<int:park_id>/<int:activity_id>/add-photo/', views.add_activity_photo, name='add-activity-photo'),

  path('parks/<int:pk>/create/', views.ParkCreate.as_view(), name='park-create'),
  path('parks/<int:pk>/update/', views.ParkUpdate.as_view(), name='park-update'),
  path('parks/<int:pk>/delete/', views.ParkDelete.as_view(), name='park-delete'), 
]