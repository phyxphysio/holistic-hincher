import pytest

@pytest.mark.django_db
def test_user_creation(create_user):
    instance = create_user()
    assert instance.__str__() == "test_user"

@pytest.mark.django_db
def test_main_category_creation(create_main_category):
    instance = create_main_category
    assert instance.__str__() == "test_main_category"

@pytest.mark.django_db
def test_sub_category_creation(create_sub_category):
    
    instance = create_sub_category
    assert instance.__str__() == "test_sub_category"

@pytest.mark.django_db
def test_post_creation(create_post):
    instance = create_post
    assert instance.__str__() == "test_post"


