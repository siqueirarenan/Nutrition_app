from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from Main.views import *
from django.conf.urls.static import static
from rest_framework import routers
from django.contrib.auth import views as auth_views
from allauth.socialaccount import views as allauth_views
from allauth.account import views as allauth_views2
from Main.admin import admin_site

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'recipes', RecipeViewSet)
router.register(r'surveyvotes', SurveyVoteViewSet)
router.register(r'users', UserViewSet)

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('myadmin/', admin_site.urls),
                  path('', include('Main.urls')),
                  path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
                      template_name="registration/passwordResetConfirm.html",
                      post_reset_login=True,
                      post_reset_login_backend='django.contrib.auth.backends.ModelBackend'),
                       name='password_reset_confirm'), #Included here because the app uses defaul email for reset
                  path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
                      template_name="registration/passwordResetDone.html"),
                       name='password_reset_done'),
                  path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
                      template_name="registration/passwordResetComplete.html"),
                       name='password_reset_complete'),

                  path("accounts/inactive/", allauth_views2.AccountInactiveView.as_view(template_name="socialaccount/inactive.html"),
                       name="account_inactive"),
                  path("accounts/social/signup/", allauth_views.SignupView.as_view(template_name="socialaccount/sign_up.html"),
                       name="socialaccount_signup"),
                  path('accounts/', include('allauth.urls')),




                  path('api/', include(router.urls)),
                  #path('api-auth/', include('rest_framework.urls'))
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

