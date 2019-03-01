from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
# from django.contrib.auth.backends import ModelBackend

class EmailBackend(object):
    def authenticate(self, username=None, password=None):
        if '@' in username:
            kwargs = {'email': username}
        else:
            kwargs = {'username': username}
        try:
            user = get_user_model().objects.get(**kwargs)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None

    def get_user(self, username):
        try:
            return get_user_model().objects.get(pk=username)
        except get_user_model().DoesNotExist:
            return None








# class EmailBackend(ModelBackend):
#     def authenticate(self, email=None,username=None, password=None, **kwargs):
#         UserModel = get_user_model()
#         try:
#             user = UserModel.objects.get(email=username)
#         except UserModel.DoesNotExist:
#             return None
#         else:
#             if user.check_password(password):
#                 return user
#         return None

# class UsernameBackend(ModelBackend):
#     def authenticate(self, email=None,password=None, **kwargs):
#         user = get_user_model()
#         try:
#             login_user = user.objects.get(username=email)
#         except user.DoesNotExist:
#             return None
#
#         else:
#             if user.check_password(password):
#                 return login_user
#
#         return None
