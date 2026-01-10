from django.urls import path
from . import views
urlpatterns = [
    path('find/', views.start_search, name='find_match'), # Kept name='find_match' for compatibility
    path('waiting/', views.waiting_page, name='waiting_page'), 
    path('check-status/', views.check_match_status, name = 'check_match_status'), 
    path('directory/', views.user_directory, name = 'user_directory'), 
    path('request/<str:username>/', views.send_call_request, name='send_call_request'),
    path('inbox/', views.inbox, name='inbox'),
    path('handle/<int:request_id>/<str:action>/', views.handle_request, name='handle_request'),
    path('cancel-search/', views.cancel_search, name='cancel_search'),
    path('check-request-status/', views.check_request_status, name='check_request_status'),
]