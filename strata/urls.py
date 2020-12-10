from django.urls import path
from . import views

app_name = 'strata'
urlpatterns = [
    path('create', views.CharacterCreateView.as_view(), name='create'),
    path('edit/<int:pk>', views.CharacterEditView.as_view(), name='edit'),
    path('', views.CharacterListView.as_view(), name='list'),
]
