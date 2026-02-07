from django.urls import path
from . import views
from . import views
from django.contrib.auth.views import (
    LogoutView, 
    PasswordResetView,
    PasswordResetDoneView, 
    PasswordResetConfirmView, 
    PasswordResetCompleteView
)
from django.urls import path, reverse_lazy

urlpatterns = [
    # Password Reset
    path('reset-password/', views.CustomPasswordResetView.as_view(), name='password_reset'),
    
    path('reset-password/done/', PasswordResetDoneView.as_view(
       template_name='registration/password_reset_done.html'
    ), name='password_reset_done'),
    
    path('reset-password/confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(
       template_name='registration/password_reset_confirm.html',
       success_url=reverse_lazy('password_reset_complete')
    ), name='password_reset_confirm'),
    
    path('reset-password/complete/', PasswordResetCompleteView.as_view(
       template_name='registration/password_reset_complete.html'
    ), name='password_reset_complete'),

    # Account Activation
    path('activate/<uidb64>/<token>/', views.activate_account, name='activate'),
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('registro/', views.registro_view, name='registro'),
    path('feed/', views.feed_view, name='feed'),
    path('siguiendo/', views.siguiendo_view, name='siguiendo'),
    path('busqueda/', views.busqueda_view, name='busqueda'),
    path('tools/', views.tools_view, name='tools'),
    
    # Cambiado de username a user_id para proteger privacidad
    path('perfil/<int:user_id>/', views.perfil_view, name='perfil'),
    path('editar-perfil/', views.editar_perfil_view, name='editar_perfil'),

    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),

    # Cambiado de username a user_id para proteger privacidad
    path('seguir/<int:user_id>/', views.seguir_toggle, name='seguir_toggle'),
    path('publicar/', views.crear_publicacion, name='crear_publicacion'),
    path('like/<int:pub_id>/', views.like_publicacion, name='like_publicacion'),
    path('dislike/<int:pub_id>/', views.dislike_publicacion, name='dislike_publicacion'),
    path('eliminar_publicacion/<int:id>/', views.eliminar_publicacion, name='eliminar_publicacion'),
    path('editar_publicacion/<int:id>/', views.editar_publicacion, name='editar_publicacion'),
    path('publicacion/<int:id>/', views.detalle_publicacion_view, name='detalle_publicacion'),
    path('comentar/<int:pub_id>/', views.crear_comentario, name='crear_comentario'),
    path('validate_rethus/', views.validate_rethus, name='validate_rethus'),
    path('eliminar_comentario/<int:com_id>/', views.eliminar_comentario, name='eliminar_comentario'),
    path('chat-api/', views.chat_proxy_view, name='chat_proxy'),
    path('chat-quota/', views.get_chat_quota, name='chat_quota'),
    path('tools/blood-test/', views.blood_test_view, name='blood_test'),
    path('tools/blood-test/upload/', views.proxy_upload_blood_test, name='proxy_upload_blood_test'),
    path('tools/blood-test/analyze/', views.proxy_analyze_blood_test, name='proxy_analyze_blood_test'),
    path('tools/blood-test/status/', views.check_blood_status_view, name='check_blood_status'),
    path('tools/blood-test/quota/', views.get_blood_quota, name='get_blood_quota'),
    path('tools/blood-test/check-credit/', views.check_available_credit, name='check_available_credit'),
    path('tools/blood-test/simulate-payment/', views.simulate_payment, name='simulate_payment'),
    
    # VITA Cloud Sync
    path('api/vita/history', views.load_vita_history_view, name='load_vita_history'),
    path('api/vita/save', views.save_vita_message_view, name='save_vita_message'),
    path('api/vita/clear', views.clear_vita_history_view, name='clear_vita_history'),
    
    # Widget State Sync
    path('api/widgets/state', views.load_widget_state_view, name='load_widget_state'),
    path('api/widgets/save', views.save_widget_state_view, name='save_widget_state'),
    path('api/widgets/rojito-increment', views.increment_rojito_count_view, name='increment_rojito_count'),

    path('', views.home, name='home')
]

handler404 = 'core.views.error_404_view'