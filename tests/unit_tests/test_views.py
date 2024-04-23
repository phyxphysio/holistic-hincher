import pytest
from django.urls import reverse
from free_pages.forms import FeedbackForm


def test_home_view(client):
    url = reverse("home")
    response = client.get(url)
    assert response.status_code == 200


def test_about_view(client):
    url = reverse("about")
    response = client.get(url)
    assert response.status_code == 200

@pytest.mark.django_db
def test_memberships_view(client):
    url = reverse("memberships")
    response = client.get(url)
    assert response.status_code == 200

@pytest.mark.django_db
def test_cleaning_services_view(client, form_data_fixture):
    url = reverse("cleaning_services")
    response = client.get(url)
    assert response.status_code == 200

    # Test form submission
    # form_instance = ContactForm()
    # form_data = form_data_fixture(form_instance)
    # response = client.post(url, form_data)
    # print(response.content.decode("utf-8"))
    # assert response.status_code == 200

    # # # Test email has been sent
    # assert len(mail.outbox) == 1
    # sent_email = mail.outbox[0]
    # assert "Sample text" in sent_email.body

def test_contact_info_view(client):
    url = reverse('contact_info')
    response = client.get(url)
    assert response.status_code == 200

def test_feedback_view(client, form_data_fixture):
    url = reverse("feedback")
    response = client.get(url)
    assert response.status_code == 200

    # Test form submission
    form_instance = FeedbackForm()
    form_data = form_data_fixture(form_instance)
    response = client.post(url, form_data)
    assert response.status_code == 200

    # # Test email has been sent
    # assert len(mail.outbox) == 1
    # sent_email = mail.outbox[0]
    # assert "Sample text" in sent_email.body


@pytest.mark.django_db
@pytest.mark.parametrize("is_member", [True, False])
def test_member_resources_view(client, create_user, is_member):
    user = create_user(is_member)
    client.force_login(user)
    url = reverse("member_resources")
    response = client.get(url)
    if user.is_member:
        assert response.status_code == 200
        assert (
            "member resources" in response.content.decode("utf-8").lower()
        )  # Check for 'member resources' in lowercase
    else:
        assert response.status_code == 302  # Non-member should be denied access


@pytest.mark.django_db
@pytest.mark.parametrize("is_member", [True, False])
def test_subcategory_and_post_view(
    client,
    create_post,
    create_user,
    create_sub_category,
    is_member,
    create_main_category,
):
    user = create_user(is_member)
    category = create_main_category
    subcategory = create_sub_category
    post = create_post
    client.force_login(user)
    subcategory_url = reverse("subcategories", kwargs={"category_slug": category.slug})
    posts_url = reverse(
        "posts",
        kwargs={"category_slug": category.slug, "subcategory_slug": subcategory.slug},
    )
    post_detail_url = reverse(
        "post_detail",
        kwargs={
            "category_slug": category.slug,
            "subcategory_slug": subcategory.slug,
            "post_slug": post.slug,
        },
    )
    urls = [subcategory_url, posts_url, post_detail_url]
    for url in urls:
        response = client.get(url)
        if user.is_member:
            assert response.status_code == 200
        else:
            assert response.status_code == 302


