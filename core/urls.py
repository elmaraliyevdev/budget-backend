from django.urls import path
from .views import *

urlpatterns = [
    path('login', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('register', register_user, name='register'),
    path('profile', get_user_profile, name='user_profile'),
    path('profile/update', update_user_profile, name='user_profile_update'),
    path('transactions', get_transactions, name='transactions'),
    path('grouped-transactions', get_grouped_transactions, name='grouped_transactions'),
    path('create-transaction', create_transaction, name='create_transaction'),
    path('categories', get_categories, name='categories'),
    path('create-category', create_category, name='create_category'),
    path('wallets', get_wallets, name='wallets'),
    path('create-wallet', create_wallet, name='create_wallet'),
]