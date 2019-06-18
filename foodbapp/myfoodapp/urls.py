from django.urls import path

from . import views

app_name = 'myfoodapp'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
    path('connexion/', views.connexion, name='connexion'),
    path('deconnexion/', views.deconnexion, name='deconnexion'),
    path('creation/', views.creation, name='creation'),
    path('compte/', views.CompteView.as_view(), name='compte'),
    path('populate/', views.PopulateView.as_view(), name='populate'),
    path('search/', views.SearchView.as_view(), name='search'),
    path('product/', views.ProductView.as_view(), name='product'),
]