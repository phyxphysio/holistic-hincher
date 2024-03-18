from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ("username", "email")

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)

        self.fields["username"].widget.attrs["placeholder"] = "Username"
        self.fields["username"].widget.attrs["style"] = "text-align:center;"

        self.fields["email"].widget.attrs["placeholder"] = "Email"
        self.fields["email"].widget.attrs["style"] = "text-align:center;"

        self.fields["password1"].widget.attrs["placeholder"] = "Password"
        self.fields["password1"].widget.attrs["style"] = "text-align:center;"

        self.fields["password2"].widget.attrs["placeholder"] = "Confirm Password"
        self.fields["password2"].widget.attrs["style"] = "text-align:center;"


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ("username", "email")


CLEANING_FREQUENCIES = [
    ("one-off", "One-off"),
    ("weekly", "Weekly"),
    ("fortnightly", "Fortnightly"),
    ("monthly", "Monthly"),
]
CLEANING_TYPE = [
    ("house", "House"),
    ("office", "Office"),
    ("presale", "Pre-sale clean"),
    ("spring", "Spring Clean"),
    ("bond/exit", "Bond or Exit Clean"),
    ("mum", "Cleaning for First-time Mums"),
    ("oven", "Oven Clean"),
    ("declutter", "Declutter and Organise"),
    ("airbnb", "Air BnB Clean"),
    ("outside", "Outdoor Patio Clean"),
    ("other", "Other (specify below)"),
]
HOME_SIZE = [
    ("n/a", "N/A"),
    ("1-2 bed", "1-2 bedrooms"),
    ("3-5 bed", "3-5 bedrooms"),
    (">5 bed", "More than 5 bedrooms"),
]
OFFICE_SIZE = [
    ("n/a", "N/A"),
    ("5-10 people", "5-10 people"),
    ("11-15 people", "11-15 people"),
    (">15 people", "More than 15 people"),
]
OTHER_SERVICES = [
    ("yoga", "Private Yoga"),
    ("pet sit", "Pet Sitting"),
    ("meal prep", "Meal Preparation"),
    ("other", "Other (specify below)"),
]


class ContactForm(forms.Form):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.EmailField()
    mobile = forms.CharField(max_length=100)
    street_address = forms.CharField(
        label="Street Address of the property",
        max_length=250,
    )
    post_code = forms.CharField(max_length=10)
    clean_type = forms.ChoiceField(
        label="What type of clean are you after?",
        choices=CLEANING_TYPE,
        widget=forms.Select(attrs={"class": "form-control"}),
        required=False,
    )
    clean_type = forms.MultipleChoiceField(
        choices=CLEANING_TYPE,
        label="What type of clean are you after?",
        required=False,
        widget=forms.CheckboxSelectMultiple,
    )
    clean_frequency = forms.MultipleChoiceField(
        label="How often should we come?",
        choices=CLEANING_FREQUENCIES,
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )
    home_size = forms.ChoiceField(
        required=False,
        label="How many bedrooms in the home?",
        widget=forms.Select(attrs={"class": "form-control"}),
        choices=HOME_SIZE,
    )
    office_size = forms.ChoiceField(
        required=False,
        label="How many people use the office?",
        widget=forms.Select(attrs={"class": "form-control"}),
        choices=OFFICE_SIZE,
    )
    other_services = forms.MultipleChoiceField(
        label="Are you interested in any of our other services?",
        choices=OTHER_SERVICES,
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    additonal_information = forms.CharField(widget=forms.Textarea, required=False)


FEEDBACK_CATEGORIES = [
    ("cleaning", "Cleaning"),
    ("business_coaching", "Business Coaching"),
    ("website", "Website"),
    ("other", "Other"),
]
SATISFACTION_RATINGS = [
    ("", ""),
    ("very satisfied", "Very satisfied"),
    ("satisfied", "Satisfied"),
    ("neutral", "Neutral"),
    ("dissatisfied", "Dissatisfied"),
    ("very dissatisfied", "Very dissatisfied"),
]
CLEANLINESS_RATINGS = [
    ("", ""),
    ("excellent", "Excellent"),
    ("good", "Good"),
    ("average", "Average"),
    ("poor", "Poor"),
    ("very poor", "Very poor"),
]
INSTRUCTIONS_FOLLOWED = [
    ("", ""),
    ("yes", "Yes, completely"),
    ("partially", "Yes, but partially"),
    ("no", "No, not at all"),
]
AREAS = [
    ("", ""),
    ("dusting/vaccumming", "Dusting and vacuuming"),
    ("kitchen/bedroom", "Kitchen & Bathrooms"),
    ("extra/rotational", "Extras & rotational items"),
    ("helpful/friendly", "Helpful & friendly manner"),
]
RECCOMMENDATION_CHOICES = [
    ("", ""),
    ("yes", "Yes, definitley"),
    ("maybe", "Yes, maybe"),
    ("probably not", "No, probably not"),
    ("no", "No, defnitley not"),
]


class FeedbackForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField(required=False, help_text="(Optional)")
    feedback_category = forms.ChoiceField(
        label="What is your feedback about?",
        choices=FEEDBACK_CATEGORIES,
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    feedback = forms.CharField(widget=forms.Textarea, required=False)
    satisfaction_rating = forms.ChoiceField(
        label="How satisfied were you with the overall cleaning service provided?",
        choices=SATISFACTION_RATINGS,
        required=False,
    )
    cleanliness_rating = forms.ChoiceField(
        label="How would you rate the cleanliness of your space after the cleaning?",
        choices=CLEANLINESS_RATINGS,
        required=False,
    )
    instructions_followed = forms.ChoiceField(
        label="Did the cleaner follow any specific instructions or requests you had given?",
        choices=INSTRUCTIONS_FOLLOWED,
        required=False,
    )
    areas_for_improvement = forms.ChoiceField(
        label="Areas for improvement",
        choices=AREAS,
        required=False,
    )
    areas_of_satisfaction = forms.ChoiceField(
        label="Areas of satisfaction",
        choices=AREAS,
        required=False,
    )
    would_reccommend = forms.ChoiceField(
        label="Would you recommend our cleaning services to others?",
        choices=RECCOMMENDATION_CHOICES,
        required=False,
    )
    additional_information = forms.CharField(
        label="Is there anything else you would like to share about your experience with our cleaning service?",
        widget=forms.Textarea,
        required=False,
    )
    contact_information = forms.CharField(
        label="Please provide your contact information if you would like us to follow up with you regarding your feedback",
        widget=forms.Textarea,
        required=False,
        help_text="Thank you for taking the time to complete this feedback form. We appreciate your input and look forward to serving you again in the future.",
    )
