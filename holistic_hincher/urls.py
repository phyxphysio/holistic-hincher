"""
URL configuration for holistic_hincher project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path, re_path
from django.contrib.sitemaps.views import sitemap
from .sitemaps import StaticViewSitemap

from free_pages import views
from free_pages.views import (
    ChangePasswordView,
    PasswordChangeSuccessView,
    PaymentCancelled,
    PaymentSuccess,
    SignUpView,
)

sitemaps = {
    "static": StaticViewSitemap,
}

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.sitemap",
    ),
    path("", include("free_pages.urls")),
    re_path(r"^ckeditor/", include("ckeditor_uploader.urls")),
    path("login/", auth_views.LoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("payment-success/", PaymentSuccess.as_view(), name="payment_sucess"),
    path("payment-cancelled/", PaymentCancelled.as_view(), name="payment_cancelled"),
    path("create-customer-portal/", views.customer_portal, name="customer_portal"),
    path("webhook/", views.webhook_received, name="webhook"),
    path("change-password/", ChangePasswordView.as_view(), name="change_password"),
    path(
        "change-password/success/",
        PasswordChangeSuccessView.as_view(),
        name="change_password_success",
    ),
    path(
        "password-reset/", auth_views.PasswordResetView.as_view(), name="password_reset"
    ),
    path(
        "password_reset/done/",
        auth_views.PasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
    path("signup/", SignUpView.as_view(), name="signup"),
    path("payment/<price>", views.create_checkout_session, name="payment"),
    path("memberships/", views.list_memberships, name="memberships"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)