import pytest
from django import forms
from django.conf import settings

from free_pages.models import CustomUser, MainCategory, SubCategory, Post


# Create fixtures
@pytest.fixture
def delete_test_user():
    try:
        test_member = CustomUser.objects.get(username="test_member")
        test_member.delete()
        print("test_member deleted")
    except CustomUser.DoesNotExist:
        print("No test_member yet.")
    return


@pytest.fixture
def domain():
    return settings.DOMAIN


@pytest.fixture
def django_admin_credentials():
    return settings.DJANGO_ADMIN_USERNAME, settings.DJANGO_ADMIN_PASSWORD


@pytest.fixture
def form_data_fixture():
    def generate_form_data(form_instance):
        form_data = {}
        for field_name, field in form_instance.fields.items():
            # Generate values for different types of fields
            if field_name == "email":
                form_data[field_name] = "sample@email.com"
            elif isinstance(field, forms.Textarea):
                form_data[field_name] = "More sample text"
            elif field_name == "post_code":
                form_data[field_name] = "1234"
            elif isinstance(field, forms.CharField):
                form_data[field_name] = "Sample Text"
            elif field_name == "email":
                form_data[field_name] = "sample@email.com"
            elif isinstance(field, forms.ChoiceField):
                # Set the value to the first choice in the choices list
                form_data[field_name] = field.choices[0][0]
            elif isinstance(field, forms.MultipleChoiceField):
                # Set the value to a list containing the first choice
                form_data[field_name] = [field.choices[0][0]]
            elif isinstance(field, forms.BooleanField):
                form_data[field_name] = True  # Example for a boolean field
            # Add more conditions for other field types as needed

        return form_data

    return generate_form_data


@pytest.fixture
def create_user(db):
    def make_user(is_member=False, stripe_customer_id=None):
        user = CustomUser.objects.create(
            username="test_user",
            email="test@example.com",
            is_member=is_member,
            stripe_customer_id=stripe_customer_id,
        )
        user.save()
        return user

    return make_user


@pytest.fixture
def create_main_category():
    main_category = MainCategory.objects.create(
        name="test_main_category",
        description="This main category is for testing",
    )
    yield main_category


@pytest.fixture
def create_sub_category(create_main_category):
    main_category_id = create_main_category.id
    instance = SubCategory.objects.create(
        name="test_sub_category",
        description="This sub category is for testing",
        category_id=main_category_id,
    )
    yield instance


@pytest.fixture
def create_post(create_sub_category, create_main_category):
    sub_category_id = create_sub_category.id
    main_category_id = create_main_category.id
    instance = Post.objects.create(
        title="test_post",
        description="This post category is for testing",
        subcategory_id=sub_category_id,
        main_category_id=main_category_id,
    )
    yield instance
