from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='listings'),
    path('<int:listing_id>', views.listing, name='listing'),
    path('search', views.search, name='search'),
    path('add_listing', views.NewListingView.as_view(), name='add_listing'),
    path('delete/<int:listing_id>', views.delete, name='delete'),
    path('delete_contact/<int:contact_id>', views.delete_contact, name='delete_contact'),
    path('listOnDash/<int:listing_id>', views.listing_on_dashboard, name='listOnDash'),
    path('deploying/<int:listing_id>', views.get_deploying, name='deploying'),
    path('get_pay/<int:listing>', views.get_pay, name='get_pay'),
    path('get_terminated/<int:listing>', views.get_terminated, name='terminated'),
    path('user_actions/<int:listing>', views.get_user_actions, name='user_actions'),

]
