from django.urls import path
from . import views
app_name = 'support'

urlpatterns = [
  
    path('submit_claim/', views.submit_claim, name='submit_claim'),
    path('claimpage/', views.claimpage, name='claimpage'),
    path('adminside/',views.adminside,name='adminside'),
    path('client/', views.clientside,name='clientside'),
    path('update_claim_status/<int:claim_id>/', views.update_claim_status, name='update_claim_status'),
      path('claim/delete/<int:claim_id>/', views.delete_claim, name='delete_claim'), 
         path('claim/confirm/<int:claim_id>/', views.confirm_claim, name='confirm_claim'),
    path('claim/reject/<int:claim_id>/', views.reject_claim, name='reject_claim'),
     path('archived-claims/', views.archived_claims_list, name='archived_claims'),
    path('problems-list/', views.list_of_problems_view, name='problems_list'),
    path('archived-claims/update-cause/<int:archived_claim_id>/', views.update_cause, name='update_cause'),

    path('archived-claims/delete/<int:archived_claim_id>/', views.delete_archived_claim, name='delete_archived_claim'),
    path('about/',views.about,name='about'),
    
    path('users/', views.manage_users, name='manage_users'),
    path('users/update-role/<int:user_id>/', views.update_user_role, name='update_user_role'),
    path('users/delete/<int:user_id>/', views.delete_user, name='delete_user'),
    path('about1/', views.about1, name='about1'),
]