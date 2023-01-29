from django.urls import path,include
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
from .views import RegisterView,ProfileView,WalletView,ChangePasswordView,UserManagementView,LogoutView
from .transaction_view import *

urlpatterns = [
    path('register/',RegisterView.as_view(),name="register"),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='auth_logout'),
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),
    path('wallet/', WalletView.as_view(), name='wallet'),
    path('profile/', ProfileView.as_view({'get':'get_user_profile'}), name='profile'),
    path('profile-update/', ProfileView.as_view({'post':'update_user_profile'}), name='profile_update'),
    path('send-money/', TransactionView.as_view({'post':'send_money'}), name='send_money'),
    path('add-money/', TransactionView.as_view({'post':'add_money'}), name='add_money'),
    path('transaction-history/', TransactionView.as_view({'get':'history'}), name='history'),
    path('send-request/', RequestView.as_view({'post':'request_money'}), name='request_money'),
    path('request-history/', RequestView.as_view({'get':'history'}), name='req_history'),
    path('accept-request/<str:id>/', RequestView.as_view({'post':'accept_request'}), name='accept_request'),
    path('reject-request/<str:id>/', RequestView.as_view({'get':'reject_request'}), name='reject_request'),
    path('users-list/', UserManagementView.as_view({'get':'user_list'}), name='user_list'),
    path('user-details/<str:id>/', UserManagementView.as_view({'get':'user_details'}), name='user_details'),
    path('transaction-list/', UserManagementView.as_view({'get':'transaction_list'}), name='transaction_list'),
    path('transaction-details/<str:id>/', UserManagementView.as_view({'get':'transaction_details'}), name='transaction_details'),
    path('request-list/', UserManagementView.as_view({'get':'request_list'}), name='request_list'),
    path('request-details/<str:id>/', UserManagementView.as_view({'get':'request_details'}), name='request_details'),
    path('make-staff/<str:id>/', UserManagementView.as_view({'post':'make_staff'}), name='make_staff'),
    path('remove-staff/<str:id>/', UserManagementView.as_view({'post':'remove_staff'}), name='remove_staff'),

]
