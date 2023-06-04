from django.urls import path
from . import views

urlpatterns = [
  path('', views.home, name='home'),
  path('about/', views.about, name='about'),
  path('parks/', views.park_index, name='park-index'),
  path('parks/<int:park_id>/', views.park_detail, name='park-detail'),
  path('parks/create/', views.ParkCreate.as_view(), name='park-create'),
  path('parks/<int:pk>/update/', views.ParkUpdate.as_view(), name='park-update'),
  path('parks/<int:pk>/delete/', views.ParkDelete.as_view(), name='park-delete'),
]