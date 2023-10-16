# import pytest
# from free_pages.decorators import member_required 

# # Define test cases
# @pytest.mark.parametrize("is_authenticated, is_member, expected_result", [
#     (True, True, True),   # User is authenticated and a member
#     (True, False, False),  # User is authenticated but not a member
#     (False, True, False),  # User is not authenticated but is a member
#     (False, False, False)  # User is neither authenticated nor a member
# ])
# @pytest.mark.django_db
# def test_is_member_decorator(create_user, is_authenticated, is_member, expected_result):
#     # Create a mock user instance
#     def create_test_user():
#         user = create_user()
#         user.is_authenticated = is_authenticated
#         user.is_member = is_member
#         user.save()
#         yield user
    
#     user = create_test_user()

#     # Apply the decorator to a dummy function
#     @member_required
#     def dummy_function(request):
#         return "Success"

#     # Create a mock request object
#     request = type("Request", (), {"user": user})

#     # Check if the decorator behaves as expected
#     result = dummy_function(request)
#     assert (result == "Success") == expected_result
