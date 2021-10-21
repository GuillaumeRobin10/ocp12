from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework_simplejwt import views as jwt_views
from . import views


urlpatterns = [
    path('login/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('signup/', views.Signup.as_view()),
    path('client/', views.ClientGeneral.as_view()),
    path('contrat/', views.ContratGeneral.as_view()),
    path('event/', views.EventGeneral.as_view()),
    path('client/<int:pk>/', views.ClientUnique.as_view()),
    path('contrat/<int:pk>/', views.ContratUnique.as_view()),
    path('event/<int:pk>/', views.EventUnique.as_view()),

]

urlpatterns = format_suffix_patterns(urlpatterns)