from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

from django.urls import path

from django.contrib.auth import views as auth_views

from allauth.account.forms import LoginForm
from allauth.account.views import LoginView

from allauth.account import views as allauth_views 

from .views import save_interest_answer

urlpatterns = [
    path('', views.login_view, name='login'),
    path('login/', views.login_view, name='login'),
    path('accounts/password/reset/', auth_views.PasswordResetView.as_view(
        template_name='registration/password_reset_form.html'  # ⬅ your custom template path
    ), name='password_reset'),

    path('accounts/login/', views.login_view, name='login'),

    path('accounts/password/reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='registration/password_reset_done.html'  # Your custom done page
    ), name='password_reset_done'),
    
    path('accounts/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='registration/password_reset_confirm.html'  # Your custom reset form
    ), name='password_reset_confirm'),
    
    path('accounts/reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='registration/password_reset_complete.html'  # Your custom complete page
    ), name='password_reset_complete'),
    
    path('signup/', views.signup_view, name='signup'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    
    path('profile/', views.profile_view, name='profile'),

   


    path('assessment/', views.assessment_view, name='assessment'),
    
    path('domains/', views.domain_list_view, name='domain_list'),
    path('domain-test/<int:domain_id>/', views.domain_test_view, name='domain_test'),

    path('interest_questions/', views.interest_questions_view, name='interest_questions'),
    path("save-answer/", views.save_interest_answer, name="save_interest_answer"),
    path("submit-test/", views.submit_interest_test, name="submit_interest_test"),

    path('interest-result/', views.interest_result_view, name='interest_result'),
    path('domain-tests/<int:domain_id>/', views.start_test, name='start_test'),
    path('submit_test/<int:domain_id>/', views.submit_test, name='submit_test'),
    path('domain-result/<int:domain_id>/', views.domain_result_view, name='domain_result'),
    path('domain-history/', views.domain_result_history_view, name='domain_result_history'),
    path('generate-roadmap/<int:domain_id>/', views.roadmap_view, name='generate_roadmap'),
    path('roadmap/', views.roadmap_view, name='roadmap'),
    
    path('domains/', views.domains_view, name='domains'),
    
    path('roadmap/', views.roadmap_view, name='roadmap'),
    path('courses/', views.courses_view, name='courses'),
    path('progress/', views.progress_view, name='progress'),
    path('update-progress/', views.update_progress_view, name='update_progress'),
    path('reset-progress/', views.reset_progress_view, name='reset_progress'),

    path('terms/', views.terms_view, name='terms'),
    path('logout/', views.logout_view, name='logout'),

      
    # Let allauth handle everything under /accounts/
    path('accounts/', include('allauth.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

