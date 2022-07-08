
from django.urls import path

from link.views import RegForm, AuthForm, logou, StartPage, UserPage, DeleteLink, redirectPage

urlpatterns = [
    path('reg/', RegForm.as_view(), name='reg'),
    path('auth/', AuthForm.as_view(), name='auth'),
    path('logout/', logou, name='logou'),
    path('', StartPage.as_view()),
    path('user/<slug:slug>', UserPage.as_view(), name='start'),
    path('delete/<int:pk>/', DeleteLink.as_view(), name='link-delete'),
    path('<str:link>/', redirectPage, name='redirectpage')
]
