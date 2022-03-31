from django.urls import path

from . import views 

urlpatterns = [
    path('<int:listing>', views.get_contact, name='contact')
]