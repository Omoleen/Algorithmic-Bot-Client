from django.urls import path
from wiseapp import views
# from django.conf.urls import handler500
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('register/', views.register, name='register'),
    path('login/', views.loginpage, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('profile/', views.profile_page, name='profile_page'),
    # path('profile/payment/', views.transactionpage, name='transaction_page'),
    path('login/otpverify/', views.verify, name='verification_page'),
    path('check_username/', views.check_username, name='check-username'),
    path('check_email/', views.check_email, name='check-email'),
    path('check_pass1/', views.check_password1, name='check-password1'),
    path('check_pass2/', views.check_password2, name='check-password2'),
    path('reset_password/', views.forgotpage, name='forgot-password'),
    path('referrals/', views.referral_page, name='referral-page'),
    path('transactions/', views.transactions, name='transactions-page'),
    path('walletbalance/', views.walletbalance, name='wallet'),
    path('referrals/transfer', views.transferwallet, name='transfer-page'),
    path('referrals/withdraw', views.withdrawal, name='withdrawal-page'),
    path('bot/on/', views.start_bot, name='start-bot'),
    path('bot/off/', views.stop_bot, name='stop-bot'),
    path('help/binance/', views.binance_tutorial, name='binance-tutorial'),
    path('blog/service-agreement/', views.service, name='service-agreement'),
    path('blog/privacy-policy/', views.privacy, name='privacy-policy'),
    path('profile/onload_check_payment/', views.load_check, name='profile-check-payment'),
    path('profile/change_password/', views.profile_change_password, name='profile-password'),
    path('profile/change_api/', views.profile_change_API, name='profile-api'),
    path('profile/activate_check/', views.activecheck, name='profile-activate-check'),
    path('profile/fuel_check/', views.fuelcheck, name='profile-fuel-check'),
    path('profile/check_bot/', views.checkbot, name='profile-check-bot'),
    path('profile/change_settings/', views.profile_change_settings, name='profile-settings'),
    path('generate_transaction/', views.generate_transaction, name='generate-transaction'),
    path('reset_password/<str:forgot_token>/', views.forgot_change_page, name='reset-password'),
    path('<str:ref_code>/', views.landing, name='landing'),
]

handler404 = 'wiseapp.views.error404'
handler403 = 'wiseapp.views.error403'
handler408 = 'wiseapp.views.error408'
# handler500 = 'wiseapp.views.error500'