import json
from typing import Any

import stripe
from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import DetailView, FormView, ListView, TemplateView
from django.views.generic.edit import CreateView
from django.contrib.auth import login
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView

from .decorators import member_required, login_required
from .forms import ContactForm, FeedbackForm, CustomUserCreationForm
from .models import MainCategory, Post, SubCategory, CustomUser, MembershipBenefits

DOMAIN = settings.DOMAIN
stripe.api_key = settings.STRIPE_SECRET_KEY
EMAIL_RECIPIENT = settings.EMAIL_RECIPIENT

# Create your views here.


def home(request):
    return render(request, "free_pages/home.html")


class PasswordChangeSuccessView(TemplateView):
    template_name = "password_change/success.html"


class ChangePasswordView(PasswordChangeView):
    template_name = "password_change/change_password.html"
    form_class = PasswordChangeForm
    success_url = reverse_lazy("change_password_success")


@login_required
def create_checkout_session(request, price):
    # try:
    checkout_session = stripe.checkout.Session.create(
        line_items=[
            {
                "price": price,
                "quantity": 1,
            },
        ],
        mode="subscription",
        success_url=DOMAIN + "payment-success/",
        cancel_url=DOMAIN + "payment-cancelled/",
        client_reference_id=request.user.id,
    )

    # except Exception as e:
    #     print(f"Error: {e}")
    #     return HttpResponseServerError(
    #         "An error occurred during checkout. \
    #                                     Please try again later."
    #     )

    return redirect(checkout_session.url)


def customer_portal(request):
    user = request.user
    return_url = DOMAIN

    portalSession = stripe.billing_portal.Session.create(
        customer=user.stripe_customer_id,
        return_url=return_url,
    )
    return redirect(portalSession.url, code=303)


@csrf_exempt
def webhook_received(request):
    if request.method == "POST":
        payload = request.body
        event = None

        try:
            event = stripe.Event.construct_from(json.loads(payload), stripe.api_key)
        except ValueError as e:
            # Invalid payload
            return HttpResponse(f"There was a problem: {e}", status=400)

        # Handle the event
        if event["type"] == "checkout.session.completed":
            session = event["data"]["object"]

            client_reference_id = session.get("client_reference_id")
            stripe_customer_id = session.get("customer")

            if not event["livemode"]:
                try:
                    user = CustomUser.objects.get(id=client_reference_id)

                    user.stripe_customer_id = stripe_customer_id
                    user.is_member = True
                    user.save()
                    print(f"{user} just subscribed")
                except CustomUser.DoesNotExist:
                    print("Stripe test customer not in database")
                    return HttpResponse(status=200)
            else:
                user = CustomUser.objects.get(id=client_reference_id)

                user.stripe_customer_id = stripe_customer_id
                user.is_member = True
                user.save()
                print(f"{user} just subscribed")

        elif event["type"] == "customer.subscription.deleted":
            session = event["data"]["object"]
            customer_id = session.get("customer")

            if not event["livemode"]:
                try:
                    user = CustomUser.objects.get(stripe_customer_id=customer_id)
                    user.is_member = False
                    user.save()
                    print(
                        f"{user.username} subscription has been deleted and they are\
                    no longer a member."
                    )
                except CustomUser.DoesNotExist:
                    print("Stripe test customer not in db")
                    return HttpResponse(status=200)
            else:
                user.is_member = False
                user.save()
                print(
                    f"{user.username} subscription has been deleted and they are\
                no longer a member."
                )

            return HttpResponse(status=200)

        return HttpResponse(status=200)


class PaymentSuccess(TemplateView):
    template_name = "payment/success.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        checkout_session_id = self.request.GET.get("session_id")

        subscription_id = self.request.GET.get("subscription")

        client_reference_id = self.request.GET.get("client_reference_id")

        # Retrieve payment intent details
        if checkout_session_id:
            print("GOT CHECKOUT SESSION ID")
            checkout_session = stripe.checkout.Session.retrieve(checkout_session_id)
            context["checkout_session"] = checkout_session

            # Save payment intent information to UserProfile
            user = CustomUser.objects.get(pk=client_reference_id)
            user.stripe_customer_id = checkout_session.customer
            user.save()

        # Retrieve subscription details
        if subscription_id:
            subscription = stripe.Subscription.retrieve(subscription_id)
            context["subscription"] = subscription

            # Update UserProfile to indicate user is a member
            user = CustomUser.objects.get(pk=client_reference_id)
            user.is_member = True
            user.save()

        return context


class PaymentCancelled(TemplateView):
    template_name = "payment/error.html"


def list_memberships(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    try:
        benefits = MembershipBenefits.objects.get(pk=1).benefits

    except MembershipBenefits.DoesNotExist:
        benefits = None

    memberships = stripe.Product.list(active=True)
    prices = stripe.Price.list()
    return render(
        request,
        "registration/memberships.html",
        {"memberships": memberships, "prices": prices, "benefits": benefits},
    )


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("memberships")
    template_name = "registration/signup.html"

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response


class ContactFormView(FormView):
    form_class = ContactForm
    template_name = "free_pages/contact_form.html"
    success_url = reverse_lazy("form_success")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            post = Post.objects.get(title="Cleaning Services")
        except Post.DoesNotExist:
            post = None

        if self.request.method == "POST":
            form = self.form_class(self.request.POST)
            context["form"] = form

        else:
            form = self.form_class()

        fields = list(form)

        index_pairs = [
            (fields[i], fields[i + 1])
            for i in range(0, len(fields), 2)
            if i + 1 < len(fields)
        ]

        context["post"] = post
        context["index_pairs"] = index_pairs

        return context

    def form_valid(self, form):
        # form.add_error('email', 'This is a global form error.')
        # form.add_error('field_name', 'This is a field-specific error.')

        cleaned_data = form.cleaned_data

        message = compose_message(cleaned_data)

        subject = f'New Business Enquiry from {cleaned_data["first_name"]} {cleaned_data["last_name"]}'

        from_email = cleaned_data["email"]
        recipient_list = EMAIL_RECIPIENT
        send_mail(subject, message, from_email, recipient_list, fail_silently=False)
        return super().form_valid(form)


class AboutView(TemplateView):
    template_name = "free_pages/about.html"


def clean_field_name(field_name):
    words = field_name.split("_")
    cleaned_name = " ".join(word.capitalize() for word in words)
    return cleaned_name


def clean_field_value(field_value):
    # Check if the field_value is a list
    if not field_value:
        return "N/A"

    elif isinstance(field_value, list):
        # Initialize an empty list to store cleaned values
        cleaned_values = []

        # Loop through each item in the list
        for item in field_value:
            # Strip brackets and quotes, capitalize, and add to the cleaned list
            cleaned_item = item.strip("[]").replace('"', "").strip().capitalize()
            cleaned_values.append(cleaned_item)

        # Join the cleaned values into a string with comma and space
        cleaned_result = ", ".join(cleaned_values)
    else:
        # If it's not a list, strip brackets and quotes, capitalize, and assign to cleaned_result
        cleaned_result = field_value.strip("[]").replace('"', "").strip().capitalize()

    return cleaned_result


def compose_message(cleaned_data):
    message = ""
    for field_name, field_value in cleaned_data.items():
        if not field_value:
            continue
        message += (
            f"{clean_field_name(field_name)}: {clean_field_value(field_value)}\n\n"
        )
    return message


class FeedbacktFormView(FormView):
    form_class = FeedbackForm
    template_name = "free_pages/feedback_form.html"
    success_url = reverse_lazy("form_success")

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        if self.request.method == "POST":
            form = self.form_class(self.request.POST)
            context["form"] = form
        return context

    def form_valid(self, form):
        name = form.cleaned_data["name"]
        email = form.cleaned_data["email"]
        cleaned_data = form.cleaned_data

        feedback_category = cleaned_data["feedback_category"]
        if feedback_category == "cleaning":
            del cleaned_data["feedback"]
        message = compose_message(cleaned_data)
        subject = f"New Feedback from {name.capitalize()}"
        from_email = email
        recipient_list = EMAIL_RECIPIENT
        send_mail(subject, message, from_email, recipient_list, fail_silently=False)
        return super().form_valid(form)


class FormSuccessView(TemplateView):
    template_name = "free_pages/form_success.html"


@method_decorator(member_required, name="dispatch")
class MemberResourcesView(TemplateView):
    template_name = "free_pages/member_resources.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Retrieve data from your models
        main_categories = MainCategory.objects.all()
        subcategories = SubCategory.objects.all()
        posts = Post.objects.all()

        # Add the data to the context dictionary
        context["main_categories"] = main_categories
        context["subcategories"] = subcategories
        context["posts"] = posts

        return context


@method_decorator(member_required, name="dispatch")
class MainCategoryListView(ListView):
    model = MainCategory
    template_name = "free_pages/member_resources.html"
    context_object_name = "main_categories"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        subcategories = SubCategory.objects.get(pk=1)
        self.context["subcategores"] = subcategories
        return context


@method_decorator(member_required, name="dispatch")
class SubCategoryListView(ListView):
    model = SubCategory
    template_name = "free_pages/subcategories.html"
    context_object_name = "subcategories"

    def get_context_data(self, **kwargs):
        category_slug = self.kwargs["category_slug"]
        context = super().get_context_data(**kwargs)
        context["main_category_slug"] = category_slug
        return context

    def get_queryset(self):
        category_slug = self.kwargs["category_slug"]
        category = MainCategory.objects.filter(slug=category_slug)[0]
        queryset = SubCategory.objects.filter(category=category)
        return queryset


@method_decorator(member_required, name="dispatch")
class PostListView(ListView):
    model = Post
    template_name = "free_pages/posts.html"
    context_object_name = "posts"

    def get_context_data(self, **kwargs):
        category_slug = self.kwargs["category_slug"]
        subcategory_slug = self.kwargs["subcategory_slug"]

        context = super().get_context_data(**kwargs)
        context["main_category_slug"] = category_slug
        context["subcategory_slug"] = subcategory_slug
        return context

    def get_queryset(self):
        subcategory_slug = self.kwargs["subcategory_slug"]
        subcategory = SubCategory.objects.filter(slug=subcategory_slug)[0]
        queryset = Post.objects.filter(subcategory=subcategory)
        return queryset


@method_decorator(member_required, name="dispatch")
class PostDetailView(DetailView):
    model = Post
    template_name = "free_pages/post_detail.html"
    context_object_name = "post"
    slug_field = "slug"
    slug_url_kwarg = "post_slug"
