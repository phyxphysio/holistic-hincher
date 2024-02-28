from django.urls import path
from . import views
from .views import (
    MainCategoryListView,
    SubCategoryListView,
    PostListView,
    PostDetailView,
    ContactFormView,
    FeedbacktFormView,
    FormSuccessView,
    AboutView,
    MemberResourcesView,
    OfferingsView,
    ContactInfoView,
)

urlpatterns = [
    path("", views.home, name="home"),
    path("member-resources/", MemberResourcesView.as_view(), name="member_resources"),
    path(
        "member-resources/<slug:category_slug>/",
        SubCategoryListView.as_view(),
        name="subcategories",
    ),
    path(
        "member-resources/<slug:category_slug>/<slug:subcategory_slug>/",
        PostListView.as_view(),
        name="posts",
    ),
    path(
        "member-resources/<slug:category_slug>/<slug:subcategory_slug>/<slug:post_slug>/",
        PostDetailView.as_view(),
        name="post_detail",
    ),
    path("cleaning-services", OfferingsView.as_view(), name="cleaning_services"),
    path("feedback", FeedbacktFormView.as_view(), name="feedback"),
    path("success", FormSuccessView.as_view(), name="form_success"),
    path("about", AboutView.as_view(), name="about"),
    path("contact-info/", ContactInfoView.as_view(), name="contact_info"),

]
