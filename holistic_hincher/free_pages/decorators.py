# decorators.py
from django.contrib.auth.decorators import user_passes_test


def is_member(user):
    try:
        return user.is_authenticated and user.is_member
    except user.DoesNotExist:
        return False


member_required = user_passes_test(is_member, login_url="memberships")


def is_user(user):
    try:
        return user.is_authenticated
    except user.DoesNotExist:
        return False


login_required = user_passes_test(is_user, login_url="login")
