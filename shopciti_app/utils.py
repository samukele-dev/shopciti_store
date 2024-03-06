from django.contrib.auth import get_user_model

def check_user_registration(email, phone):
    User = get_user_model()
    try:
        # Check if a user with the given email and phone exists
        user = User.objects.get(email=email, customuser__profile__phone_number=phone)
        return True  # User is registered
    except User.DoesNotExist:
        return False  # User is not registered