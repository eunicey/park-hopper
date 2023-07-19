from django.urls import path
from . import views

urlpatterns = [
  path('', views.Home.as_view(), name='home'),
  path('about/', views.about, name='about'),
  path('parks/', views.park_index, name='park-index'),
  path('parks/all', views.get_parks, name='get_parks'),
  # path('parks/<int:park_id>/redirect', views.park_redirect, name='park-redirect'),
  path('accounts/signup/', views.signup, name='signup'),

  path('favorites/<int:park_id>/', views.park_detail, name='park-detail'),
  path('favorites/<int:park_id>/add-activity/', views.add_activity, name='add-activity'),
  path('favorites/<int:park_id>/add-photo/', views.add_park_photo, name='add-park-photo'),
  path('favorites/<int:park_id>/<int:activity_id>/add-photo/', views.add_activity_photo, name='add-activity-photo'),

  path('parks/<int:pk>/create/', views.ParkCreate.as_view(), name='park-create'),
  path('favorites/<int:pk>/update/', views.ParkUpdate.as_view(), name='park-update'),
  path('favorites/<int:pk>/delete/', views.ParkDelete.as_view(), name='park-delete'), 
]